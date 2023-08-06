.. -*- mode: rst -*-

|Version|_ |PythonVersion|_

.. _Linkedin: https://www.linkedin.com/in/abhishek-kaddipudi-0b5183253
.. _GitHub : https://github.com/Abhishekkaddipudi


.. |PythonVersion| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue
.. _PythonVersion: https://pypi.org/project/modelLab/

.. |Version| image:: https://img.shields.io/badge/Version-V0.1-blue
.. _Version: https://github.com/Abhishekkaddipudi/modelLab

.. |Unit_Test| image:: https://github.com/Abhishekkaddipudi/modelLab/actions/workflows/main.yml/badge.svg
.. _Unit_Test: https://github.com/Abhishekkaddipudi/modelLab

.. _Mail: mailto:abhishekkaddipudi123@gmail.com

**modelLab** is a comprehensive library of machine learning models
designed to facilitate regression or classification tasks on a given
dataset. It encompasses a diverse range of models and provides a
comprehensive evaluation of each model's performance, delivering a
comprehensive set of metrics in a Python dictionary.

PURPOSE OF THE PACKAGE
======================

-  The primary objective of the package is to offer a curated ensemble
   of renowned scikit-learn models, enabling users to conveniently train
   all models with a single function call.

FEATURES
========

-  Collections of Machine learning models

   -  **Classification Models**

      -  'LinearSVC'
      -  'SGDClassifier'
      -  'MLPClassifier'
      -  'Perceptron'
      -  'LogisticRegression'
      -  'LogisticRegressionCV'
      -  'SVC'
      -  'CalibratedClassifierCV'
      -  'PassiveAggressiveClassifier'
      -  'LabelPropagation'
      -  'LabelSpreading'
      -  'RandomForestClassifier'
      -  'GradientBoostingClassifier'
      -  'QuadraticDiscriminantAnalysis'
      -  'HistGradientBoostingClassifier'
      -  'RidgeClassifierCV'
      -  'RidgeClassifier'
      -  'AdaBoostClassifier'
      -  'ExtraTreesClassifier'
      -  'KNeighborsClassifier'
      -  'BaggingClassifier'
      -  'BernoulliNB'
      -  'LinearDiscriminantAnalysis'
      -  'GaussianNB'
      -  'NuSVC'
      -  'DecisionTreeClassifier'
      -  'NearestCentroid'
      -  'ExtraTreeClassifier'
      -  'DummyClassifier'

   -  **Regression Models**

      -  'SVR'
      -  'RandomForestRegressor'
      -  'ExtraTreesRegressor'
      -  'AdaBoostRegressor'
      -  'NuSVR'
      -  'GradientBoostingRegressor'
      -  'KNeighborsRegressor'
      -  'HuberRegressor'
      -  'RidgeCV'
      -  'BayesianRidge'
      -  'Ridge'
      -  'LinearRegression'
      -  'LarsCV'
      -  'MLPRegressor'
      -  'XGBRegressor'
      -  'CatBoostRegressor'
      -  'LGBMRegressor'

-  Can also be used for the custom models ### GETTING STARTED This
   package is available on PyPI, allowing for convenient installation
   through the PyPI repository.

Dependencies
============

::

   -  'scikit-learn'
   -  'xgboost'
   -  'catboost'
   -  'lightgbm'

INSTALLATION
============

If you already installed scikit-learn, the easiest way to install
modelLab is using ``pip``:

.. code:: bash

   pip install modelLab

USAGE
=====

.. code:: python

   >>> from modelLab import regressors,classifier
   >>> regressors(X, y, models=models, verbose=False, rets=True) #X,y is data
   >>> classifier(X, y, models=models, verbose=False, rets=True)

Examples
========

-  Regression Problem

.. code:: python

   >>> from modelLab import regressors
   >>> from sklearn.datasets import fetch_california_housing
   >>> X,y=fetch_california_housing(return_X_y=True)
   >>> regressors(X,y,verbose=True)
   Model: SVR
   Adjusted R^2: -0.0249
   R^2: -0.0229
   MSE: 1.3768
   RMSE: 1.1734
   MAE: 0.8698

   Model: RandomForestRegressor
   Adjusted R^2: 0.8034
   R^2: 0.8038
   MSE: 0.2641
   RMSE: 0.5139
   MAE: 0.3364

   Model: ExtraTreesRegressor
   Adjusted R^2: 0.8102
   R^2: 0.8105
   MSE: 0.2550
   RMSE: 0.5050
   MAE: 0.3333

   Model: AdaBoostRegressor
   Adjusted R^2: 0.4563
   R^2: 0.4574
   MSE: 0.7304
   RMSE: 0.8546
   MAE: 0.7296

   Model: NuSVR
   Adjusted R^2: 0.0069
   R^2: 0.0088
   MSE: 1.3342
   RMSE: 1.1551
   MAE: 0.8803

   Model: GradientBoostingRegressor
   Adjusted R^2: 0.7753
   R^2: 0.7757
   MSE: 0.3019
   RMSE: 0.5494
   MAE: 0.3789

   Model: KNeighborsRegressor
   Adjusted R^2: 0.1435
   R^2: 0.1451
   MSE: 1.1506
   RMSE: 1.0727
   MAE: 0.8183

   Model: HuberRegressor
   Adjusted R^2: 0.3702
   R^2: 0.3714
   MSE: 0.8461
   RMSE: 0.9198
   MAE: 0.5800

   Model: RidgeCV
   Adjusted R^2: 0.5868
   R^2: 0.5876
   MSE: 0.5551
   RMSE: 0.7450
   MAE: 0.5423

   Model: BayesianRidge
   Adjusted R^2: 0.5868
   R^2: 0.5876
   MSE: 0.5551
   RMSE: 0.7451
   MAE: 0.5422

   Model: Ridge
   Adjusted R^2: 0.5867
   R^2: 0.5875
   MSE: 0.5552
   RMSE: 0.7451
   MAE: 0.5422

   Model: LinearRegression
   Adjusted R^2: 0.5867
   R^2: 0.5875
   MSE: 0.5552
   RMSE: 0.7451
   MAE: 0.5422

   Model: LarsCV
   Adjusted R^2: 0.5211
   R^2: 0.5220
   MSE: 0.6433
   RMSE: 0.8021
   MAE: 0.5524

   Model: MLPRegressor
   Adjusted R^2: -3.5120
   R^2: -3.5032
   MSE: 6.0613
   RMSE: 2.4620
   MAE: 1.7951

   Model: XGBRegressor
   Adjusted R^2: 0.8269
   R^2: 0.8272
   MSE: 0.2326
   RMSE: 0.4822
   MAE: 0.3195

   Model: CatBoostRegressor
   Adjusted R^2: 0.8461
   R^2: 0.8464
   MSE: 0.2068
   RMSE: 0.4547
   MAE: 0.3005

   Model: LGBMRegressor
   Adjusted R^2: 0.8319
   R^2: 0.8322
   MSE: 0.2259
   RMSE: 0.4753
   MAE: 0.3185

-  Classification Problem

.. code:: python

   >>> from modelLab import regressors,classifier
   >>> from sklearn.datasets import load_iris
   >>> X,y=load_iris(return_X_y=True)
   >>> import warnings                           
   >>> warnings.filterwarnings('ignore')
   >>> classifier(X,y,verbose=True)              
   Model: LinearSVC
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: SGDClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9661

   Model: MLPClassifier
   Accuracy: 1.0000
   Precision: 1.0000
   Recall: 1.0000
   F1 Score: 1.0000

   Model: Perceptron
   Accuracy: 0.8667
   Precision: 0.9022
   Recall: 0.8667
   F1 Score: 0.8626

   Model: LogisticRegression
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: SVC
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: CalibratedClassifierCV
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: PassiveAggressiveClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: LabelPropagation
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: LabelSpreading
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: RandomForestClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: GradientBoostingClassifier
   Accuracy: 0.9333
   Precision: 0.9436
   Recall: 0.9333
   F1 Score: 0.9331

   Model: QuadraticDiscriminantAnalysis
   Accuracy: 1.0000
   Precision: 1.0000
   Recall: 1.0000
   F1 Score: 1.0000

   Model: HistGradientBoostingClassifier
   Accuracy: 0.9000
   Precision: 0.9214
   Recall: 0.9000
   F1 Score: 0.8989

   Model: RidgeClassifierCV
   Accuracy: 0.8667
   Precision: 0.8754
   Recall: 0.8667
   F1 Score: 0.8662

   Model: RidgeClassifier
   Accuracy: 0.8667
   Precision: 0.8754
   Recall: 0.8667
   F1 Score: 0.8662

   Model: AdaBoostClassifier
   Accuracy: 0.9333
   Precision: 0.9436
   Recall: 0.9333
   F1 Score: 0.9331

   Model: ExtraTreesClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: KNeighborsClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: BaggingClassifier
   Accuracy: 0.9333
   Precision: 0.9436
   Recall: 0.9333
   F1 Score: 0.9331

   Model: BernoulliNB
   Accuracy: 0.2333
   Precision: 0.0544
   Recall: 0.2333
   F1 Score: 0.0883

   Model: LinearDiscriminantAnalysis
   Accuracy: 1.0000
   Precision: 1.0000
   Recall: 1.0000
   F1 Score: 1.0000

   Model: GaussianNB
   Accuracy: 0.9333
   Precision: 0.9333
   Recall: 0.9333
   F1 Score: 0.9333

   Model: NuSVC
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: DecisionTreeClassifier
   Accuracy: 0.9333
   Precision: 0.9436
   Recall: 0.9333
   F1 Score: 0.9331

   Model: NearestCentroid
   Accuracy: 0.9000
   Precision: 0.9025
   Recall: 0.9000
   F1 Score: 0.9000

   Model: ExtraTreeClassifier
   Accuracy: 0.9667
   Precision: 0.9694
   Recall: 0.9667
   F1 Score: 0.9667

   Model: DummyClassifier
   Accuracy: 0.2333
   Precision: 0.0544
   Recall: 0.2333
   F1 Score: 0.0883

-  Using Custom Models

.. code:: python

   >>> from sklearn.datasets import make_regression
   >>> from sklearn.linear_model import LinearRegression
   >>> from modelLab import regressors
   >>> X, y = make_regression(n_samples=100, n_features=10, random_state=42)
   >>> models = {'Linear Regression': LinearRegression()}
   >>> regressors(X, y, models=models, verbose=False, rets=True)
   defaultdict(<class 'dict'>, {'Linear Regression': {'Adjusted R^2': 1.0, 'R^2': 1.0, 'MSE': 3.097635893749451e-26, 'RMSE': 1.7600101970583725e-13, 'MAE': 1.4992451724538115e-13}})

.. code:: python

   >>> from sklearn.datasets import make_regression, make_classification
   >>> from sklearn.linear_model import LogisticRegression
   >>> from modelLab import classifier
   >>> X, y = make_classification(n_samples=100, n_features=10, random_state=42)
   >>> models = {'Logistic Regression': LogisticRegression()}  
   >>> classifier(X, y, models=models, verbose=False, rets=True)
   defaultdict(<class 'dict'>, {'Logistic Regression': {'Accuracy': 0.95, 'Precision': 0.9545454545454545, 'Recall': 0.95, 'F1 Score': 0.949874686716792}})


Contributor and Author
======================
   [**Abhishek Kaddipudi**]

   `Mail`_ 
   
   `Linkedin`_

   `GitHub`_
