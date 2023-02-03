import pandas as pd
import numpy as np
import random
import mysql.connector as sql
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor


def main():
    connection = sql.connect(database='CAR_DB', user='admin', password='')

    data = pd.read_sql('SELECT model, price, year, mileage from car', con=connection)
    print(data)
    number_of_distinct_models = data.model.nunique()
    distinct_model = data.model.unique()
    le = preprocessing.LabelEncoder()
    le.fit(distinct_model)

    new_data = data.copy()
    new_data['model'] = le.transform(new_data['model'])

    msk = np.random.rand(len(new_data)) < 0.8
    train = new_data[msk]
    test = new_data[~msk]

    regressor = RandomForestRegressor(min_samples_leaf=4, max_leaf_nodes=200)
    x = np.asanyarray(train[['model', 'year', 'mileage']])
    y = np.asanyarray(train[['price']])
    regressor.fit(x, y.ravel())
    x_test = np.asanyarray(test[['model', 'year', 'mileage']])
    y_test = np.asanyarray(test[['price']])
    score = regressor.score(x_test, y_test)
    print("Model score: %.2f" % score)
    model_number = random.randint(0, number_of_distinct_models)
    max_year = new_data[new_data.model == model_number].year.max()
    min_year = new_data[new_data.model == model_number].year.min()
    model_year = random.randint(min_year, max_year)
    model_mileage = random.randint(0, data.mileage.max())
    predict = regressor.predict([[model_number, model_year, model_mileage]])
    predict = ''.join(str(round(i)) for i in predict)
    model_name = ''.join(le.inverse_transform([model_number]))
    print(data[data.model == model_name])
    print(f'for {model_name} of year {model_year} with mileage '
          f'{model_mileage}, the model estimates:\n\t\t\t\t${predict}')
    return score


if __name__ == '__main__':
    main()
