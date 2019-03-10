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

    #process data
    dataset_train, dataset_test = process_data()
    dataset_train, dataset_test = transform_data(dataset_train, dataset_test)
    x_train, y_train, x_test, y_test = get_training_testing_datasets(dataset_train, dataset_test)

    #scale data
    x_train, y_train, x_test, y_test  = scale_data(dataset_train, dataset_test)
    
    #check if model for the product exists and use it, otherwise create new one
    if(not os.path.exists(get_model_path("phone_prediction2"))):
        model = get_model(x_train)
        model.fit(x_train, y_train, epochs=1, batch_size=32)
        model.save(get_model_path("phone_prediction2"))
        
    else:
        model = load_model(get_model_path("phone_prediction2"))

    predictions = model.predict(x_test) 
    #inverse transformation we did
    predictions = scaler.inverse_transform(predictions)

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


def get_training_testing_datasets(dataset_train, dataset_test):

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
    """Create empty lists, and put dataset in them"""

    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i,0])
        y.append(df[i,0])
    #convert data to numpy array
    x = np.array(x)
    y = np.array(y)
    
    return x,y


def get_model_path(amazon_id):
    """Take amazon_id and create a path where model will be saved"""

    path_to_model = '/home/vagrant/src/' + str(amazon_id) + '.h5'

    return path_to_model




    




