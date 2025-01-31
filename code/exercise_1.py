"""
This module contains the DatasetGenerator class which generates random datasets
and provides functionality to add datasets together and save the results.
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import os

class DatasetGenerator:
    """
    A class to generate and manipulate datasets by creating random data and 
    combining multiple datasets.
    """
    def __init__(self, num_points=100, noise=16):
        """
        Initializes the DatasetGenerator instance with the specified number of 
        points and noise level.

        Parameters:
        num_points (int): The number of points to generate in each dataset.
        noise (int): The noise level to apply when generating the datasets.
        """
        self.num_points = num_points
        self.noise = noise

    def generate_random(self, num_points=None):
        """
        Generates a random dataset with two columns and the specified number of 
        points.

        Parameters:
        num_points (int, optional): The number of points to generate. Defaults to 
                                     self.num_points.

        Returns:
        numpy.ndarray: A 2D array containing the random data.
        """
        if num_points is None:
            num_points = self.num_points  # Default to self.num_points if no argument is passed
        rand_data = np.random.rand(num_points, 2)
        return rand_data

    def add_datasets(self, num_points=None):
        """
        Generates two random datasets and combines them by appending them together.

        Parameters:
        num_points (int, optional): The number of points to generate. Defaults to 
                                     self.num_points.

        Returns:
        numpy.ndarray: The combined dataset.
        numpy.ndarray: The first random dataset.
        numpy.ndarray: The second random dataset.
        """
        if num_points is None:
            num_points = self.num_points  # Default to self.num_points if no argument is passed
        dataset_1 = self.generate_random(num_points)
        dataset_2 = self.generate_random(num_points)
        sum_of_data = np.append(dataset_1, dataset_2, axis=0).reshape(-1, 2)
        return sum_of_data, dataset_1, dataset_2

    def save(self, folder='MOD550/data', filename='dataset.npy', plot_filename='plots.png',
             metadata_filename='metadata.json'):
        """
        Saves the generated datasets, their sum, and metadata to files. Also, 
        generates and saves plots of the datasets.

        Parameters:
        filename (str): The filename to save the datasets to.
        plot_filename (str): The filename to save the plot to.
        metadata_filename (str): The filename to save the metadata to.
        """
        # Ensure the folder exists
        os.makedirs(folder, exist_ok=True)

        # Generate data
        data, dataset_1, dataset_2 = self.add_datasets()

        # Save the data and metadata to a .npz file
        np.savez(os.path.join(folder, filename), sum_of_data=data, dataset_1=dataset_1, 
                 dataset_2=dataset_2)

        # Save metadata
        metadata = {
            "num_points": self.num_points,
            "noise": self.noise,
            "data_shape": data.shape,
            "dataset_1_shape": dataset_1.shape,
            "dataset_2_shape": dataset_2.shape
        }
        with open(os.path.join(folder, metadata_filename), 'w') as f:
            json.dump(metadata, f, indent=4)

        # Create the plot
        plt.figure(figsize=(12, 4))

        # First subplot: Dataset 1
        plt.subplot(1, 3, 1)
        plt.scatter(dataset_1[:, 0], dataset_1[:, 1], label="Dataset 1", alpha=0.6)
        plt.title("Dataset 1")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        # Second subplot: Dataset 2
        plt.subplot(1, 3, 2)
        plt.scatter(dataset_2[:, 0], dataset_2[:, 1], label="Dataset 2", alpha=0.6)
        plt.title("Dataset 2")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        # Third subplot: Sum of Datasets
        plt.subplot(1, 3, 3)
        plt.scatter(data[:, 0], data[:, 1], label="Sum of Datasets", alpha=0.6)
        plt.title("Sum of Datasets")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        # Save the plot to the specified folder
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.savefig(os.path.join(folder, plot_filename))
        plt.close()

# Example usage
dataset_generator = DatasetGenerator(num_points=200)
dataset_generator.save(folder='MOD550/data', filename='generated_data.npz',
                       plot_filename='generated_plots.png', metadata_filename='metadata.json')
