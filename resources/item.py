from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):

	parser = reqparse.RequestParser()

	parser.add_argument('price',
		type=float,
		required=True,
		help="This field is required"
		)
	
	parser.add_argument('store_id',
		type=float,
		required=True,
		help="This field is required"
		)

	@jwt_required()
	def get(self, name):
		
		item = ItemModel.find_by_name(name)

		if item:
			return item.json()
		return{"message": "Item not found"}, 404

	def post(self, name):

		if ItemModel.find_by_name(name):
			return {"message" : "An item with name '{}'already exists".format(name)}, 400

		data = Item.parser.parse_args()

		item = ItemModel(name, data["price"], data["store_id"])

		try:
			item.save_to_db()
		except:
			return {"message": "Error occured trying to insert item"}, 500


		return item, 201

	def delete(self, name):
		
		item = ItemModel.find_by_name(name)

		if item:
			item.delete_from_db()
		return {"message" : "Item not deleted" if ItemModel.find_by_name(name) else "Item deleted"}

	def put(self, name):
		
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item:
			item = ItemModel(name, data["price"], data["store_id"])
		else:
			item.price = data["price"]

		ite.save_to_db()

		return item.json()

class ItemList(Resource):
	def get(self):
		
		return {"items" : [item.json() for item in ItemModel.query.all()]}
		