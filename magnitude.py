# importing essential libraries
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import time
import joblib

# reading the dataset for training
dataset = pd.read_csv('C:/Users/ajwad/source/repos/Earthquake_Magnitude/Earthquake_Magnitude/app/Dataset/SignificantEarthquakesDataset.csv')

print(dataset.head)

# creating the data_frame to be used for training with only essential columns
data_frame = dataset[["Date", "Time", "Latitude", "Longitude", "Type", "Depth", "Magnitude", "Source"]]


def MLClassifier(user_date, user_time, user_lat, user_long):
    training_model()
    result=prediction_model(user_date, user_time, user_lat, user_long)
    return result


# function to append the timestamp column
def create_timestamp():
    timestamp = []

    for d, t in zip(dataset['Date'], dataset['Time']):

        try:
            ts = datetime.datetime.strptime(d + ' ' + t, '%m/%d/%YT%H:%M:%S')
            timestamp.append(time.mktime(ts.timetuple()))
        except ValueError:
            timestamp.append('ValueError')

    timeStamp = pd.Series(timestamp)
    data_frame.insert(8, 'Timestamp', timeStamp, allow_duplicates=False)
    return data_frame


# function to create the training model
def training_model():
    df = pd.DataFrame(create_timestamp())

    #final_dataset = df.loc[:, ~df.columns.isin(['Date', 'Time'])]
    #print (df.head)
    #print (final_dataset.head)
    #final_dataset = final_dataset[final_dataset.Timestamp != 'ValueError']

    #df = df[df.Timestamp == '0']

    #X = df[['Timestamp', 'Latitude', 'Longitude']]
    X = df[['Latitude', 'Longitude']]
    y = df[['Magnitude', 'Depth']]
    print (X.head)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    reg = RandomForestRegressor(random_state=42)
    reg.fit(X_train, y_train)
    # save model
    joblib.dump(reg, 'RandomForestModel.joblib')


def prediction_model(input_date, input_time, input_lat, input_long):
    model = joblib.load('RandomForestModel.joblib')
    d1 = input_date
    t1 = input_time
    ts1 = datetime.datetime.strptime(d1 + ' ' + t1, '%m/%d/%Y %H:%M:%S')
    timestamp1 = time.mktime(ts1.timetuple())

    #user_inp_data = pd.DataFrame({"Timestamp": [timestamp1], "Latitude": [input_lat], "Longitude": [input_long]})
    user_inp_data = pd.DataFrame({"Latitude": [input_lat], "Longitude": [input_long]})
    predicted_value = np.char.split(np.array2string(model.predict(user_inp_data)).replace("[", "").replace("]", ""))

    return predicted_value



