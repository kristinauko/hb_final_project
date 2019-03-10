import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras import backend as Clear
from data_helper import get_python_list

import os
import tensorflow as tf


PREDICT_SAMPLE = 50

#data scaling: convert dataset to values from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))

#PREPROCESSING DATA, STRUCTURING

def get_prediction():
    """Get prediction from the given data"""

    # convert values to pd DataFrame
    df = process_data()
    
    #check if model for the product exists and use it, otherwise create new one
    if(not os.path.exists(get_model_path("phone_prediction2"))):

        #process data
        dataset_train, dataset_test = split_reshape_dataset(df)

        #transform data
        dataset_train, dataset_test = transform_data(dataset_train, dataset_test)

        #scale data
        x_train, y_train, x_test, y_test  = reshape_datasets(dataset_train, dataset_test)

        #create model
        model = get_model(x_train)

        #fit data 
        model.fit(x_train, y_train, epochs=1, batch_size=32)

        #save model 
        model.save(get_model_path("phone_prediction2"))

        #clear the session
        Clear.clear_session()
  
    if os.path.exists(get_model_path("phone_prediction2")):

        print("STARTED THE Prediction **********************************")

        #upload model
        model = load_model(get_model_path("phone_prediction2")) 

        print("LOADED MODEL **********************************")

        df = df[len(df) - PREDICT_SAMPLE:]

        print(len(df), "***********************Length of DF")

        inputs = df.reshape(-1,1)
        print(type(inputs), len(inputs), "***********************Length of inputs")

        scaler.fit(inputs)

        # print(len(inputs), "***********************Length of inputs after fiting and transforming")
        inputs = scaler.transform(inputs)

        print(len(inputs), "***********************Length of inputs after  transforming")
        # Slide the window forward by one, so the last predicted value now becomes the head of 
        # the new window and predict the next, slide again, and so on
        for i in range(PREDICT_SAMPLE):
            x_predict = []

            x_predict.append(inputs[i:i + PREDICT_SAMPLE,0])
            x_predict = np.array(x_predict)
            x_predict = np.reshape(x_predict, (x_predict.shape[0],x_predict.shape[1],1))
            nextPrice = model.predict(x_predict)
                
            inputs = np.append(inputs, nextPrice, axis=0)
            print(i, "********************************* this is I ************************************")

        #inverse transformation we did
        predictions = scaler.inverse_transform(inputs[PREDICT_SAMPLE:])
        print(len(predictions), "******************* Length of predictions")
    
        #get predictions
        # predictions = get_prediction_array(df, model)

        #convert numpy array to python list
        python_list = get_python_list(predictions)

        #clear the session after creating or loading model
        Clear.clear_session()

    return python_list

def process_data():
    """ Preprocess given data"""

    #open dataset
    df = pd.read_csv(r'~/src/phone.csv')

    #take pricing data
    df = df['Close'].values

    return df


def split_reshape_dataset(df):
    """Take processed data, reshape it and split into two datasets"""

    #keras requirement: reshape data, convert original data
    df = df.reshape(-1,1)

    #split dataset into train and test datasets
    #train 80 percent of rows
    dataset_train = np.array(df[:int(df.shape[0]*0.8)])

    #test dataset is 20 percent of rows
    #50 - that's where historical data and prediction overlap
    dataset_test = np.array(df[int(df.shape[0]*0.8)- 50:])

    return dataset_train, dataset_test


def transform_data(dataset_train, dataset_test):
    """Scale and transform dataset_train and dataset_test"""

    #transform dataset using fit_transform
    dataset_train = scaler.fit_transform(dataset_train)

    #transform dataset using transform (does not influence teaching)
    dataset_test = scaler.transform(dataset_test)

    return dataset_train, dataset_test


def reshape_datasets(dataset_train, dataset_test):
    """Take training and testing datasets, reshape them"""

    x_train, y_train = create_my_dataset(dataset_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    x_test, y_test = create_my_dataset(dataset_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return x_train, y_train, x_test, y_test 


def get_model(x_train):
    """Build AI model"""

    tf.logging.set_verbosity(tf.logging.ERROR)

    #model type
    model = Sequential()

    #LSTM layers: add layers for the model
    #50 days, 1
    model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1],1)))

    #to avoid overfitting
    model.add(Dropout(0.2))

    #to avoid overfitting
    #input shape needs to be defind in first layer
    model.add(LSTM(units=96, return_sequences=True)) 

    #to avoid overfitting
    model.add(Dropout(0.2))

    model.add(LSTM(units=96))

    model.add(Dropout(0.2))

    #After fifty days of training what is the opening price for the first day
    model.add(Dense(units=1))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


def create_my_dataset(df):
    """Create empty lists, and put values in them"""

    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i,0])
        y.append(df[i,0])
    #convert data to numpy array
    x = np.array(x)
    y = np.array(y)
    
    return x,y


# def get_prediction_array(df, model):
#     """Take data, get 50 last values reshape ir and pass it to the model to get predicted values"""

#     df = df[len(df) - PREDICT_SAMPLE:]

#     print(len(df), "***********************Length of DF")

#     inputs = df[:PREDICT_SAMPLE].reshape(-1,1)
#     print(type(inputs), len(inputs), "***********************Length of inputs")
#     inputs = scaler.fit_transform(inputs)
#     print(len(inputs), "***********************Length of inputs after fiting and transforming")
#     inputs = scaler.transform(inputs)

#     print(len(inputs), "***********************Length of inputs after  transforming")
#     # Slide the window forward by one, so the last predicted value now becomes the head of 
#     # the new window and predict the next, slide again, and so on
#     for i in range(PREDICT_SAMPLE):
#         x_predict = []

#         x_predict.append(inputs[i:i + PREDICT_SAMPLE,0])
#         x_predict = np.array(x_predict)
#         x_predict = np.reshape(x_predict, (x_predict.shape[0],x_predict.shape[1],1))
#         nextPrice = model.predict(x_predict)
            
#         predictions_array = np.append(inputs, nextPrice, axis=0)
#         print(i, "********************************* this is I ************************************")

#     #inverse transformation we did
#     predictions = scaler.inverse_transform(predictions_array)
#     print(len(predictions), "******************* Length of predictions")

#     return predictions


def get_model_path(amazon_id):
    """Take amazon_id and create a path where model will be saved"""

    path_to_model = '/home/vagrant/src/' + str(amazon_id) + '.h5'

    return path_to_model




    




