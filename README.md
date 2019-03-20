# CrystAl
CrystAl allows bargain hunters to explore historical Amazon product prices and evaluate future pricing predictions.

Users find the product of interest on Amazon, then simply paste the URL into CrystAl search dialog. 
![](https://github.com/kristinauko/hb_final_project/blob/master/readme_pics/homepage.png?raw=true)

The application retrieves historical Amazon quotes through a 3rd party API (Keepa.com) and uses Keras/Tensorflow machine learning backend to train an LSTM-based time series model to predict future trends, plotting both on an interactive chart. 
![](https://github.com/kristinauko/hb_final_project/blob/master/readme_pics/chart.png?raw=true)

The system re-uses datasets and ML models of frequently queried products for optimal user experience.
![](https://github.com/kristinauko/hb_final_project/blob/master/readme_pics/ChrystAl_flow.png?raw=true)

# Tech stack
* Python 
* JavaScript
* JSON
* HTML
* CSS
* jQuery
* pandas
* Keras
* NumPy

### Usage
Create virtual env, activate:
```sh
$ virtualenv env
$ source env/bin/activate
```
Install requirements:
```sh
(env) $ pip3 install -r requirements.txt
```
Source unique Keepa API key, as well. 
### Todos
 - Write Tests
 - Experiment with model hyperparameters
 - Add categories to products database
 - Experiment with models for categories

### About
Kristina's career spans journalism, communications, and software development. She holds both BS in journalism and MS in political science and previously worked as a journalist and science & technology editor. After researching and writing about technology trends for years, she decided to become a software engineer herself.

Kristina moved to the Bay Area in 2016 and was accepted to a QA internship at an IoT startup. She also completed a number of online programming courses in Python, as well as the Google/Udacity Android Nanodegree and was accepted to Hackbright in early 2019. In her final project, she focused on backend development, including applied machine learning, and is looking forward to an exciting career in software engineering.