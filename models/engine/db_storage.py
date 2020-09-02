#!/usr/bin/python3
""" This module defines a class to manage DataBase for hbnb clone"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import Base


class DBStorage():
    """ This class manages DataBase of hbnb models in MySQL"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects depending
        of the class name"""

        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            for clase in classes:
                result = self.__session.query(clase).all()
                dic = {}
                for element in result:
                    key = "{}.{}".format(clase.__name__, element.id)
                    dic[key] = element
            return dic
        else:
            result = self.__session.query(cls).all()
            dic = {}
            for element in result:
                key = "{}.{}".format(cls.__name__, element.id)
                dic[key] = element
            return dic

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database(feature of SQLAlchemy)
        create the current database session(self.__session)
        from the engine(self.__engine) by using a sessionmaker """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ to reload the 'Session' """
        self.__session.remove()
