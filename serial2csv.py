import serial
import csv

arduino_port = "/dev/cu.usbmodem14301"
baud = 115200
filename="mpu6050-data.csv"
nsamples = 3000

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)

print_labels = False
line = 0 #start at 0 because our header is 0 (not real data)
sensor_data = [] #store data

print("Collecting samples..")

# collect the samples
dmpReady = False
while line <= nsamples:
    getData = ser.readline()
    dataString = getData.decode('utf-8')

    if dmpReady:
        data = dataString[:-4].split(',')
        readings = [float(x) for x in data]
        print(line,':',readings)
        sensor_data.append(readings)

    if 'DMP' in dataString: dmpReady = True

    line = line+1

print("Data collection complete!")
print("Writing to file..")

# create the CSV
with open(filename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(sensor_data)

print("Writing to file complete!")
