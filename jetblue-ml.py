import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import pickle

pathPickle = 'data.p'
pathCheck = '/cp'
size = .1

X, Y = pickle.load(open(pathPickle, 'rb'))

network = tflearn.input_data(shape=[None, len(X[0])], name='input')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = tflearn.fully_connected(network, 500, activation='relu')
network = dropout(network, 0.8)
network = tflearn.fully_connected(network, 500, activation='relu')
network = dropout(network, 0.8)
network = tflearn.fully_connected(network, 3, activation='softmax')
network = tflearn.regression(network, optimizer='adam', learning_rate=0.0001, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(network, checkpoint_path=pathCheck, max_checkpoints=0, tensorboard_verbose=0)
model.fit({'input': X}, {'targets': Y}, n_epoch=100, validation_set=size, shuffle=True, snapshot_epoch=True, show_metric=True, run_id='jetblue-ml')

