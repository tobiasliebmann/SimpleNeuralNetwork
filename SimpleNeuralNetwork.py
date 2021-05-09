import numpy as np


class SimpleNeuralNetwork:
    _layer_counter = 0

    def __init__(self, first_layer: np.ndarray, layer_sizes: np.ndarray, weight_list: list, bias_list: list) -> None:
        """
        Tested.
        This is the constructor for a simple feed forward neural network object. The neural network consist of
        individual layers of different which are connected through the weights and biases via linear equation.
        The result of this linear equation is then put in a Sigmoid function to amp it to the interval [0, 1].
        For further reading checkout the book http://neuralnetworksanddeeplearning.com/ by Michael Nielsen.

        :param first_layer: The first layer of the neural network which corresponds to the input fed to the network.
        :param layer_sizes: A 1D numpy array, containing the size (number of neurons) of the individual layers.
        :param weight_list: List of weight matrix connecting the layers of the network via multiplication.
        :param bias_list: List of bias vectors added to neurons of each layer.
        """
        self.first_layer = self.sigmoid_function(first_layer)
        self.current_layer = self.sigmoid_function(first_layer)
        self.layer_sizes = layer_sizes
        self.weights = weight_list
        self.biases = bias_list

    @property
    def layer_sizes(self) -> np.ndarray:
        return self._layer_sizes

    @layer_sizes.setter
    def layer_sizes(self, new_layer_sizes) -> None:
        """
        Tested.
        Setter method for the layer sizes. it is tested if the new layer sizes is a numpy, has an according shape and is
        filled with positive integers. If this is not the case, an according error is raised. If no error is raised, the
        layer sizes are updated.

        :param new_layer_sizes: Numpy array containing the size (number of neurons) of each layer of the neural network.
        :return: None
        """
        # Check: The new layer sizes is a list of numpy array.
        if not isinstance(new_layer_sizes, np.ndarray):
            raise TypeError("The layer sizes have to be a numpy array.")

        # Check: The new layer size array is one-dimensional.
        if len(new_layer_sizes.shape) != 1:
            raise ValueError("The sizes of the layers has to be a one-dimensional array.")

        # Check: Check if the entries in the array are ints.
        if new_layer_sizes.dtype != int:
            raise TypeError("Size of the layers have to of type int.")

        # Check: All ints in the array are greater than zero.
        if not all(new_layer_sizes > 0):
            raise ValueError("The sizes of the layers have to be positive.")

        # Check: The layer size of the current layer corresponds to one in the new list of layer sizes.
        if len(self.current_layer) != new_layer_sizes[self._layer_counter]:
            raise ValueError("The size of the current layer has to coincide with the corresponding value in the"
                             "layer_sizes array.")

        self._layer_sizes = new_layer_sizes

        # Print a warning in colored text to the console when the layer size is changed.
        # print("\033[93m" + "Warning: Size of the layers was changed. The shape of the weights and biases might not"
        #                   "coincide with the layer sizes anymore." + "\033[0m")

    @property
    def biases(self) -> list:
        return self._biases

    @biases.setter
    def biases(self, new_biases) -> None:
        """
        Tested.
        Setter method for the biases used in the connections of the neural networks. Before a new array of biases is
        set, it is checked if it is a numpy array, has an according shape, is filled with real numbers and if the shapes
        of the biases conform with the sizes entered in the layer_sizes field.

        :param new_biases: New basis, replacing the old biases after the checks have been, which are described above.
        :return: None
        """
        # Check the type of the new biases.
        if not isinstance(new_biases, list):
            raise TypeError("All entries of the biases have to be numpy arrays.")

        # Loop through all the array in the biases.
        for n, bias_vector in enumerate(new_biases):
            # Check type of all entries in biases.
            if not isinstance(bias_vector, np.ndarray):
                raise TypeError("All entries of the bias list have to be numpy arrays.")

            # Check if all the arrays have are one-dimensional.
            if len(bias_vector.shape) != 1:
                raise ValueError("All entries of biases have to be one-dimensional.")

            # Check if all the entries in the arrays are numbers.
            if not (bias_vector.dtype == float or bias_vector.dtype == int):
                raise TypeError("The entries of the biases have to be real numbers.")

        self._biases = new_biases

    @property
    def weights(self) -> list:
        return self._weights

    @weights.setter
    def weights(self, new_weights) -> None:
        """
        Tested.
        Setter method for the weights which are used in the connection of the layers. Before a the weights are set a
        number of checks is performed. These checks include if the newly entered weights are in a numpy array, if this
        array has the right shape, if the numpy is filled with numbers and if the shapes of the individual weight
        matrices correspond to the number of neurons declared by the layer_sizes array.

        :param new_weights: New weights which are set after the checks have been performed.
        :return: None.
        """
        # Check if the assigned object is a list.
        if not isinstance(new_weights, list):
            raise TypeError("The weights have to be a list.")

        # Loop through all the entries.
        for n, weight_matrix in enumerate(new_weights):
            # Check if each entry is a numpy array.
            if not isinstance(weight_matrix, np.ndarray):
                raise TypeError("The entries of the weight list have to be numpy arrays.")

            shape = weight_matrix.shape  # Save the shape of the matrix.

            # Check of the shape of each entry
            if not (len(shape) == 2 or len(shape) == 1):
                raise ValueError("All entries of weight list have to be one- or two-dimensional.")

            # Check if the entries a re numbers
            if not (weight_matrix.dtype == float or weight_matrix.dtype == int):
                raise TypeError("The entries of the weights have to be real numbers.")

        self._weights = new_weights

    @staticmethod
    def sigmoid_function(num):
        """
        Tested.
        Sigmoid function compatible with numpy arrays.

        :param num: A number
        :return: The value of the sigmoid function using the num as input.
        """
        return 1. / (1. + np.exp(-num))

    def check_shapes(self) -> None:
        """
        Tested.
        This method checks if the shapes of the entries in weights and biases coincide with the entries in layer sizes.
        If this is not the case an according error is raised.

        :return: None
        """
        # Loop through all the entries in weights.
        for n, weight_matrix in enumerate(self.weights):

            shape = weight_matrix.shape  # Save the shape

            # Check if the dimension of the weight matrices coincide with the layer sizes.
            if len(shape) == 2:
                if shape[0] != self.layer_sizes[n + 1] or shape[1] != self.layer_sizes[n]:
                    raise ValueError(f"Shapes {shape} of the {n}-th weight matrix does not coincide with the layer"
                                     f" sizes {(self.layer_sizes[n + 1], self.layer_sizes[n])} .")
            elif len(shape) == 1:
                if shape[0] != self.layer_sizes[n]:
                    raise ValueError(f"Shapes {shape} of the {n}-th weight matrix does not coincide with the layer"
                                     f"sizes {self.layer_sizes[n]}.")

        # Loop through all the entries in biases.
        for n, bias_vector in enumerate(self.biases):

            shape = bias_vector.shape  # Save the shape.

            if shape[0] != self.layer_sizes[n + 1]:
                raise ValueError(f"Shape f{shape} of the {n}-th bias vector does not coincide with the {n + 1}-th layer"
                                 f"size {self.layer_sizes[n + 1]}.")

    def update(self) -> np.ndarray:
        """
        Tested.
        Moves from on layer to the next, updating the current layer.

        :return: The new layer, which is now the current layer.
        """
        # Update function from one layer to another.
        self.current_layer = self.sigmoid_function(np.dot(self.weights[self._layer_counter], self.current_layer) +
                                                   self.biases[self._layer_counter])
        self._layer_counter += 1
        return self.current_layer

    def run(self) -> list:
        """
        Tested.
        Runs the update() method repeatedly. How often the method is run is determined by the length of the layer_sizes
        attribute.

        :return: A list containing a one-dimensional numpy array containing the values of the corresponding layer.
        """
        self.check_shapes()  # Check the shapes

        if self._layer_counter:
            self._layer_counter = 0  # If the layer counter is not zero, set it to zero.
            self.current_layer = self.first_layer  # Set the current layer to the first layer

        # Return a list of numpy arrays corresponding to neurons in the according layer.
        return [self.current_layer] + [self.update() for _ in self.layer_sizes[:-1]]
