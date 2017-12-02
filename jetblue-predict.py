import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np

pathModel = 'model.tflearn'
length = 7

network = tflearn.input_data(shape=[None, length], name='input')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = dropout(network, 0.8)
network = tflearn.fully_connected(network, 500, activation='relu')
network = dropout(network, 0.8)
network = tflearn.fully_connected(network, 3, activation='softmax')
network = tflearn.regression(network, optimizer='adam', learning_rate=0.0001, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(network)
model.load(pathModel)

def isDomestic(origin, destination):
	intPorts = ['BQN', 'ANU', 'AUA', 'BDA', 'BGI', 'CMW', 'CUR', 'GCM', 'GND', 
	'HAV', 'HOG', 'KIN', 'LRM', 'MBJ', 'NAS', 'PSE', 'PAP', 'POS', 'PLS', 'POP', 
	'PUJ', 'STX', 'UVF', 'SXM', 'STT', 'SJU', 'SNU', 'STI', 'SDQ', 'BOG', 'CTG', 
	'LIM', 'MDE', 'UIO', 'CUN', 'LIR', 'MEX', 'SJO']
	if origin in intPorts and destination in intPorts:
		return 0
	else:
		return 1

# [origin, destination, month, day, time, domestic, private]

# predict dates from flight
def predictDates(origin, destination):
	listFlights = []
	cheapFlights = []
	for month in range(12):
		for day in range(30):
			for time in range(24):
				listFlights.append([origin, destination, month + 1, day + 1, time, isDomestic(origin, destination), 0])
	for flight in listFlights:
		leavePrediction = model.predict(np.array(flight).reshape([1, length]))
		if leavePrediction > .6:
			cheapFlights.append(flight)

	print(cheapFlights)

# predict flight from dates
def predictFlights(origin, leaveMonth, leaveDay, backMonth, backDay):
	listFlights = []
	cheapFlights = []
	for destination in range(99):
		for time in range(24):
			if origin != destination:
				listFlights.append([[origin, destination, leaveMonth, leaveDay, time, isDomestic(origin, destination), 0], 
					[destination, origin, backMonth, backDay, time, isDomestic(destination, origin), 0]])
	for flight in listFlights:
		leavePrediction = model.predict(np.array(flight[0]).reshape([1, length]))[0]
		backPrediction = model.predict(np.array(flight[1]).reshape([1, length]))[0]
		if leavePrediction[0] > .6:
			cheapFlights.append(flight)
		if backPrediction[0] > .6:
			cheapFlights.append(flight)

	print(cheapFlights)

predictFlights(0, 12, 4, 12, 10)

