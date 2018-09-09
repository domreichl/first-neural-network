# neural_network.py by Dom Reichl
# a simple neural network that recognizes digits drawn with paint.py

import numpy as np
import imageio, os, sys

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        ''' Initializes the neural network with three layers, weights between them, and a learning rate. '''
        
        self.input_nodes = input_nodes # layer 1
        self.hidden_nodes = hidden_nodes # layer 2
        self.output_nodes = output_nodes # layer 3
        
        # initialize weights sampled from a normal distribution
        self.weightsIH = np.random.normal(0.0, # centered around zero
                                          pow(self.input_nodes, -0.5), # SD relative to number of incoming links
                                          (self.hidden_nodes, self.input_nodes)) # here: 200x784 matrix
        self.weightsHO = np.random.normal(0.0,
                                          pow(self.hidden_nodes, -0.5),
                                          (self.output_nodes, self.hidden_nodes)) # here: 10x200 matrix

        self.learning_rate = learning_rate

    def sigmoid(self, x):
        '''
        Called by functions 'train' and 'test'.
        Calculates the logistic activation of layers 2 and 3 to get their nodes' output.
        '''
        
        verhulst = 1 / (1+np.exp(-x)) # sigmoid/logistic activation function
        return verhulst

    def train(self, image_data, target_array):
        ''' Trains the neural network on image data by calculating outputs and updating weights relative to a target array. '''
        
        # transform input and target data into two-dimensional, transposed arrays
        inputs = np.array(image_data, ndmin=2).T
        targets = np.array(target_array, ndmin=2).T
        
        # hidden nodes
        inputs_hidden = np.dot(self.weightsIH, inputs) # weighted output of layer 1
        outputs_hidden = self.sigmoid(inputs_hidden) # output of layer 2
        
        # output nodes
        inputs_final = np.dot(self.weightsHO, outputs_hidden) # weighted output of layer 2
        outputs_final = self.sigmoid(inputs_final) # output of layer 3

        # output errors
        errors_output = targets - outputs_final # error of layer 3 output
        errors_hidden = np.dot(self.weightsHO.T, errors_output) # weighted error

        # update weights between layers 2 and 3 (Hidden & Output)
        self.weightsHO += self.learning_rate * np.dot(
            (errors_output * outputs_final * (1.0 - outputs_final)),
            np.transpose(outputs_hidden))
        
        # update weights between and layers 1 and 2 (Input & Hidden)
        self.weightsIH += self.learning_rate * np.dot(
            (errors_hidden * outputs_hidden * (1.0 - outputs_hidden)),
            np.transpose(inputs))
    
    def test(self, image_data):
        ''' Test the neural network on new image data. '''
        
        inputs = np.array(image_data, ndmin=2).T # transform image data into 2d array
        
        # hidden nodes
        inputs_hidden = np.dot(self.weightsIH, inputs) # weighted outputs of layer 1
        outputs_hidden = self.sigmoid(inputs_hidden) # outputs of layer 2
        
        # output nodes
        inputs_final = np.dot(self.weightsHO, outputs_hidden) # weighted outputs of layer 2
        outputs_final = self.sigmoid(inputs_final) # outputs of layer 3
        
        return outputs_final

# build neural network
nodes_input = 784 # images have 28x28 pixels
nodes_hidden = 200 # experimentally chosen; keep between number of input and output nodes for good feature detection
nodes_output = 10 # for digits 0-9
learning_rate = 0.08 # experimentally chosen
nn = NeuralNetwork(nodes_input, nodes_hidden, nodes_output, learning_rate)

# load and process image data for training the network
print('Training model', end='')
with open('training_data.csv', 'r') as file:
    training_data = file.readlines() # get data from csv file
    for epoch in range(5): # less epochs work well, too
        print('.', end='') # display progress
        for record in training_data: # one record is a category index plus the data of one image
            values = record.split(',') # extract values from record
            inputs = np.asfarray(values[1:]) # turn image data values into array
            targets = np.zeros(nodes_output) + 0.01 # create default target array
            targets[int(values[0])] = 0.99 # define category index (integer < 10) as target
            nn.train(inputs, targets) # train the network
print(' done.')

# preprocessing: build list of image data arrays for testing
image_list = []
for i in range(10): # one iteration per digit
    try:
        image_path = os.path.join(os.getcwd(), 'test/{num}.png'.format(num=i))
        image = imageio.imread(image_path) # get image object
        image = 255.0 - image.flatten() # turn image object into 1d array and reverse color
        image = image / 255.0 * 0.99 + 0.01 # bring values into range 0.01-1.00
        image_list.append(image)
    except FileNotFoundError:
        print('Test images not found.\nRun paint.py first.')
        sys.exit()

# test neural network while tracking matches in a list
performance = []
for i, data in enumerate(image_list):
    outputs = nn.test(data) # get output array
    label = np.argmax(outputs) # get highest output value
    print('Network says', label,
          '({d} is true){m}'.format(d=i, m=(' -> MATCH' if label == i else '')))
    performance.append(1) if label == i else performance.append(0) # build list of matches

# calculate overall performance
performance = np.asarray(performance)
print('Model performance:', performance.sum() / performance.size)
