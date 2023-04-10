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
    mesh_max_dfs = pd.concat([meshinfo, mesh_max_c, mesharea], axis=1)
    mesh_max_dfs.columns = ['x', 'y', 'z', 'c', 'area']        # Specify the merged data column header

    # Filter all element data and retain the part with concentration >= 0.05
    filter_c = mesh_max_dfs.query('c >= 0.05')
    # The sum of the filter element areas is the sum of the Oil sweeping sea areas
    filter_area = filter_c['area'].sum()
    print(str(h) + 'Hours', filter_area)

    # Calculate interpolation
    x, y, z = mesh_max_dfs["x"], mesh_max_dfs["y"], mesh_max_dfs['c']
    x_interp = np.linspace(x.min(), x.max(), int((x.max() - x.min()) // 1000))
    y_interp = np.linspace(y.min(), y.max(), int((y.max() - y.min()) // 1000))
    x_interp, y_interp = np.meshgrid(x_interp, y_interp)
    z_interp = griddata((x, y), z, (x_interp, y_interp), method='nearest')

    # Draw contour maps
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  # Set the aspect ratio of the graph, with 'equal' being constant
    OS_levels = (0.05, 0.5, 1, 10, 100, 9999)
    OS_cmap = ('#99FFFF', 'Yellow', 'Orange', 'Red', '#CC33FF')
    cs = ax.contourf(x_interp, y_interp, z_interp, levels=OS_levels, colors=OS_cmap)

    cbar = fig.colorbar(cs, shrink=0.618)  # shrink: Legend Box Scale Adjustment Factor
    cbar.set_label('mg/L')
    cbar.set_ticks(OS_levels)
    new_data = lambda x: '' if x == 9999 else x
    cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{}'.format(new_data(x))))

    # Read the base map dxf file
    import ezdxf
    basemap_file = "basemap.dxf"
    doc = ezdxf.readfile(basemap_file)
    msp = doc.modelspace()
    polylines = msp.query('LWPOLYLINE')
    polygons = []
    for pline in polylines:
        x0, y0 = [], []
        for point in pline:
            x0.append(point[0]); y0.append(point[1])
        x0.append(x0[0]); y0.append(y0[0])   # Add the first point of the polyline for later drawing to close
        plt.fill(x0, y0, color='lightgray')  # Area Fill
        plt.plot(x0, y0, color='k', linewidth=0.5)  # Border Line
    ax.margins(0)

    plt.savefig(str(h) + 'Hours_contour.svg', format='svg')
