import pandas as pd
import numpy as np
import mysql.connector as sql
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor

connection = sql.connect(database='CAR_DB', user='admin', password='')

data = pd.read_sql('SELECT model, price, year, mileage from car', con=connection)
print(data)

distinct_model = data.model.unique()
le = preprocessing.LabelEncoder()
le.fit(distinct_model)

new_data = data.copy()
new_data['model'] = le.transform(new_data['model'])

msk = np.random.rand(len(new_data)) < 0.8
train = new_data[msk]
test = new_data[~msk]

regr = RandomForestRegressor(min_samples_leaf=4, max_leaf_nodes=200)
x = np.asanyarray(train[['model', 'year', 'mileage']])
y = np.asanyarray(train[['price']])
model = regr.fit(x, y.ravel())

x_test = np.asanyarray(test[['model', 'year', 'mileage']])
y_test = np.asanyarray(test[['price']])
score = regr.score(x_test, y_test)
print("score: %.2f" % score)
