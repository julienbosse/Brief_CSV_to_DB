from flask import render_template, request, abort, redirect, url_for, Flask, Response
from app import app
from app import models
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import json

@app.route('/')
def index():

    path = '../Data/CSV_2.csv'
    
    data = models.data_preparation(path)

    table_city = models.make_table('city', data)
    table_country = models.make_table('country', data)
    table_job_title = models.make_table('job_title', data)
    table_movie_genre = models.make_table('movie_genre', data)
    table_domain_name = models.make_table('domain_name', data)
    table_person = data[['person_id','email_address','firstname','lastname','city_id','movie_genre_id','domain_name_id','country_id','job_title_id']]

    path_credentials = '../sql_credentials.json'

    # On récupère les credentials dans un json pour se connecter à la db
    with open(path_credentials) as file:
        credentials = json.load(file)
        myUser = credentials['user']
        myPassword = credentials['password']
        myHost = credentials['host']

    engine = models.connect_db(myUser,myPassword,myHost,'brief_csv')

    # Création des tables
    Base = declarative_base()

    class Person(Base):
        __tablename__ = 'person'

        # Primary key
        person_id = Column('person_id', Integer, primary_key=True)

        # Autres colonnes
        firstname = Column('firstname', String(50))
        lastname = Column('lastname', String(50))
        email_address = Column('email_address', String(50))

        # Foreign keys
        city_id = Column('city_id', Integer, ForeignKey('city.city_id'))
        city = relationship('City')

        movie_genre_id = Column('movie_genre_id', Integer, ForeignKey('movie_genre.movie_genre_id'))
        movie_genre = relationship('Movie_genre')

        domain_name_id = Column('domain_name_id', Integer, ForeignKey('domain_name.domain_name_id'))
        domain_name = relationship('Domain_name')

        country_id = Column('country_id', Integer, ForeignKey('country.country_id'))
        country = relationship('Country')

        job_title_id = Column('job_title_id', Integer, ForeignKey('job_title.job_title_id'))
        jobs_title = relationship('Job_title')
        
    class City(Base):
        __tablename__ = 'city'

        city_id = Column('city_id', Integer, primary_key=True)
        name = Column('name', String(50))
        person = relationship('Person')

    class Movie_genre(Base):
        __tablename__ = 'movie_genre'

        movie_genre_id = Column('movie_genre_id', Integer, primary_key=True)
        genre = Column('name', String(50))

    class Domain_name(Base):
        __tablename__ = 'domain_name'

        domain_name_id = Column('domain_name_id', Integer, primary_key=True)
        domain = Column('name', String(50))

    class Country(Base):
        __tablename__ = 'country'

        country_id = Column('country_id', Integer, primary_key=True)
        name = Column('name', String(50))

    class Job_title(Base):
        __tablename__ = 'job_title'

        country_id = Column('job_title_id', Integer, primary_key=True)
        name = Column('name', String(50))

    Base.metadata.create_all(bind=engine)

    # Remplissage des tables
    try:
        table_job_title.to_sql('job_title', if_exists='append', con=engine, index=False)
        table_country.to_sql('country', if_exists='append', con=engine, index=False)
        table_city.to_sql('city', if_exists='append', con=engine, index=False)
        table_domain_name.to_sql('domain_name', if_exists='append', con=engine, index=False)
        table_movie_genre.to_sql('movie_genre', if_exists='append', con=engine, index=False)
        table_person.to_sql('person', if_exists='append', con=engine, index=False)
        print(' - Données ajoutées à la DB avec succès')
    except Exception as e:
        print(e)
        print(' - Erreur, données non ajoutées à la BD')

    return render_template('index.html')

@app.route('/result_query', methods=['GET', 'POST'])
def result_query():

    query = request.form['query']

    path_credentials = '../sql_credentials.json'

    # On récupère les credentials dans un json pour se connecter à la db
    with open(path_credentials) as file:
        credentials = json.load(file)
        myUser = credentials['user']
        myPassword = credentials['password']
        myHost = credentials['host']

    engine = create_engine('mysql+pymysql://'+myUser+':'+myPassword+'@'+myHost+'/'+'brief_csv')

    if 'limit' not in query.lower():
        query += ' LIMIT 50'

    try :
        response = pd.read_sql_query(query, engine)
        response_html = response.to_html()
    except Exception as e:
        response_html = f"Une erreur est survenue lors de la requête SQL: {e} "
    
    return render_template('result_query.html',response_html=response_html)

@app.route('/result_graph', methods=['GET', 'POST'])
def result_graph():

    variable = request.form['variable']

    path_credentials = '../sql_credentials.json'

    query = f"SELECT {variable}.name FROM person JOIN {variable} ON person.{variable}_id = {variable}.{variable}_id"

    # On récupère les credentials dans un json pour se connecter à la db
    with open(path_credentials) as file:
        credentials = json.load(file)
        myUser = credentials['user']
        myPassword = credentials['password']
        myHost = credentials['host']

    engine = create_engine('mysql+pymysql://'+myUser+':'+myPassword+'@'+myHost+'/'+'brief_csv')

    try :
        response = pd.read_sql_query(query, engine)
        plt.figure(figsize=(11,12))
        plt.title(f"Diagramme à batons de : {variable}")
        ax = response.value_counts().head(15).plot(kind='barh').invert_yaxis()
        plt.yticks(rotation=45)
        plt.savefig('app/static/img/graph.png')

    except Exception as e:
        response = f"Une erreur est survenue lors de la requête SQL: {e} "

    

    return render_template('result_graph.html')




