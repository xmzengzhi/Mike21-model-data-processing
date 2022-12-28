import ezdxf
fw = open('boundary.xyz', 'w')                                         #Prepare Output File: boundary.xyz
doc = ezdxf.readfile('boundary.dxf')                                   #Read boundary.dxf file
msp = doc.modelspace()                                                 #Getting the model space layout
polylines = msp.query('LWPOLYLINE')                                    #Get all LWPOLYLINE entities from the model space
for pline in polylines:                                                #Iterate over all LWPOLYLINE in model space
    for index, point in enumerate(pline):                              #Iterate every point on the polyline
        x, y = point[0], point[1]                                      #Get the x, y coordinates of each point
        fw.write(str(x) + ' ' + str(y) + ' 1\n')                       #Write data in XYZ format
    fw.write(str(pline[0][0]) + ' ' + str(pline[0][1]) + ' 0\n')       #Write the first data to close the polygon
fw.close()
