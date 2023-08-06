from sklearn.svm import LinearSVC, SVC, NuSVC
from sklearn.linear_model import SGDClassifier, Perceptron, LogisticRegression, LogisticRegressionCV, PassiveAggressiveClassifier, RidgeClassifierCV, RidgeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier, HistGradientBoostingClassifier
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier

Cmodels = {
    'LinearSVC': LinearSVC(),
    'SGDClassifier': SGDClassifier(),
    'MLPClassifier': MLPClassifier(),
    'Perceptron': Perceptron(),
    'LogisticRegression': LogisticRegression(),
    'LogisticRegressionCV': LogisticRegressionCV(),
    'SVC': SVC(),
    'CalibratedClassifierCV': CalibratedClassifierCV(),
    'PassiveAggressiveClassifier': PassiveAggressiveClassifier(),
    'LabelPropagation': LabelPropagation(),
    'LabelSpreading': LabelSpreading(),
    'RandomForestClassifier': RandomForestClassifier(),
    'GradientBoostingClassifier': GradientBoostingClassifier(),
    'QuadraticDiscriminantAnalysis': QuadraticDiscriminantAnalysis(),
    'HistGradientBoostingClassifier': HistGradientBoostingClassifier(),
    'RidgeClassifierCV': RidgeClassifierCV(),
    'RidgeClassifier': RidgeClassifier(),
    'AdaBoostClassifier': AdaBoostClassifier(),
    'ExtraTreesClassifier': ExtraTreesClassifier(),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'BaggingClassifier': BaggingClassifier(),
    'BernoulliNB': BernoulliNB(),
    'LinearDiscriminantAnalysis': LinearDiscriminantAnalysis(),
    'GaussianNB': GaussianNB(),
    'NuSVC': NuSVC(),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'NearestCentroid': NearestCentroid(),
    'ExtraTreeClassifier': ExtraTreeClassifier(),
    'DummyClassifier': DummyClassifier()
}



from .classification_metrics import *
from .classification import *