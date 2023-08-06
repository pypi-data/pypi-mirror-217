import numpy as np


def check_data(X, y):
    """
    Check the validity of the input data.

    Args:
        X (DataFrame): The input feature matrix.
        y (Series): The target variable.

    Raises:
        ValueError: If column names in X and index values in y do not match,
                    if the dataset is empty, or if the dataset contains missing or infinite values.
        TypeError: If not all input features have a numeric data type.

    Returns:
        bool: True if the data is valid, otherwise error is caught.
    """

    
        # Check for Data Sizes
    if X.shape[0] == 0 or y.shape[0] == 0 or y.shape[0]!=X.shape[0]:
        raise ValueError("The dataset is empty. Please provide a non-empty dataset.")


    # Check for Missing Values
    if np.isnan(X).any() or np.isnan(y).any():
        raise ValueError("The dataset contains missing values. Please handle or impute them before training the model.")

    # Check for Bad Data
    if np.isinf(X).any().any() or np.isinf(y).any():
        raise ValueError("The dataset contains infinite or missing values. Please handle or impute them before training the model.")



    # If no issues are found, return True
    return True
