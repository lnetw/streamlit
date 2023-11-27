import pandas as pd
import numpy as np


def prepare_data(df: pd.DataFrame, scaler: object) -> pd.DataFrame:
    """
    Prepare the data for modeling by performing the following steps:
    1. Create lagged features for the 'meantemp' column with lags ranging from 1 to 2.
    2. Drop rows with missing values.
    3. Drop the 'meantemp' and 'meanpressure' columns.
    4. Transform the remaining columns using the provided scaler.
    5. Return the transformed data.
    Parameters:
    - data: A pandas DataFrame containing the data to be prepared.
    - scaler: An object implementing the transform method for scaling the data.
    Returns:
    - A pandas DataFrame containing the transformed data.
    """
    df_scaled = df.copy()
    for lag in range(1, 3):
        df_scaled['meantemp_'+str(lag)] = df_scaled['meantemp'].shift(lag)
    df_scaled = df_scaled.dropna()
    df_scaled = df_scaled.drop(['meantemp', 'meanpressure'], axis=1)
    date = pd.to_datetime(df_scaled['date'])
    df_scaled = df_scaled.drop(['date'], axis=1)
    df_scaled = scaler.transform(df_scaled)
    return df_scaled, date


def predict_temprature(data: pd.DataFrame, model: object) -> np.array:
    """
    Predict the temperature using the provided model and data.
    Parameters:
    - data: A pandas DataFrame containing the data to be used for prediction.
    - model: An object implementing the predict method for making predictions.
    Returns:
    - A numpy array representing the predicted temperature.
    """
    predict = model.predict(data)
    return predict


def construct_and_predict_new_temprature(humidity: float, wind_speed: float,
                                         meantemp_lag1: float, meantemp_lag2: float,
                                         scaler: object, model: object) -> float:
    """
    Constructs and predicts a new temperature based on the given parameters.

    Parameters:
        humidity (float): The humidity value.
        wind_speed (float): The wind speed value.
        meantemp_lag1 (float): The mean temperature at lag 1.
        meantemp_lag2 (float): The mean temperature at lag 2.
        scaler (object): The scaler object used to transform the features.
        model (object): The model object used for prediction.

    Returns:
        float: The predicted mean temperature.
    """
    scaled_features = scaler.transform(
        [[humidity, wind_speed, meantemp_lag1, meantemp_lag2]])
    mean_temp = predict_temprature(scaled_features, model)[0]
    return mean_temp
