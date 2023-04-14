import pandas as pd
import os

from sklearn.model_selection import train_test_split

import env
import numpy as np


def check_file_exists(fn, query, url):
    """
    check if file exists in my local directory, if not, pull from sql db
    return dataframe
    """
    if os.path.isfile(fn):
        print('csv file found and loaded')
        return pd.read_csv(fn, index_col=0)
    else:
        print('creating df and exporting csv')
        df = pd.read_sql(query, url)
        df.to_csv(fn)
        return df

def get_titanic_data():
    url = env.get_db_url('titanic_db')
    filename = 'titanic.csv'
    query = 'select * from passengers'

    df = check_file_exists(filename, query, url)

    return df


def get_iris_data():
    url = env.get_db_url('iris_db')
    query = '''
            select * from measurements
                join species
                    using (species_id)
            '''
    filename = 'iris.csv'
    df = check_file_exists(filename, query, url)
    return df



def get_telco_churn():
    url = env.get_db_url('telco_churn')
    query = ''' select * from customers
	join contract_types
		using (contract_type_id)
	join internet_service_types
		using (internet_service_type_id)
	join payment_types
		using (payment_type_id)
        '''
    filename = 'telco.csv'
    df = check_file_exists(filename, query, url)

    return df

def prep_iris(iris):
    iris = iris.drop(columns=['species_id', 'measurement_id'])
    iris = iris.rename(columns={'species_name': 'species'})
    num=iris.select_dtypes(include="number")
    char=iris.select_dtypes(include="object")
    char = pd.get_dummies(char)
    iris_clean = pd.concat([num, char], axis=1)
    return iris_clean

def prep_telco(telco):
    telco = telco.drop(columns=['customer_id', 'payment_type_id', 'internet_service_type_id', 'contract_type_id'])
    num=telco.select_dtypes(include="number")
    char=telco.select_dtypes(include="object")
    char = pd.get_dummies(char)
    telco_clean = pd.concat([num, char], axis=1)
    return telco_clean

def prep_telco():
    telco = get_telco_churn()
    telco = telco.drop(columns=['customer_id', 'payment_type_id', 'internet_service_type_id', 'contract_type_id'])
    telco['senior_citizen'] = telco['senior_citizen'].replace({0: 'No', 1: 'Yes'})
    telco['total_charges'] = telco['total_charges'].replace({' ': 0})
    telco['total_charges'] = telco['total_charges'].astype('float')
    num=telco.select_dtypes(include="number")
    char=telco.select_dtypes(include="object")
    char = pd.get_dummies(char)
    telco_clean = pd.concat([num, char], axis=1)
    return telco_clean

def test_train(df, target):

    temp_train, test = train_test_split(df,  test_size= .2, random_state=123, stratify=df[target])
    train, validate = train_test_split(temp_train, test_size= .25, random_state=123, stratify=temp_train[target])
    return train, validate, test