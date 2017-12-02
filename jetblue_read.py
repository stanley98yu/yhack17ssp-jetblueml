import pickle

pathSpread = 'LowestFares.csv'
pathPickle = 'data.p'

def makeFeatureset(path):
	with open(path, 'r') as file:
		contents = file.readlines()
		# remove header
		del contents[0]

		featureset = []
		counter = 0
		for line in contents:
			splitline = line.split(',')
			
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
			# is domestic
			flight.append(float(splitline[9]))
			# is private
			flight.append(float(splitline[10]))
			
			# cost
			flight.append(float(splitline[5]) + float(splitline[6]))
		
			featureset.append(flight)

		# turn cities into numbers
		cities = list(set([i[0] for i in featureset] + [i[1] for i in featureset]))
		print(cities)
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

		return ff

featureset = makeFeatureset(pathSpread)
toPickle = [[i[0] for i in featureset], [i[1] for i in featureset]]

pickle.dump(toPickle, open(pathPickle, 'wb'))
