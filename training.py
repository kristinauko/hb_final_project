import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
import os
import tensorflow as tf
import itertools

#PREPROCESSING DATA, STRUCTURING

def get_prediction():
    """ Preprocess given data"""

    #open dataset
    df = pd.read_csv(r'~/src/phone.csv')

    #prich pricing data
    df = df['Close'].values

    #keras requirement: reshape data, convert original data
    df = df.reshape(-1,1)
    print(df.shape)

    #split dataset into train and test datasets
    #train 80 percent of rows
    dataset_train = np.array(df[:int(df.shape[0]*0.8)])

    #test dataset is 20 percent of rows
    #50 - that's where historical data and prediction overlap
    dataset_test = np.array(df[int(df.shape[0]*0.8)- 50:])

    #data scaling: convert dataset to values from 0 to 1
    scaler = MinMaxScaler(feature_range=(0, 1))

    #transform dataset using fit_transform
    dataset_train = scaler.fit_transform(dataset_train)

    #transform dataset using transform (does not influence teaching)
    dataset_test = scaler.transform(dataset_test)

    x_train, y_train = create_my_dataset(dataset_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test, y_test = create_my_dataset(dataset_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    #BUILDING MODEL

    #avoid keras error messages
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

    if(not os.path.exists(r'/home/vagrant/src/phone_prediction.h5')):
        model.fit(x_train, y_train, epochs=50, batch_size=32)
        model.save(r'/home/vagrant/src/phone_prediction.h5')

    predictions = model.predict(x_test) 
    #inverse transformation we did
    predictions = scaler.inverse_transform(predictions)

    python_list = get_python_list(predictions)

    return python_list

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


def get_python_list(predictions):
    """Take numpy array and return Python list"""

    merged_prediction = list(itertools.chain.from_iterable(predictions))

    python_list = []

    for item in merged_prediction:
        pyval = item.item()
        rounded_value = round(pyval, 2)
        python_list.append(rounded_value)
    return python_list
    




