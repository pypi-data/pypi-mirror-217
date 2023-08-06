import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def adjusted_r2_score(y_true, y_pred, n_features):
    """
    Calculate the adjusted R-squared score.

    Args:
        y_true (array-like): The true target values.
        y_pred (array-like): The predicted target values.
        n_features (int): The number of features used in the model.

    Returns:
        float: The adjusted R-squared score.
    """
    r2 = r2_score(y_true, y_pred)
    adjusted_r2 = 1 - ((1 - r2) * (len(y_true) - 1)) / (len(y_true) - n_features - 1)
    return adjusted_r2

def calculate_metrics(y_true, y_pred, n_features):
    """
    Calculate various evaluation metrics for regression models.

    Args:
        y_true (array-like): The true target values.
        y_pred (array-like): The predicted target values.
        n_features (int): The number of features used in the model.

    Returns:
        dict: A dictionary containing the evaluation metrics.
            - 'Adjusted R^2': The adjusted R-squared score.
            - 'R^2': The R-squared score.
            - 'MSE': The mean squared error.
            - 'RMSE': The root mean squared error.
            - 'MAE': The mean absolute error.
    """
    metrics = {}
    metrics['Adjusted R^2'] = adjusted_r2_score(y_true, y_pred, n_features)
    metrics['R^2'] = r2_score(y_true, y_pred)
    metrics['MSE'] = mean_squared_error(y_true, y_pred)
    metrics['RMSE'] = np.sqrt(metrics['MSE'])
    metrics['MAE'] = mean_absolute_error(y_true, y_pred)
    return metrics
