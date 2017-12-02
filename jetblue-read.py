#import numpy as np
import pickle

pathSpread = 'LowestFares.csv'
pathPickle = 'data.p'
#size = .1

def makeFeatureset(path):
	with open(path, 'r') as file:
		contents = file.readlines()
		# remove header
		del contents[0]

		del contents[100:]

		featureset = []
		counter = 0
		for line in contents:
			splitline = line.split(',')
			
			# check if both cost and points cost exist
			if float(splitline[7]) > 0:
				flight = []
				# origin
				flight.append(splitline[0])
				# destination
				flight.append(splitline[1])
				time = splitline[2].split(' ')
				# month
				flight.append(float(time[0].split('/')[0]))
				# day
				flight.append(float(time[0].split('/')[1]))
				# time
				flight.append(float(time[1].split(':')[0]) + float(time[1].split(':')[1]) / 60)
				# points
				flight.append(float(splitline[7]) + float(splitline[8]))
				# is domestic
				flight.append(float(splitline[9]))
				# is private
				flight.append(float(splitline[10]))
			
				flight.append(float(splitline[5]) + float(splitline[6]))
			
				featureset.append(flight)

			# count progress
			counter += 1
			if(counter % 100 == 0):
				print(str(counter / len(contents) * 100) + ' percent complete')

		print(featureset)
		# turn cities into numbers
		cities = list(set([i[0] for i in featureset])) + list(set([i[1] for i in featureset]))
		for i in featureset:
			i[0] = cities.index(i[0])
			i[1] = cities.index(i[1])
		
		# turn costs into classification
		featureset.sort(key=lambda x: (x[0], x[1]))
		ff = []
		while len(featureset) > 0:
			sameflight = []
			index = 0
			while index < len(featureset) and featureset[0][0] == featureset[index][0] and featureset[0][1] == featureset[index][1]:
				sameflight.append(featureset[index])
				index += 1

			minprice = min([i[-1] for i in sameflight])
			avgprice = sum(i[-1] for i in sameflight) / len(sameflight)
			for i in sameflight:
				classification = []
				if i[-1] <  minprice + .2 * avgprice:
					classification = [1, 0, 0]
				elif i[-1] < avgprice:
					classification = [0, 1, 0]
				else:
					classification = [0, 0, 1]
				del i[-1]
				ff.append([i, classification])
			del featureset[:index]

		#for i in ff:
		#	print(i)
		return ff

def trainAndTest(featureset):

	X = [i[0] for i in featureset]
	Y = [i[1] for i in featureset]
	
	#featureset = np.array(featureset)
	#print(featureset)
	#X = list(featureset[:,0])
	#Y = list(featureset[:,1])

	return X, Y

#	featureset = np.array(featureset)
#	test_size = int(size * len(featureset))
#	train_x = list(featureset[:,0][:-test_size])
#	train_y = list(featureset[:,1][:-test_size])
#	test_x = list(featureset[:,0][-test_size:])
#	test_y = list(featureset[:,1][-test_size:])
#	return train_x, train_y, test_x, test_y

featureset = makeFeatureset(pathSpread)
topickle = trainAndTest(featureset)


pickle.dump(topickle, open(pathPickle, 'wb'))
