import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("Calibration_tide.xlsx")                    #Read Calibration_tide.xlsx table.
Stations = ['T1', 'T2']
for s in Stations:
    x = data['TimeSeries']                                       #Set the x-axis data, same as the Excel table title
    y1 = data[s + '_measured']                                   #Set y-axis data: T1_measured or T2_measured
    y2 = data[s + '_simulated']                                  #Set y-axis data: T1_simulated or T2_simulated
    fig = plt.figure(figsize=(12, 3.6))                          #Prepare a graphic space 12 wide and 3.6 high
    # Draw a scatter plot with x and y1, the color is blue, the line width is 3, and the size of the dot is 8
    plt.plot(x, y1, color='blue', linestyle=' ', linewidth=3, marker='.', markersize=8)
    plt.plot(x, y2, color='red')                                 #Draw a line graph with x and y2 in red
    plt.xlabel('TimeSeries')                                     #Set X axis label as Timeseries
    plt.ylabel('Water level(m)')                                 #Set y-axis label to Water lever(m)
    plt.legend((s + '_measured', s + '_simulated'), loc='best')  #Set the legend in the best position
    plt.savefig('images\\' + s + '_tide.svg', format='svg')      #Save the image in svg format
