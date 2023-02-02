# Mike21-model-data-processing
Pre and post data processing for mike21 hydrodynamic and environmental model.

I have been self-studying the MIKE21 hydrodynamic and environmental modeling, and have explored some codes for data preprocessing and postprocessing. I have saved these codes here for reference by colleagues who may need them

At present, it mainly includes the extraction of boundary and water depth before modeling, the drawing of tide, velocity and flow direction verification charts, the affected area of oil spill simulation results, and the time and proportion of affecting the main sensitive areas.


F1. ezdxf_get_boundary_xyz.py
Translate DXF file shoreline to XYZ file needed for mesh creation in Mike21 software using the ezdxf library.

F2. ezdxf_get_depth_xyz.py
Translate DXF file water depth points to XYZ file needed for mesh creation in Mike21 software using the ezdxf library.

F3_0. matplotlib_Verification diagram_tide.py
Draw a tidal level validation comparison chart in the model calculation results using the matplotlib library.

F3_1. matplotlib_Verification diagram_speed.py
Draw a flow velocity validation comparison chart in the model calculation results using the matplotlib library.

F3_2. matplotlib_Verification diagram_direction.py
Draw a flow direction validation comparison chart in the model calculation results using the matplotlib library.

F4. Mikeio_OS_affect_area.py
Use the mikeio library to calculate the oil spill impact area in the model calculation results.

F5. Mikeio_OS_arrival_time.py
Use the mikeio library to calculate the time and extent of oil spill impact reaching surrounding important sensitive areas in the model calculation results.
