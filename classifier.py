import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def data_clean(x):
    ## Were going to change Born to date time
    x['Born'] = pd.to_datetime(x.Born, yearfirst=True)
    x['dowBorn'] = x.Born.dt.dayofweek
    x["doyBorn"] = x.Born.dt.dayofyear
    x["monBorn"] = x.Born.dt.month
    x['yrBorn'] = x.Born.dt.year
    ## Drop Pr/St due to NaNs from other countries and First Name
    x.drop(['Pr/St','First Name'], axis=1, inplace=True)
    ocols = ['City', 'Cntry', 'Nat', 'Last Name', 'Position', 'Team']
    for oc in ocols:
        temp = pd.get_dummies(x[oc])
        x = x.join(temp, rsuffix=str('_'+oc))
    x['Hand'] = pd.factorize(x.Hand)[0]
    x.drop(ocols, axis=1, inplace=True)
    x.drop(['Born'],axis=1,inplace=True)
    return x


class Classifier(object):
    def __init__(self):
        self.model = joblib.load("hockey.pkl")
        self.train = pd.read_csv('train.csv', encoding='ISO-8859-1')
        self.test = pd.read_csv('test.csv', encoding="ISO-8859-1")
        
        full = self.train.merge(self.test, how='outer')
        full0 = full.drop(['Salary'],axis=1)
        full_c = data_clean(full0)
        ss = StandardScaler()
        self.train_c = ss.fit_transform(full_c)


    def predict_salary(self, player_id):
        try:
            res = np.exp(self.model.predict([self.train_c[player_id]])[0])
            return res
        except:
            print("prediction error")
            return None 
