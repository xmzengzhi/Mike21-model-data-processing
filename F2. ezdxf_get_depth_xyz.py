import ezdxf                                                       #Import Library File
fw = open('depth.xyz', 'w')                                        #Prepare Output File: depth.xyz
doc = ezdxf.readfile('depth.dxf')                                  #Read depth.dxf file
msp = doc.modelspace()                                             #Getting the model space layout
for flag_ref in msp.query('INSERT'):                               #iterate over all INSERT in model space
    x = flag_ref.dxf.all_existing_dxf_attribs()['insert'][0]
    y = flag_ref.dxf.all_existing_dxf_attribs()['insert'][1]
    z = flag_ref.get_attrib_text('height')
    fw.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')          #Write data in XYZ format
fw.close()

