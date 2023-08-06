from sklearn.svm import SVR, NuSVR
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import HuberRegressor, RidgeCV, BayesianRidge, Ridge, LinearRegression, LarsCV
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor



Rmodels = {
    'SVR': SVR(),
    'RandomForestRegressor': RandomForestRegressor(),
    'ExtraTreesRegressor': ExtraTreesRegressor(),
    'AdaBoostRegressor': AdaBoostRegressor(),
    'NuSVR': NuSVR(),
    'GradientBoostingRegressor': GradientBoostingRegressor(),
    'KNeighborsRegressor': KNeighborsRegressor(),
    'HuberRegressor': HuberRegressor(),
    'RidgeCV': RidgeCV(),
    'BayesianRidge': BayesianRidge(),
    'Ridge': Ridge(),
    'LinearRegression': LinearRegression(),
    'LarsCV': LarsCV(),
    'MLPRegressor': MLPRegressor(),
    'XGBRegressor': XGBRegressor(),
    'CatBoostRegressor': CatBoostRegressor(verbose=False),
    'LGBMRegressor': LGBMRegressor()
}

from .regression_metrics import *
from .regression import *
