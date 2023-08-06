# Anomaly_Ensemble_App

![PyPI](https://img.shields.io/pypi/v/anomaly-ensemble-app?label=pypi%20package) 

## Table of contents ##
- [A statement of need](#A-statement-of-need)
  - [Overview of Anomaly_Ensemble_App](#Overview_of_Anomaly_Ensemble_App)
  - [Features](#Features)
  - [Target audience](#Target-audience)
- [Functionality](#Functionality)
  - [Module anomaly_libs](#Module-anomaly_libs)
  - [Module anomaly_data_preprocessing](#Module-anomaly_data_preprocessing)
  - [Module anomaly_models](#Module-anomaly_models)
  - [Module anomaly_detection](#Module-anomaly_detection)
  - [Module anomaly_main](#Module-anomaly_main)
- [Installation instructions](#Installation-instructions)
  - [Prerequisites](#Prerequisites)
  - [App installation](#App-installation)
- [Demo](#Demo)
  - [Data](#Data)
  - [Code](#Code)
- [Community guidelines](#Community-guidelines)
  - [Contribute to the software](#Contribute-to-the-software)
  - [Report issues or problems with the software](#Report-issues-or-problems-with-the-software)
  - [Seek support](#Seek-support)
- [Software license](#Software-license)

## A statement of need ##

### Overview of Anomaly_Ensemble_App ###
Anomaly_Ensemble_App is an anomaly detection python library that is based on the ensemble learning algorithm to derive better predictions. It combines multiple independent anomaly detection models such as Isolation Forest, DBSCAN, ThymeBoost, One-Class Support Vector Machine, Local Outlier Factor and TADGAN. Then, it returns the output according as the average prediction of the individual models is above a certain threshold. This package is specially designed for univariate time series.

**Process Flow Diagram:**

<img src="Anomaly_Ensemble_App.png" width="800" height="500">

**Performance Metrics**

A confusion matrix consists of different combinations of predicted and actual anomaly labels.
- True Positive (TP): Number of instances correctly classified as anomaly by the model. A high value indicates that the model is accurately identifying anomalies.
- True Negative (TN): Number of instances correctly classified as non anomaly by the model. A high value indicates that the model is accurately identifying non-anomalies.
- False Positive (FP): Number of instances incorrectly classified as anomaly by the model. A high value indicates that the model is producing a large number of false alarms.
- False Negative (FN): Number of instances incorrectly classified as non anomaly by the model. A high value indicates that the model is failing to detect many anomalies.

|             |              |Predicted Class  |             |
| :-------    | :-------     | :------:  | -------:    |
|             |              | *Anomaly*   | *Non Anomaly* |
| **Actual Class**  | *Anomaly*    |   True Positive    |    False Negative    |
|             | *Non Anomaly*|  False Positive   |     True Negative   |

The confusion matrix helps to calculate important metrics that is used to evaluate anomaly detection models:

- Accuracy: It measures the overall correctness of the model's predictions, calculated as (TP + TN) / (TP + TN + FP + FN).
- Precision: It quantifies the proportion of correctly predicted anomalies out of all predicted anomalies, calculated as TP / (TP + FP).
- Recall/Sensitivity: It represents the proportion of correctly predicted anomalies out of all actual anomalies, calculated as TP / (TP + FN).
- F1 score: It combines precision and recall into a single metric that is used in case of imbalanced classes (for eg, less anomalies and more non anomalies), calculated as 2 * (precision * recall) / (precision + recall).

### Features ###
1. Works well when the underlying data distribution is unknown.
2. Handles time series data.
3. Deals with trends and seasonality.
4. Provides options to choose anomaly detection models for ensemble learning.
5. Suggests hyperparameters for each anomaly detection model.
6. Provides execution time for each anomaly detection model.
7. Provides more accurate anomaly predictions. 

### Target audience ###
Anomaly_Ensemble_App should be of interest to readers who are involved in outlier detection for time series data.

## Functionality ##
The package consists of several modules and each module contains several functions.

**Package Structure:**

<img src="package_structure.png" width="500" height="400">

### Module anomaly_libs ###
This module imports all the needed python libraries that are required to run the package.

### Module anomaly_data_preprocessing ###
This module contains the data preprocessing tasks which includes detrending and deseasonalising the time series, as well as finding optimal hyperparameters for the models.

1. output = detrend(df, id\_column, time\_column, time\_format)
   - Definition: This function is used to identify trend and then, detrend a time series.
     - Identify trend: Augmented Dickey Fuller Test (ADF test) is used to capture trend of the time series.
     - Detrend: 'detrend' function is used from the 'scipy' module for detrending the time series.
   - Input Parameters: 
     - df is the dataset.
     - id\_column is the column over which the function will iterate.
     - time\_column is the datetime column.
     - time\_format is the datetime format of time\_column.
   - Output: Returns detrended time series.

2.  output = deseasonalise(df, id\_column, time\_column, time\_format)
    - Definition: This function is used to determine seasonality and then, deseasonlise a time series.
       - Determine seasonality: Autocorrelation function is used to check seasonality.
       - Deseasonalise: 'seasonal_decompose' function is used from the 'statsmodel' module for deseasonalising the time series.
    - Input Parameters: 
      - df is the dataset.
      - id\_column is the column over which the function will iterate.
      - time\_column is the datetime column.
      - time\_format is the datetime format of time\_column.
    - Output: Returns deseasonalised time series.
    
3. min\_samples = find\_min\_samples(df)
   - Definition: This function is used to find an hyperparameter for DBSCAN.
      - Find min\_samples: min\_samples is chosen as 2\*n, where n = the dimensionlity of the data.
   - Input Parameters: df is the dataset.
   - Output: Returns min\_samples.

4. eps = find\_eps(df)
   - Definition: This function is used to find an hyperparameter for DBSCAN.
     - Find eps: eps is chosen as the point of maximum curvature of the k-NN distance graph.
   - Input Parameters: df is the dataset.
   - Output: Returns eps.

5. p = find\_seasonal\_period(df)
   - Definition: This function is used to find an hyperparameter for Thymeboost.
     - Find p: seasonal\_period is chosen as the first expected seasonal period at the maximum amplitude, computed using Fast Fourier Transform.
   - Input Parameters: df is the dataset.
   - Output: Returns seasonal\_period.

6. (best\_nu, best\_kernel) = parameters_oc_svm(X, y, trials=10)
   - Definition: This function is used to hyperparameters for One Class SVM.
     - Find best\_nu & best\_kernel: Best optimal nu and kernal are found using Optuna hyperparameter optimization framework
   - Input Parameters: 
     - df is the dataset.
     - id\_column is the column over which the function will iterate.
     - time\_column is the datetime column.
     - time\_format is the datetime format of time\_column.
   - Output: Returns best\_nu and best\_kernel.

### Module anomaly_models ###
This module contains the models which are to be fitted on the data and hence used in anomaly prediction.

1. ifo\_labels = fit_iforest(X, \** kwargs)
   - Definition: This function is used to fit isolation forest model to the data and predict anomaly labels.
     - Model: Isolation forest is a decision tree based anomaly detection algorithm. 
               It isolates the outliers by randomly selecting a feature, and 
               then randomly selecting a split value between the max and min values of that feature.
               It randomly selects a feature, and then randomly selects a split value from the max and min                  values of that feature.
               It isolates the outliers based on path length of the node/data point in the tree structure.
   - Input Parameters: 
     - X is the dataset.
     - \** kwargs takes the hyperparameter for Isolation Forest from a keyword-based Python dictionary.
   - Output: Returns the anomaly labels.
   
2. dbscan\_labels = fit_dbscan(X, \** kwargs)
   - Definition: This function is used to fit dbscan model to the data and predict anomaly labels.
     - Model: DBSCAN is a density based anomaly detection algorithm. 
               It groups together the core points in clusters which are in high density regions, surrounded by border points.
               It marks the other points as outliers.
     - Prediction labels: Anomaly marked as -1 and normal as 1.
   - Input Parameters: 
     - X is the dataset.
     - \** kwargs takes the hyperparameters for DBSCAN, eps and min\_samples.
   - Output: Returns the anomaly labels.
   
 3. tb\_labels = fit_ThymeBoost(df, \** kwargs)
    - Definition: This function is used to fit thymeboost model to the data and predict anomaly labels.
      - Model: ThymeBoost is an anomaly detection algorithm which applies gradient boosting on time series                   decomposition.It is a time series model for trend/seasonality/exogeneous estimation and                       decomposition using gradient boosting. It classifies a datapoint as outlier when it does not                 lie within the range of the fitted trend.
      - Prediction labels: Anomaly marked as -1 and normal as 1.
    - Input Parameters: 
      - X is the dataset.
      - \** kwargs takes the hyperparameter for Thymeboost, seasonal\_period.
    - Output: Returns the anomaly labels.

 4. ocsvm\_labels = fit_oc_svm(df, \** kwargs)
    - Definition: This function is used to fit one-class svm model to the data and predict anomaly labels.
      - Model: One-Class Support Vector Machine (SVM) is an anomaly detection algorithm. 
               It finds a hyperplane that separates the data set from the origin such that 
               the hyperplane is as close to the datapoints as possible. It fits a non-linear 
               boundary around the dense region of the data set separating the remaining points
               as outliers.
               It minimizes the volume of the hypersphere that separates the data points from the origin in the feature space. 
               It marks the data points outside the hypersphere as outliers.
      - Prediction labels: Anomaly marked as -1 and normal as 1.
    - Input Parameters: 
      - X is the dataset.
      - \** kwargs takes the hyperparameter for One Class SVM, best\_nu and best\_kernel.
    - Output: Returns the anomaly labels.

5. lof\_labels = fit_lof(df, k):
   - Definition: This function is used to fit lof model to the data and predict anomaly labels.
     - Model: Local outlier factor (LOF) is an anomaly detection algorithm.
               It computes the local density deviation of a data point with respect to its neighbors.
               It considers the data points that fall within a substantially lower density range than its neighbors as outliers.
     - Prediction labels: Anomaly marked as -1 and normal as 1.
   - Input Parameters: 
     - X is the dataset.
     - \** kwargs takes the hyperparameter for LOF, alg.
   - Output: Returns the anomaly labels.

6. tadgan\_labels = fit_tadgan(df, k):
   - Definition: This function is used to fit tadgan model to the data and predict anomaly labels.
     - Model: 
     - Prediction labels: Anomaly marked as -1 and normal as 1.
   - Input Parameters: 
     - X is the dataset.
     - \** kwargs takes the hyperparameter for tadgan, epochs.
   - Output: Returns the anomaly labels.

### Module anomaly_detection ###
This module contains the majority vote algorithm.

1. voters = election(voters, n_voters, threshold)
   - Definition: This function is used to find the final anomaly labels of the ensemble method.
     - Model: Ensemble method is a tree based anomaly detection method. It identifies outliers based on majority voting logic. If the average predicted data point of all the models is above a certain threshold, then it is marked as an outlier.
     - Prediction labels: Anomaly marked as 1 and normal as 0.
   - Input Parameters: 
     - voters is the dataframe that contains prediction columns of all models that are fit for the run.
     - n_voters is the number of models that are fit for the run.
     - threshold is the limit above which a datapoint is considered an outlier.
   - Output: Returns the anomaly labels. 

2. (election_results, models_dict) = get_labels(X, \** kwargs)
   - Definition: This function is used to .
     - Model: 
     - Prediction labels: Anomaly marked as 1 and normal as 0.
   - Input Parameters: 
     - X is the dataset.
     - \** kwargs
   - Output: Returns the anomaly labels. 
     - election_results is the datframe with predicted labels of all models. 
     - models_dict is the Python dictionary of the models containing fit function, execution time, labels and parameters.
     
### Module anomaly_main ###
This module contains the results to be displayed.

1. find_parameters(self)
   - Definition: This function is used to provide parameters of all the models. 

2. find_anomalies(self)
   - Definition: This function is used to find the model performance. 
   
**Input parameters:**





## Installation instructions ##

### Prerequisites ###
Anomaly_Ensemble_App has been developed and tested in Python Version: v3.7 and requires some libraries.

```python3 -m pip install -r "topath\requirements.txt"```

### Application installation ###
```python3 -m pip install Anomaly_Ensemble_App```

## Demo ##

### Data ###
Use exemplary datasets 

### Code ###

```
from anomaly_ensemble_app.anomaly_main import *
import pandas as pd
original_data = "syntethic_original.csv"
original_DF = pd.read_csv(original_data, sep=";")
anomaly_detection_obj = AnomalyDetection(original_DF, 'spare_part_id', 'yyyymm', '%Y%m', models=["full"])
anomaly_detection_labels.performance_DF 
anomaly_detection_labels.final_df
```

## Community guidelines ##

### Contribute to the software ###
To contribute fixes, feature modifications or enhancements, a pull request can be created in the [Pull requests](https://github.com/devosmitachatterjee2018/Anomaly_Ensemble_App/pulls) tab of the project GitHub repository. When contributing to the software, the folowing should be included.
1. Description of the change;

2. Check that all tests pass;

3. Include new tests to report the change.

### Report issues or problems with the software ###
Any feature request or issue can be submitted to the the [Issues](https://github.com/devosmitachatterjee2018/Anomaly_Ensemble_App/issues) tab of the project GitHub repository. When reporting issues with the software, the folowing should be included.
1. Description of the problem;

2. Error message;

3. Python version and Operating System.

### Seek support ###
If any support needed, the authors can be contacted by e-mail @volvo.com. 

## Software license ##
Anomaly_Ensemble_App is released under the MIT License.

