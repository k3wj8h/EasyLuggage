from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_cors import CORS


''' Sources
https://www.freecodecamp.org/news/build-a-simple-json-api-in-python/
'''


# Create a new Flask application
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
db = SQLAlchemy(app)


# Define classes for tables
class Luggage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return '<Name %r>' % self.id


class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    luggage_id = db.Column(db.Integer, db.ForeignKey('luggage.id'))
    isOpen = db.Column(db.Integer)
    size = db.Column(db.String)
    luggage = db.relationship('Luggage', backref=db.backref('boxes', cascade='all,delete'))

    def __init__(self, luggage_id, size, isOpen=0):
        self.luggage_id = luggage_id
        self.isOpen = 0
        self.size = size

    def __repr__(self):
        return '<Name %r>' % self.id


db.create_all()


# Create data abstraction layer
class LuggageSchema(Schema):
    class Meta:
        type_ = 'luggage'
        self_view = 'luggage_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'luggage_many'

    id = fields.Integer()
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    boxes = Relationship(self_view='luggage_boxes',
                         self_view_kwargs={'id': '<id>'},
                         related_view='box_many',
                         many=True,
                         schema='BoxSchema',
                         type_='box')


class BoxSchema(Schema):
    class Meta:
        type_ = 'box'
        self_view = 'box_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'box_many'

    id = fields.Integer()
    luggage_id = fields.Integer(required=True)
    isOpen = fields.Integer(required=True)
    size = fields.Str(required=True)


# Create resource managers and endpoints
class LuggageOne(ResourceDetail):
    schema = LuggageSchema
    data_layer = {'session': db.session, 'model': Luggage}


class LuggageMany(ResourceList):
    schema = LuggageSchema
    data_layer = {'session': db.session, 'model': Luggage}
    methods = ['GET', 'POST']


class BoxOne(ResourceDetail):
    schema = BoxSchema
    data_layer = {'session': db.session, 'model': Box}


class BoxMany(ResourceList):
    schema = BoxSchema
    data_layer = {'session': db.session, 'model': Box}


class LuggageBox(ResourceRelationship):
    schema = LuggageSchema
    data_layer = {'session': db.session, 'model': Luggage}


api = Api(app)
api.route(LuggageOne, 'luggage_one', '/luggages/<int:id>')
api.route(LuggageMany, 'luggage_many', '/luggages')
api.route(BoxOne, 'box_one', '/boxes/<int:id>')
api.route(BoxMany, 'box_many', '/boxes')
api.route(LuggageBox, 'luggage_boxes', '/luggages/<int:id>/relationships/boxes')


# main loop to run app
if __name__ == '__main__':
    app.run(debug=True)
