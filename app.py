import sys
import os
import json
from flask import (Flask, request, abort, render_template,
                   url_for, redirect, Response, jsonify, session, flash)
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError)
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import (UserMixin, login_user, LoginManager,
                         current_user, logout_user, login_required)
from forms import login_form, register_form
from flask_bcrypt import Bcrypt
from models import setup_db, Restaurant, Item, User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class SuperUserView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_superUser

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    setup_db(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    admin = Admin(app)
    login_manager.init_app(app)

    admin.add_view(UserView(Restaurant, db.session))
    admin.add_view(UserView(Item, db.session))
    admin.add_view(SuperUserView(User, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def session_handler():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)

    @app.route('/', methods=('GET', 'POST'), strict_slashes=False)
    def index():
        return render_template('index.html', title='Home')

    @app.route('/login/', methods=('GET', 'POST'), strict_slashes=False)
    def login():
        form = login_form()

        if form.validate_on_submit():
            try:
                user = User.query.filter_by(email=form.email.data).first()
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('Invalid Username or password!', 'danger')
            except Exception as e:
                flash(e, 'danger')

        return render_template('auth.html',
                               form=form,
                               text='Login',
                               title='Login',
                               btn_action='Login'
                               )

    @app.route('/register/', methods=('GET', 'POST'), strict_slashes=False)
    def register():
        form = register_form()
        if form.validate_on_submit():
            try:
                email = form.email.data
                password = form.password.data
                username = form.username.data

                print(email)

                newuser = User(
                    username=username,
                    email=email,
                    password=bcrypt.generate_password_hash(password),
                )

                db.session.add(newuser)
                db.session.commit()

                flash(f'Account Succesfully created', 'success')

                return redirect(url_for('login'))

            except InvalidRequestError:
                db.session.rollback()
                flash(f'Something went wrong!', 'danger')
            except IntegrityError:
                db.session.rollback()
                flash(f'User already exists!.', 'warning')
            except DataError:
                db.session.rollback()
                flash(f'Invalid Entry', 'warning')
            except InterfaceError:
                db.session.rollback()
                flash(f'Error connecting to the database', 'danger')
            except DatabaseError:
                db.session.rollback()
                flash(f'Error connecting to the database', 'danger')
            except BuildError:
                db.session.rollback()
                flash(f'An error occured !', 'danger')
        return render_template('auth.html',
                               form=form,
                               text='Create account',
                               title='Register',
                               btn_action='Register account'
                               )

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/api')
    def api_test():
        return jsonify(
            {
                'Restaurants': Restaurant.get_all_restaurants(),
                'Items': Item.get_all_items()
            }
        )

    @app.route('/restaurants/<slug>')
    def get_restaurant_by_slug(slug):
        return jsonify(
            {
                'Restaurant': Restaurant.get_restaurant(slug)
            }
        )

    @app.route('/restaurants')
    def get_restaurants():
        return jsonify(
            {'Restaurants': Restaurant.get_all_restaurants()}
        )

    @app.route('/items')
    def get_items():
        return jsonify(
            {'Items': Item.get_all_items()}
        )

    @app.route('/restaurants', methods=['POST'])
    @login_required
    def add_restaurant():
        body = request.get_json()
        new_name = body.get('name', None)
        new_slug = body.get('slug', None)
        new_description = body.get('description', None)
        new_city = body.get('city', None)
        new_state = body.get('state', None)
        new_address = body.get('address', None)
        new_phone = body.get('phone', None)
        new_imageUrl = body.get('imageUrl', None)
        new_websiteUrl = body.get('websiteUrl', None)
        new_instagramUrl = body.get('instagramUrl', None)
        new_facebookUrl = body.get('facebookUrl', None)

        try:
            restaurant = Restaurant(
                name=new_name,
                slug=new_slug,
                description=new_description,
                city=new_city,
                state=new_state,
                address=new_address,
                phone=new_phone,
                imageUrl=new_imageUrl,
                websiteUrl=new_websiteUrl,
                instagramUrl=new_instagramUrl,
                facebookUrl=new_facebookUrl
            )
            restaurant.add()

            return jsonify({
                'success': True,
                'created restaurant': restaurant.to_dict()
            })

        except Exception as error:
            print(sys.exc_info)
            abort(422)

    @app.route('/restaurants/<int:id>/items', methods=['POST'])
    @login_required
    def add_items(id):
        body = request.get_json()

        new_section = body.get('section', None)
        new_name = body.get('name', None)
        new_shortDescription = body.get('shortDescription', None)
        new_price = body.get('price', None)
        new_imageUrl = body.get('imageUrl', None)
        new_categories = body.get('categories', None)

        try:
            item = Item(
                section=new_section,
                name=new_name,
                shortDescription=new_shortDescription,
                price=new_price,
                imageUrl=new_imageUrl,
                categories=new_categories,
                restaurant_id=id
            )
            item.add()

            return jsonify({
                'success': True,
                'created item': item.to_dict()
            })

        except Exception as error:
            print(sys.exc_info)
            abort(422)

    @app.route('/restaurants/<int:id>', methods=['PATCH'])
    @login_required
    def update_restaurant(id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_slug = body.get('slug')
        new_description = body.get('description')
        new_city = body.get('city')
        new_state = body.get('state', None)
        new_address = body.get('address')
        new_phone = body.get('phone')
        new_imageUrl = body.get('imageUrl')
        new_websiteUrl = body.get('websiteUrl')
        new_instagramUrl = body.get('instagramUrl')
        new_facebookUrl = body.get('facebookUrl')

        try:
            restaurant = Restaurant.query.filter(
                Restaurant.id == id).one_or_none()

            if restaurant is None:
                abort(404)
            else:
                restaurant.name = new_name,
                restaurant.slug = new_slug,
                restaurant.description = new_description,
                restaurant.city = new_city,
                restaurant.state = new_state,
                restaurant.address = new_address,
                restaurant.phone = new_phone,
                restaurant.imageUrl = new_imageUrl,
                restaurant.websiteUrl = new_websiteUrl,
                restaurant.instagramUrl = new_instagramUrl,
                restaurant.facebookUrl = new_facebookUrl
                restaurant.update()

            return jsonify({
                'success': True,
                'updated restaurant': restaurant.to_dict()
            })

        except Exception as error:
            print(sys.exc_info)
            abort(422)

    @app.route('/items/<int:id>', methods=['PATCH'])
    @login_required
    def update_item(id):
        body = request.get_json()

        new_section = body.get('section')
        new_name = body.get('name')
        new_shortDescription = body.get('shortDescription')
        new_price = body.get('price')
        new_imageUrl = body.get('imageUrl')
        new_categories = body.get('categories')

        try:
            item = Item(
                section=new_section,
                name=new_name,
                shortDescription=new_shortDescription,
                price=new_price,
                imageUrl=new_imageUrl,
                categories=new_categories
            )
            item.update()

            return jsonify({
                'success': True,
                'updated item': item.to_dict()
            }), 200

        except Exception as error:
            print(sys.exc_info)
            abort(422)

    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    @login_required
    def delete_restaurant(id):

        try:
            restaurant = Restaurant.query.filter(
                Restaurant.id == id).one_or_none()

            if restaurant is None:
                abort(404)

            else:
                restaurant.delete()

            return jsonify({
                'success': True,
                'deleted': restaurant.to_dict()
            }), 200

        except Exception as error:
            print(sys.ecx_info)
            abort(422)

    @app.route('/items/<int:id>', methods=['DELETE'])
    @login_required
    def delete_item(id):

        try:
            item = Item.query.filter(Item.id == id).one_or_none()

            if item is None:
                abort(404)

            else:
                item.delete()

            return jsonify({
                'success': True,
                'deleted': item.to_dict()
            }), 200

        except Exception as error:
            print(sys.ecx_info)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
