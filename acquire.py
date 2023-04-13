import os

from env import host, username, password
import pandas as pd


def get_db_url(db_name):
    '''
    This function uses my info from a env.py file to create a url to access the Codeup db.
    '''
    from env import host, username, password
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'

def new_titanic_data(sql_query):
    '''
    This function reads the titanic data from the Codeup db into a df.
    '''
    sql_query = 'SELECT * FROM passengers'
    return pd.read_sql(sql_query, get_db_url('titanic_db'))


def get_titanic_data(SQL_query, directory, filename="titanic.csv"):
    """
    This function will:
    - Check local directory for csv file
        - return if exists
    - If csv doesn't exists:
        - create a df of the SQL_query
        - write df to csv
    - Output titanic df
"""
    if os.path.exists(directory + filename):
        df = pd.read_csv(filename)
        return df

    else:
        df = new_titanic_data(SQL_query)

        # want to save to csv
        df.to_csv(filename)
        return df

def new_telco_data(sql_query):
    '''
        This function reads the titanic data from the Codeup db into a df.
        '''
    sql_query = 'select c.*, ct.*, ist.*, pt.* from customers c join contract_types ct on c.contract_type_id = ct.contract_type_id join internet_service_types ist on c.internet_service_type_id = ist.internet_service_type_id join payment_types pt on c.payment_type_id = pt.payment_type_id'
    return pd.read_sql(sql_query, get_db_url('telco_churn'))

def get_telco_data(SQL_query, directory, filename="telco_churn.csv"):
    """
    This function will:
    - Check local directory for csv file
        - return if exists
    - If csv doesn't exists:
        - create a df of the SQL_query
        - write df to csv
    - Output titanic df
"""
    if os.path.exists(directory + filename):
        df = pd.read_csv(filename)
        return df

    else:
        df = new_telco_data(SQL_query)


        df.to_csv(filename)
        return df

def new_iris_data(sql_query):
    '''
    This function reads the iris data from the Codeup db into a df.
    '''
    sql_query = 'SELECT * FROM measurements JOIN species USING(species_id)'
    return pd.read_sql(sql_query, get_db_url('iris_db'))

def get_iris_data(SQL_query, directory, filename="iris.csv"):
    if os.path.exists(directory + filename):
        df = pd.read_csv(filename)
        return df

    else:
        df = new_telco_data(SQL_query)

        # want to save to csv
        df.to_csv(filename)
        return df