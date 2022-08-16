import sys
from flask import (
    Flask,
    request,
    abort,
    render_template,
    Response,
    jsonify
)
from .models import setup_db, Restaurant, Item
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .config import Config


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    app.config.from_object(Config)
    db = SQLAlchemy()
    admin = Admin(app)

    admin.add_view(ModelView(Restaurant, db.session))
    admin.add_view(ModelView(Item, db.session))

    @app.route('/')
    def index():
        return 'Server is up.'

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
            "success": False,
            "error": 422,
            "message": "unprocessable"
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
    app.run()
