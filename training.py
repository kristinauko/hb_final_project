import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras import backend as Clear
from data_helper import get_python_list

import os
import tensorflow as tf

#data scaling: convert dataset to values from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))

#PREPROCESSING DATA, STRUCTURING

def get_prediction(amazon_id, df):
    """Get prediction from the given data"""

    # convert values to pd DataFrame
    df, predict_window = process_data(df)

    #check if model for the product exists and use it, otherwise create new one
    if(not os.path.exists(get_model_path(amazon_id))):

        #process data
        dataset_train, dataset_test = split_dataset(df, predict_window)

        #transform data
        dataset_train, dataset_test = transform_data(dataset_train, dataset_test)

        #scale data
        x_train, y_train, x_test, y_test  = reshape_datasets(dataset_train, dataset_test, predict_window)

        #create model
        model = get_model(x_train)

        #fit data 
        model.fit(x_train, y_train, epochs=3, batch_size=1)

        #save model 
        model.save(get_model_path(amazon_id))

        #clear the session
        Clear.clear_session()
  
    if os.path.exists(get_model_path(amazon_id)):

        #upload model
        model = load_model(get_model_path(amazon_id)) 

        #run scaler
        scaler.fit(df)

        #get inputs for prediction
        inputs = df[len(df) - predict_window:]

        #transform inputs
        inputs = scaler.transform(inputs)

        # Slide the window forward by one, so the last predicted value now becomes the head of 
        # the new window and predict the next, slide again, and so on
        for i in range(predict_window):
            x_predict = []

            x_predict.append(inputs[i:i + predict_window,0])
            x_predict = np.array(x_predict)
            x_predict = np.reshape(x_predict, (x_predict.shape[0], x_predict.shape[1],1))
            nextPrice = model.predict(x_predict)
                
            inputs = np.append(inputs, nextPrice, axis=0)

        #inverse transformation we did
        predictions = scaler.inverse_transform(inputs[predict_window:])

        #convert numpy array to python list
        python_list = get_python_list(predictions)

        #clear the session after creating or loading model
        Clear.clear_session()

    return python_list

def process_data(df):
    """ Preprocess given data"""

    predict_window = len(df) // 10 * 3

    #convert list of normalized data to pandas DataFrame
    # df = create_pd_dataframe(df)

    #take pricing data
    df = df['Price'].values

    #keras requirement: reshape data, convert original data
    df = df.reshape(-1,1)

    return df, predict_window


def split_dataset(df, predict_window):
    """Take processed data, split into two datasets - training and testing"""

    #split dataset into train and test datasets
    #train 80 percent of rows
    dataset_train = np.array(df[:int(df.shape[0]*0.8)])

    #test dataset is 20 percent of rows
    #50 - that's where historical data and prediction overlap
    dataset_test = np.array(df[int(df.shape[0]*0.8)- predict_window:])

    return dataset_train, dataset_test


def transform_data(dataset_train, dataset_test):
    """Scale and transform dataset_train and dataset_test"""

    #transform dataset using fit_transform
    dataset_train = scaler.fit_transform(dataset_train)

    #transform dataset using transform (does not influence teaching)
    dataset_test = scaler.transform(dataset_test)

    return dataset_train, dataset_test


def reshape_datasets(dataset_train, dataset_test, predict_window):
    """Take training and testing datasets, reshape them"""

    x_train, y_train = create_my_dataset(dataset_train, predict_window)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    x_test, y_test = create_my_dataset(dataset_test, predict_window)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return x_train, y_train, x_test, y_test 


def get_model(x_train):
    """Build AI model"""

    tf.logging.set_verbosity(tf.logging.ERROR)

    #model type
    model = Sequential()

    #LSTM layers: add layers for the model
    #50 days, 1
    #model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))

    model.add(LSTM(units=50))

    # #to avoid overfitting
    # model.add(Dropout(0.2))

    # #to avoid overfitting
    # #input shape needs to be defind in first layer
    # model.add(LSTM(units=96, return_sequences=True)) 

    # #to avoid overfitting
    # model.add(Dropout(0.2))

    # model.add(LSTM(units=96))

    # model.add(Dropout(0.2))

    #After fifty days of training what is the opening price for the first day
    model.add(Dense(units=1))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


def create_my_dataset(df, predict_window):
    """Create empty lists, and put values in them"""

    x = []
    y = []
    for i in range(predict_window, df.shape[0]):
        x.append(df[i-predict_window:i,0])
        y.append(df[i,0])
    #convert data to numpy array
    x = np.array(x)
    y = np.array(y)
    
    return x,y


def get_model_path(amazon_id):
    """Take amazon_id and create a path where model will be saved"""

    path_to_model = '/home/vagrant/src/' + str(amazon_id) + '.h5'

    return path_to_model




    




