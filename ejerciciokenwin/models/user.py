#This file is for the users db structure, password hashing and user exists check
#Este archivo es para que Sqlalchemy le de estructura a la base de datos de usuarios, para hashear los
#passwords y para validar si el usuario que queres registrar existe o no.
from sqlalchemy import Column, Integer, Text, LargeBinary, ForeignKey, DateTime
from .meta import Base
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)
    image = Column(LargeBinary)
    posts = relationship('BlogPosts', backref = 'author',lazy=True)

    def __init__(self, name, password, role):
        self.name = name
        self.role = role
        self.password_hash = generate_password_hash(password)
        self.image = b'123'


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def check_user(self, name,request):
        return True if request.dbsession.query(User).filter_by(name=name).first() else False


class BlogPosts(Base):
    
    __tablename__ = 'blogposts'
    users = relationship(User)

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    date = Column(DateTime,nullable=False,default=datetime.utcnow)
    title = Column(Text,nullable=False)
    text = Column(Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f'Post id {self.id} -- Fecha: {self.date} -- Titulo: {self.title}'