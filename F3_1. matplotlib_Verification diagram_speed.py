import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = pd.read_excel("Calibration_current.xlsx", sheet_name='speed')       #Read the speed sheet.
Stations = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
for s in Stations:
    x = data['TimeSeries']
    y1 = data[s + '_measured']
    y2 = data[s + '_simulated']
    fig = plt.figure(figsize=(10, 4), dpi=200)                             #Prepare a graphic space 10 wide and 4 high
    # Draw a scatter plot with x and y1, the color is blue, the line width is 3, and the size of the dot is 8
    plt.plot(x, y1, color='blue', linestyle=' ', linewidth=3, marker='.', markersize=8)
    plt.plot(x, y2, color='red')                                           #Draw a line graph with x and y2 in red
    plt.xlabel('TimeSeries', {'weight': 'normal', 'size': 16})             #Set X axis label as Timeseries
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(4))           #Set X axis data ticker interval to 2
    plt.ylabel('Speed(m/s)', {'weight': 'normal', 'size': 16})             #Set y-axis label to Speed(m/s)
    plt.ylim([0, 0.8])
    plt.legend((s + '_measured', s + '_simulated'), loc='best')            #Set the legend in the best position
    plt.savefig('images\\' + s + '_speed.svg', format='svg')               #Save the image in svg format
