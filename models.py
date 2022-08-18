import os
import json
from flask import Flask
from sqlalchemy import Column, String, Integer, LargeBinary, ARRAY, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# database_path = 'postgresql://postgres@localhost:5432/menu-db-v1'
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # db_drop_and_create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    restaurant = Restaurant(
        name='Padoca Veronese',
        slug='padoca-veronese',
        description='Paes de fermentacao natural',
        city='Floripa',
        state='Santa Catarina - Brasil',
        address='Av. do Campeche, 123',
        instagramUrl='https://www.instagram.com/cassiareginaveronezi/'
    )

    db.session.add(restaurant)
    db.session.commit()

    # item = Item(
    #     section='Paes Italianos',
    #     name='Pao italiano clássico',
    #     shortDescription='Delicioso pão italiano com casca crocante.',
    #     price='69.90',
    #     imageUrl='https://images.unsplash.com/photo-1603984042729-a34adc2ac9d0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80',
    #     categories=['sem gluten', 'vegetariano']
    # )

    # db.session.add(item)
    # db.session.commit()


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True)
    description = Column(String)
    city = Column(String)
    state = Column(String)
    address = Column(String)
    phone = Column(String)
    imageUrl = Column(String)
    websiteUrl = Column(String)
    instagramUrl = Column(String)
    facebookUrl = Column(String)
    items = db.relationship('Item', backref='restaurant', lazy=True)
    users = db.relationship('User', backref='restaurant', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'imageUrl': self.imageUrl,
            'websiteUrl': self.websiteUrl,
            'instagramUrl': self.instagramUrl,
            'facebookUrl': self.facebookUrl
        }

    def get_restaurant(_slug):
        return [Restaurant.to_dict(Restaurant.query.filter_by(slug=_slug).first())]

    def get_all_restaurants():
        return [Restaurant.to_dict(restaurant) for restaurant in Restaurant.query.all()]

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Restaurant {self.id}: {self.name}'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    is_superUser = Column(Boolean, unique=False, default=False)
    restaurant_id = Column(Integer, db.ForeignKey(
        'restaurants.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'restaurant_id': self.restaurant_id
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    section = Column(String(100))
    name = Column(String)
    shortDescription = Column(String)
    price = Column(String)
    imageUrl = Column(String)
    categories = Column(ARRAY(String))
    restaurant_id = Column(Integer, db.ForeignKey(
        'restaurants.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'section': self.section,
            'name': self.name,
            'shortDescription': self.shortDescription,
            'price': self.price,
            'imageUrl': self.imageUrl,
            'categories': self.categories
        }

    def get_all_items():
        return [Item.to_dict(item) for item in Item.query.all()]

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Item {self.id}: {self.name}'
