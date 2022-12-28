import pandas as pd
from mikeio import Dfsu
import ezdxf, os, isPointsinPolygons

# Step 1: Identify sensitive areas
dxf_filename = 'Sensitive_area.dxf'
doc = ezdxf.readfile(dxf_filename)
msp = doc.modelspace()
polylines = msp.query('LWPOLYLINE')
Sensitive_area_polygons_lists = []
for pline in polylines:
    polygons_list = []
    for point in pline:
        polygons_list.append(point)
    polygons_list.append(polygons_list[0])
    Sensitive_area_polygons_lists.append(polygons_list)     # Put each sensitive area polygons in a list.

# Step 2 Number sensitive areas, The number of the sensitive area is saved to the file during the first operation,
# and the file is read directly during the next operation.
dfsu_file = 'OS_result.dfsu'
dfs = Dfsu(dfsu_file)
ds = dfs.read()
meshinfo = pd.DataFrame(dfs.element_coordinates, columns=['x', 'y', 'z'])
mesharea = pd.DataFrame(dfs.get_element_area())
meshinfo['area'] = mesharea
meshinfo['SAN'] = 0                                         # SAN: Abbreviation of "Sensitive Area Nubmer".

if not os.path.exists(dxf_filename.replace('.dxf', '_Sensitive_area_number.csv')):
    for index, row in meshinfo.iterrows():
        x = row[0]
        y = row[1]
        point0 = [x, y]
        meshinfo.loc[index, 'SAN'] = 0
        for ns, plist in enumerate(Sensitive_area_polygons_lists):
            if isPointsinPolygons.isPointinPolygon(point0, plist):
                meshinfo.loc[index, 'SAN'] = ns + 1           # Start numbering from 1 for multiple sensitive areas
    meshinfo.to_csv(dxf_filename.replace('.dxf', '_Sensitive_area_number.csv'))
else:
    meshinfo = pd.read_csv(dxf_filename.replace('.dxf', '_Sensitive_area_number.csv'))

# Step 3 is to calculate the time point when the cell concentration within the sensitive area reaches the specified
# minimum concentration, and the affected area of the sensitive area and its proportion.
arrival_time_area_list = []
for ns in range(1, len(Sensitive_area_polygons_lists) + 1):
    Sensitive_area_mesh = meshinfo[meshinfo['SAN'] == ns].index  # Filter the area index with SAN = ns
    # The sum of the four components of the spilled oil is the total spilled oil concentration
    Oil_sum = pd.DataFrame(ds[0].values + ds[1].values + ds[2].values + ds[3].values).loc[:, Sensitive_area_mesh]

    # Processing arrival time
    # The maximum oil spill concentration of all element within the sensitive area is taken as axis=1 in the column.
    Oil_sum_max_by_mesh = Oil_sum.max(axis=1)
    # The minimum index of oil spill concentration>0.05 in the time series is the time when the oil spill reaches
    # the sensitive area, It is converted into hours according to the time step of the model.
    arrival_time = Oil_sum_max_by_mesh[Oil_sum_max_by_mesh > 0.05].index.min() * dfs.timestep / 3600

    # Processing affected area
    # The maximum oil spill concentration of all elements in the sensitive area shall be taken as axis=0.
    Oil_sum_max_by_time = Oil_sum.max(axis=0)
    # Merging elements area and Concentration Maximum Data
    # join='inner 'indicates that the common part of the data is obtained by merging.
    # Here mesharea contains all meshes, And Oil_sum_max_by_Time only contains sensitive area ns.
    Sensitive_area_df = pd.concat([mesharea, Oil_sum_max_by_time], axis=1, join='inner')
    Sensitive_area_df.columns = ['area', 'c']
    arrival_area = Sensitive_area_df.query('c >= 0.05')['area'].sum()     #Affected area in sensitive area ns
    Sensitive_area = round(Sensitive_area_df['area'].sum(), 0)            #Total area of sensitive area ns
    ratio = '{:.0%}'.format(round(arrival_area / Sensitive_area, 2))      #Integer of percentage

    #Save arrival time and affected area
    arrival_time_area_list.append([ns, arrival_time, 'hours', arrival_area, 'm2', Sensitive_area, ratio])
    print(ns, arrival_time, 'hours', arrival_area, 'm2', ratio)

arrival_time_area_dfs = pd.DataFrame(arrival_time_area_list)
arrival_time_area_dfs.fillna('/', inplace=True)
arrival_time_area_dfs.to_csv('Oil_arrival_time_area.txt', sep='\t', header=None, index=False)

