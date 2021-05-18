from keras.datasets import mnist
import numpy as np
import SimpleNeuralNetwork as snn
import modules.NeuralNetworksAndDeepLearning.src.network as nn

num_pixels = 784  # Number of pixels in a training images.
num_output_neurons = 10  # Number of neurons in the output layer.
layer_sizes = np.array([784, 10])  # Sizes of the layers in the neural network.

weights = [np.random.rand(num_output_neurons, num_pixels)]  # Weights used in the neural network.
biases = [np.random.rand(num_output_neurons)]  # Biases used in the neural networks.

print(weights, biases)

neural_network = snn.SimpleNeuralNetwork(layer_sizes, weights, biases)  # Define the neural network.
(train_inputs, desired_results), (test_X, test_y) = mnist.load_data()  # Load the test data


def convert_number(number: int) -> np.ndarray:
    """
    This function converts a number of the training data of the expected results to a numpy array with a one at the
    index num.

    :return: Numpy array with a 1 at the index num.
    """
    vec = np.zeros(10)
    vec[number] = 1.
    return vec


# Convert the elements of the desired results from numbers to numpy arrays.
converted_desired_results = np.array([convert_number(num) for num in desired_results])

# Declare the parameters for the neural network.
# Reshape the training input so that it is only one vector.
# train_inputs = np.ndarray([data.reshape(num_pixels) for data in train_inputs])
train_inputs = train_inputs.reshape(len(train_inputs), num_pixels)
training_data = list(zip(train_inputs, converted_desired_results))
mini_batch_size = 1000
learning_rate = 3.
epochs = 10

print("Started learning.")
neural_network.learn(training_data, mini_batch_size, epochs, learning_rate)  # Let the neural network learn.
print("Finished learning.")

print(neural_network.weights, neural_network.biases)

# Test the neural network by going through the test images and counting the number of rightly classified images.
result_counter = 0
test_X = test_X.reshape(len(test_X), num_pixels)

verification_data = list(zip(test_X, test_y))

for data, desired_result in verification_data:

    last_layer_activation = neural_network.feed_forward(data)
    # print(last_layer_activation)
    if desired_result == np.argmax(last_layer_activation):
        result_counter += 1

print(f"{result_counter} of {len(test_X)} test images were verified correctly by my net work.")

reference_neural_network = nn.Network(layer_sizes, weights, biases)
reference_neural_network.SGD(training_data, epochs, mini_batch_size, learning_rate, test_data=verification_data)
