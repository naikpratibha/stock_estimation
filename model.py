from datetime import date
import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split


def get_prediction(code, days) : 
    quandl.ApiConfig.verify_ssl = False
    company_code = 'WIKI/'+code
    df = quandl.get(company_code)
    df = df[['Adj. Close']]

    forcast_out = days
    df['Prediction'] = df[['Adj. Close']].shift(-forcast_out)
    X = np.array(df.drop(['Prediction'],1))
    X = X[:-forcast_out]
    y = np.array(df['Prediction'])
    y = y[:-forcast_out]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    svr_rbf = SVR(kernel = 'rbf', C = 1e3, gamma = 0.1)
    svr_rbf.fit(X_train, y_train)

    svr_confindence = svr_rbf.score(X_test, y_test)
   # lr = LinearRegression()
   # lr_confidence = lr.score(X_test, y_test)

    x_forcast = np.array(df.drop(['Prediction'],1))[-forcast_out:]
   # lr_prediction = lr.predict(x_forcast)
    svr_prediction = svr_rbf.predict(x_forcast)
    return {'Days': range(len(svr_prediction)), 'Stock Price': svr_prediction}
