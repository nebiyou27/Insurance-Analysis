import pandas as pd
import numpy as np
from typing import Tuple  # Import Tuple

class InsuranceDataProcessor:
    def __init__(self, raw_data_path: str):
        """
        Initialize the data processor with path to raw data
        
        Args:
            raw_data_path: Path to the raw CSV file
        """
        self.raw_data_path = raw_data_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """Load the raw insurance data"""
        # Add low_memory=False to handle mixed types and avoid warnings
        self.data = pd.read_csv(self.raw_data_path, low_memory=False)
        return self.data

    def clean_data(self) -> pd.DataFrame:
        """
        Clean the insurance data by:
        - Handling missing values
        - Converting data types
        - Standardizing text fields
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        df = self.data.copy()
        
        # Check the column names to ensure correct ones are used
        print("Columns in the dataset:", df.columns)

        # Convert date column
        df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'], errors='coerce')
        
        # Convert numeric columns and handle missing values
        numeric_columns = ['TotalPremium', 'TotalClaims', 'SumInsured', 
                         'CalculatedPremiumPerTerm', 'CustomValueEstimate']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())  # Use assignment instead of inplace
        
        # Handle categorical missing values
        categorical_columns = ['Province', 'Gender', 'MaritalStatus', 'VehicleType']
        for col in categorical_columns:
            df[col] = df[col].fillna('Unknown')  # Use assignment instead of inplace
            
        # Standardize text fields
        text_columns = ['Make', 'Model', 'Province', 'PostalCode']
        for col in text_columns:
            if col in df.columns:  # Check if the column exists
                df[col] = df[col].astype(str).str.strip().str.upper()

        self.data = df
        return df

    def create_features(self) -> pd.DataFrame:
        """
        Create additional features for analysis:
        - Vehicle age
        - Claims ratio
        - Premium per sum insured
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        df = self.data.copy()
        
        # Calculate vehicle age
        df['VehicleAge'] = pd.to_datetime(df['TransactionMonth']).dt.year - df['RegistrationYear']
        
        # Calculate claims ratio
        df['ClaimsRatio'] = df['TotalClaims'] / df['TotalPremium']
        df['ClaimsRatio'] = df['ClaimsRatio'].replace([np.inf, -np.inf], np.nan)
        df['ClaimsRatio'] = df['ClaimsRatio'].fillna(0)
        
        # Calculate premium per sum insured
        df['PremiumPerSumInsured'] = df['TotalPremium'] / df['SumInsured']
        df['PremiumPerSumInsured'] = df['PremiumPerSumInsured'].replace([np.inf, -np.inf], np.nan)
        df['PremiumPerSumInsured'] = df['PremiumPerSumInsured'].fillna(df['PremiumPerSumInsured'].median())
        
        self.data = df
        return df

    def split_train_test(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split the data into training and testing sets
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (train_df, test_df)
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        # Randomly split the data
        mask = np.random.rand(len(self.data)) < (1 - test_size)
        train_df = self.data[mask]
        test_df = self.data[~mask]
        
        return train_df, test_df

    def save_processed_data(self, output_path: str) -> None:
        """
        Save the processed data to a CSV file
        
        Args:
            output_path: Path where processed data should be saved
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        self.data.to_csv(output_path, index=False)

# Example usage:
if __name__ == "__main__":
    # Path to the raw data file
    raw_data_path = r'C:\Users\neba\Documents\Insurance-Analysis\data\raw\MachineLearningRating_v3.csv'

    # Path to save the processed data
    processed_data_path = r'C:\Users\neba\Documents\Insurance-Analysis\data\processed\processed_data.csv'

    # Initialize the processor
    processor = InsuranceDataProcessor(raw_data_path)

    # Load the data
    processor.load_data()

    # Clean the data
    processor.clean_data()

    # Create additional features
    processor.create_features()

    # Save the processed data to the processed folder
    processor.save_processed_data(processed_data_path)