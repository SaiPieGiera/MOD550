import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        sum_of_data = np.concatenate((dataset_1, dataset_2), axis=0)
        return sum_of_data, dataset_1, dataset_2

    def save(self, filename="dataset.csv", plot_filename="plots.png", metadata_filename="metadata.json"):
        # Save data in MOD550/data/
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        os.makedirs(folder, exist_ok=True)

        # Generate data
        data, dataset_1, dataset_2 = self.add_datasets()

        # Save dataset as CSV
        df = pd.DataFrame(data, columns=['X', 'Y'])
        df.to_csv(os.path.join(folder, filename), index=False, encoding="utf-8")

        # Save metadata
        metadata = {
            "MOD550 ASSIGNMENT": "Dataset Generation",
            "Student": {
                "Name": "Urszula Starowicz",
                "Email": "283591@uis.no",
                "Github": "SaiPieGiera"
            },
            "Title": "Random Dataset Generation and Analysis",
            "Description": "This dataset consists of two randomly generated datasets that are combined together.",
            "Parameters": {
                "num_points": self.num_points,
                "noise_level": self.noise
            },
            "Dataset Details": {
                "Total Points": data.shape[0],
                "Dataset 1 Points": dataset_1.shape[0],
                "Dataset 2 Points": dataset_2.shape[0],
                "Mean of combined dataset": data.mean(axis=0).tolist(),
                "Standard deviation of combined dataset": data.std(axis=0).tolist()
            }
        }

        with open(os.path.join(folder, metadata_filename), 'w', encoding="utf-8") as f:
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

        # Save the plot
        plt.tight_layout()
        plt.savefig(os.path.join(folder, plot_filename))
        plt.close()

# Example usage
dataset_generator = DatasetGenerator(num_points=200)
dataset_generator.save()

# --- SECOND PART: READ FROM DEA FOLDER ---
# Define file paths for reading (only from MOD550/data/dea/)
DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dea"))
dataset_path = os.path.join(DATA_FOLDER, "dataset.csv")
metadata_path = os.path.join(DATA_FOLDER, "metadata.json")

# Load the dataset
data_file = pd.read_csv(dataset_path, encoding="utf-8")

# Load the metadata
with open(metadata_path, "r", encoding="utf-8") as file_meta:
    metadata_dea_file = json.load(file_meta)

# Integrate metadata with dataset 
integrated_data = {
    "data": data_file.to_dict(orient="records"),
    "metadata": metadata_dea_file
}

# Assumption about the origin of the data
ASSUMPTION = "This dataset consists of 250 points generated by combining two distributions of random points based on sine and cosine truth functions, with random noise added to the outputs."
print("Integrated metadata file generated successfully.")
print("Assumption about the data source:", ASSUMPTION)
