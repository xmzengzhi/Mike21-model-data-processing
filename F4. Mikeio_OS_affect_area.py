import pandas as pd
from mikeio import Dfsu

dfs = Dfsu('OS_result.dfsu')
meshinfo = pd.DataFrame(dfs.element_coordinates)     # Get the element coordinate, as x, y, z format
mesharea = pd.DataFrame(dfs.get_element_area())      # Get the element area
ds = dfs.read()
# The sum of the four components of the spilled oil is the total spilled oil concentration
Oil_sum = pd.DataFrame(ds[0].values + ds[1].values + ds[2].values + ds[3].values)

hours = [1, 3, 6, 9, 12, 24, 48, 72]   #Specify the impact time period to be calculated
for h in hours:
    # Get the maximum concentration of each element from time 0 to the specified time for oil spill concentration
    mesh_max_c = Oil_sum[:int(h * 3600 / ds.timestep)].max()
    # Merge element coordinate, maximum concentration and element area
    surfer_file = pd.concat([meshinfo, mesh_max_c, mesharea], axis=1)
    surfer_file.columns = ['x', 'y', 'z', 'c', 'area']        # Specify the merged data column header
    # Output file for Surfer drawing
    surfer_file.to_csv(str(h) + 'Hours_OilSpill4surfer.dat', sep='\t', header=None, index=False)

    # Filter all element data and retain the part with concentration >= 0.05
    filter_c = surfer_file.query('c >= 0.05')
    # The sum of the filter element areas is the sum of the Oil sweeping sea areas
    filter_area = filter_c['area'].sum()
    print(str(h) + 'Hours', filter_area)
