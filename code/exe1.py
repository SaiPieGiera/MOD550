import numpy as np
import json
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET

class DatasetGenerator:
    """
    A class to generate and manipulate datasets by creating random data and 
    combining multiple datasets.
    """
    def __init__(self, num_points=100, noise=16):
        self.num_points = num_points
        self.noise = noise

    def generate_random(self, num_points=None):
        if num_points is None:
            num_points = self.num_points
        return np.random.rand(num_points, 2)

    def add_datasets(self, num_points=None):
        if num_points is None:
            num_points = self.num_points
        dataset_1 = self.generate_random(num_points)
        dataset_2 = self.generate_random(num_points)
        sum_of_data = np.append(dataset_1, dataset_2, axis=0).reshape(-1, 2)
        return sum_of_data, dataset_1, dataset_2

    def save(self, folder='MOD550/data', filename='dataset.xml', plot_filename='plots.png', metadata_filename='metadata.json'):
        os.makedirs(folder, exist_ok=True)

        data, dataset_1, dataset_2 = self.add_datasets()

        # Create XML structure
        root = ET.Element("datasets")

        sum_data_elem = ET.SubElement(root, "sum_of_data")
        for point in data:
            point_elem = ET.SubElement(sum_data_elem, "point")
            ET.SubElement(point_elem, "x").text = str(point[0])
            ET.SubElement(point_elem, "y").text = str(point[1])

        dataset_1_elem = ET.SubElement(root, "dataset_1")
        for point in dataset_1:
            point_elem = ET.SubElement(dataset_1_elem, "point")
            ET.SubElement(point_elem, "x").text = str(point[0])
            ET.SubElement(point_elem, "y").text = str(point[1])

        dataset_2_elem = ET.SubElement(root, "dataset_2")
        for point in dataset_2:
            point_elem = ET.SubElement(dataset_2_elem, "point")
            ET.SubElement(point_elem, "x").text = str(point[0])
            ET.SubElement(point_elem, "y").text = str(point[1])

        # Write XML to file
        tree = ET.ElementTree(root)
        xml_path = os.path.join(folder, filename)
        tree.write(xml_path)

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
        plt.subplot(1, 3, 1)
        plt.scatter(dataset_1[:, 0], dataset_1[:, 1], label="Dataset 1", alpha=0.6)
        plt.title("Dataset 1")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 3, 2)
        plt.scatter(dataset_2[:, 0], dataset_2[:, 1], label="Dataset 2", alpha=0.6)
        plt.title("Dataset 2")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 3, 3)
        plt.scatter(data[:, 0], data[:, 1], label="Sum of Datasets", alpha=0.6)
        plt.title("Sum of Datasets")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(os.path.join(folder, plot_filename))
        plt.close()

# Example usage
dataset_generator = DatasetGenerator(num_points=200)
dataset_generator.save(folder='MOD550/data', filename='generated_data.xml',
                       plot_filename='generated_plots.png', metadata_filename='metadata.json')
