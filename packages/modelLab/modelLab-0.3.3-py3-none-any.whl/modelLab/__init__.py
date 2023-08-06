from modelLab.Regression import RegressionChecker,Rmodels
from modelLab.Classification import ClassificationChecker,Cmodels
from .initial_checks import check_data




def regressors(X,y,scaled=True,n_splits=5,random_state=42,models=Rmodels,verbose=False,rets=False):
    """
    Perform regression on the given dataset using the specified models.

    Args:
        X (array-like or sparse matrix): The input data.
        y (array-like): The target labels.
        scaled (bool, optional): Whether to scale the input data. Defaults to True.
        n_splits (int, optional): Number of cross-validation splits. Defaults to 5.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.
        models (dict, optional): Dictionary containing the regression models to be checked. 
                                The keys represent model names, and the values represent the model instances. 
                                Defaults to Rmodels.
        verbose (bool, optional): Whether to print the evaluation results. Defaults to False.

    Returns:
        dict: Dictionary containing the evaluation results for each model. 
              The keys represent model names, and the values represent the corresponding metrics.
    """
    data_valid=check_data(X,y)
    regression_checker = RegressionChecker(models,scaled=scaled,n_splits=n_splits,random_state=random_state)
    if data_valid:
        regression_checker.fit_models(X, y)
        results = regression_checker.get_results()

        # Print the evaluation results
        if verbose:
            for model_name, metrics in results.items():
                print(f"Model: {model_name}")
                for metric_name, metric_value in metrics.items():
                    print(f"{metric_name}: {metric_value:.4f}")
                print()
    if rets:
        return results


def classifier(X,y,scaled=True,n_splits=5,random_state=42,models=Cmodels,verbose=False,rets=False):

    """
    Perform classification on the given dataset using the specified models.

    Args:
        X (array-like or sparse matrix): The input data.
        y (array-like): The target labels.
        scaled (bool, optional): Whether to scale the input data. Defaults to True.
        n_splits (int, optional): Number of cross-validation splits. Defaults to 5.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.
        models (dict, optional): Dictionary containing the classification models to be checked. 
                                The keys represent model names, and the values represent the model instances. 
                                Defaults to Cmodels.
        verbose (bool, optional): Whether to print the evaluation results. Defaults to False.

    Returns:
        dict: Dictionary containing the evaluation results for each model. 
              The keys represent model names, and the values represent the corresponding metrics.

    """

    data_valid=check_data(X,y)
    classfication_checker = ClassificationChecker(models,scaled=scaled,n_splits=n_splits,random_state=random_state)
    if data_valid:
        classfication_checker.fit_models(X, y)
        results = classfication_checker.get_results()

        # Print the evaluation results
        if verbose:
            for model_name, metrics in results.items():
                print(f"Model: {model_name}")
                for metric_name, metric_value in metrics.items():
                    print(f"{metric_name}: {metric_value:.4f}")
                print()
    if rets:
        return results






