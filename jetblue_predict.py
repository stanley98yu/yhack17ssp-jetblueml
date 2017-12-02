import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
import datetime

pathModel = 'model.tflearn'
length = 8
flightRef = ['JFK', 'ACK', 'OAK', 'BWI', 'BTV', 'ANU', 'POS', 'LAX', 'PHX', 'PSP', 
'SEA', 'STI', 'GND', 'ALB', 'HOG', 'PLS', 'ABQ', 'SAV', 'DTW', 'SMF', 'CUR', 'CUN', 
'TPA', 'LGB', 'HPN', 'UIO', 'SRQ', 'BDL', 'GCM', 'SXM', 'BUR', 'SNU', 'IAD', 'STX', 
'DCA', 'BGI', 'PBI', 'BUF', 'SJO', 'MEX', 'PAP', 'PSE', 'MBJ', 'ORD', 'CLT', 'MSY', 
'SFO', 'PIT', 'BOG', 'SJU', 'DAB', 'AUS', 'HOU', 'MVY', 'DFW', 'BDA', 'PHL', 'BQN', 
'LAS', 'RDU', 'PWM', 'FLL', 'MCO', 'UVF', 'DEN', 'CTG', 'HAV', 'RNO', 'SJC', 'RIC', 
'LGA', 'ORH', 'CHS', 'SLC', 'KIN', 'NAS', 'ATL', 'SDQ', 'MDE', 'SYR', 'CMW', 'RSW', 
'CLE', 'SAN', 'PDX', 'LIR', 'JAX', 'STT', 'LRM', 'EWR', 'POP', 'ROC', 'AUA', 'BOS', 
'BNA', 'LIM', 'PUJ', 'SWF', 'PVD']

def init():
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
	return model

def isDomestic(origin, destination):
	intPorts = ['BQN', 'ANU', 'AUA', 'BDA', 'BGI', 'CMW', 'CUR', 'GCM', 'GND', 
	'HAV', 'HOG', 'KIN', 'LRM', 'MBJ', 'NAS', 'PSE', 'PAP', 'POS', 'PLS', 'POP', 
	'PUJ', 'STX', 'UVF', 'SXM', 'STT', 'SJU', 'SNU', 'STI', 'SDQ', 'BOG', 'CTG', 
	'LIM', 'MDE', 'UIO', 'CUN', 'LIR', 'MEX', 'SJO']
	if origin in intPorts and destination in intPorts:
		return 0
	else:
		return 1

# [origin, destination, month, day, day of week, time, domestic, private]

# BROKEN ADD DAY OF WEEK SUPPORT
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

	return cheapFlights

# predict flight from dates
def predictFlights(origin, leaveMonth, leaveDay, leaveYear, backMonth, backDay, backYear):
	listFlights = []
	cheapFlights = []
	for destination in range(99):
		for time in range(24):
			if origin != destination:
				listFlights.append([[origin, destination, leaveMonth, leaveDay, datetime.date(leaveYear, leaveMonth, leaveDay).weekday(), time, isDomestic(origin, destination), 0], 
					[destination, origin, backMonth, backDay, datetime.date(backYear, backMonth, backDay).weekday(), time, isDomestic(destination, origin), 0]])
	
	top = 0
	for flight in listFlights:
		leavePrediction = model.predict(np.array(flight[0]).reshape([1, length]))[0]
		backPrediction = model.predict(np.array(flight[1]).reshape([1, length]))[0]
		if leavePrediction[0] > top:
			cheapFlights.append(flight)
			top = leavePrediction[0]

	routes = []
	finalFlights = []
	for flight in cheapFlights:
		if [flight[0][0], flight[0][1]] not in routes:
			routes.append([flight[0][0], flight[0][1]])
			finalFlights.append(flight)

	return finalFlights[-3:]

model = init()
final = predictFlights(8, 12, 4, 2017, 12, 10, 2017)
print(final)





