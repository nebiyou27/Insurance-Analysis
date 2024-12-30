import os

# Define the folder structure
folder_structure = {
    '.github/workflows': ['ci.yml'],
    'data/raw': ['MachineLearningRating_v3.csv'],
    'data/processed': [],
    'notebooks': ['01_data_exploration.ipynb', '02_hypothesis_testing.ipynb', '03_modeling.ipynb'],
    'src': {
        'data': ['preprocessing.py'],
        'features': ['engineering.py'],
        'models': ['hypothesis_testing.py', 'training.py'],
        'visualization': ['plots.py']
    },
    'tests': ['test_preprocessing.py', 'test_hypothesis.py', 'test_models.py'],
}

# Function to create folders and files
def create_structure(base_dir, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    pass  # Creating empty files
                print(f"Created: {file_path}")

# Create the folder structure
create_structure('.', folder_structure)