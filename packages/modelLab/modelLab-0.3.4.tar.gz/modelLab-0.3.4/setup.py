from setuptools import setup,find_packages
import os

REQUIREMENT_FILE_NAME="requirements.txt"
Project_Name="modelLab"
Version="0.3.4"
AUTHOR="Abhishek Kaddipudi"
DESCRIPTION="A lib for automating model training process of choosing best model that works for you data"
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.11',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


def read(fname):
    f=open(os.path.join(os.path.dirname(__file__), fname)).read()
    return f
setup(

    name=Project_Name,
    version=Version,
    author=AUTHOR,
    description=DESCRIPTION,
    url='https://github.com/Abhishekkaddipudi/modelLab',
    packages=find_packages()+find_packages(where="./modelLab/Regression")+find_packages(where="./modelLab/Classification"),
    install_requires=['scikit-learn',
                      'xgboost',
                      'catboost',
                      'lightgbm'
                      ],
    keywords=["automl","model","modelbuilder","modelLab"],
    long_description=read("README.rst"),
    author_email = "abhishekkaddipudi007@gmail.com",
    classifiers=CLASSIFIERS,

)
