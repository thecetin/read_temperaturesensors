# read_temperaturesensors
Three temperature sensors are reading with raspberry pi and showing on python written dashboard

This Python script is designed to read temperature data from three temperature sensors and display them on a PySimpleGUI-based dashboard. The script uses the w1-gpio and w1-therm modules to communicate with the sensors and reads the temperature data using the read_temp() function. The temperature readings are displayed on the dashboard and if the temperature exceeds the user-set warning temperature, the corresponding sensor's label will display a warning message.

The script also provides a user interface for changing the warning temperature for each sensor by clicking the corresponding "Change warning temp" button and entering the new temperature value in the input field.

Overall, this script can be useful for monitoring temperature data in a variety of settings, such as in a laboratory or greenhouse.
