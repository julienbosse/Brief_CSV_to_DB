import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database

def data_preparation(path):
    print(' - Importation des données')
    data = pd.read_csv(path)

    print(' - Préparation des données')
    data['Name'] = data['FirstName LastName'].apply(lambda x: x.split(' '))

    data['firstname'] = data['Name'].apply(lambda x: x[0])
    data['lastname'] = data['Name'].apply(lambda x: x[1])

    data['Email Address'] = data['Email Address'].apply(lambda x: x.lower()) 

    to_rename = {'ID':'person_id',
                'Job Title':'job_title',
                'Email Address':'email_address',
                'City':'city',
                'Movie Genre':'movie_genre',
                'Domain name':'domain_name',
                'Country':'country'}

    data = data.rename(columns = to_rename)
    data = data.drop(['FirstName LastName','Name'], axis=1)

    print(' - Importation et préparation terminées')
    return data

def make_table(s,data):

    table = pd.DataFrame(sorted(set(data[s])),columns=['name'])
    table[s+'_id'] = table.index+1
    table_dict = table.set_index('name',inplace=False)
    dic = table_dict.to_dict('index')
    data[s+'_id'] = data[s].apply(lambda x: dic[x][s+'_id'])
    print(f" - Table {s} créée")
    return table

def connect_db(user, password, host, bd):
    """ Crée la db MySQL si elle n'existe pas, et se connecte avec des credentials """

    s = 'mysql+pymysql://'
    s += user+':'+password+'@'+host+'/'+bd

    engine = create_engine(s)

    if not database_exists(engine.url):
        try :
            create_database(engine.url)
            print(' - DB créée avec succès')
        except Exception as e:
            print('Erreur lors de la création de la DB.')
            print(e)
        
    else:
        try :
            drop_database(engine.url)
            create_database(engine.url)
            print(' - DB créée avec succès')
        except Exception as e:
            print('Erreur lors de la création de la DB.')
            print(e)

    return engine