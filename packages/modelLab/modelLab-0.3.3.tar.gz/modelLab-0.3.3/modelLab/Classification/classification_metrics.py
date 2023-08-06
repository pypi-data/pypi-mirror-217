from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics for classification.

    Args:
        y_true (array-like): The true target values.
        y_pred (array-like): The predicted target values.

    Returns:
        dict: A dictionary containing the calculated evaluation metrics.

    """
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted'),
        'Recall': recall_score(y_true, y_pred, average='weighted'),
        'F1 Score': f1_score(y_true, y_pred, average='weighted')
    }
    return metrics