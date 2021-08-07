from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)

		if store:
			return store.json()

		return {"message": "Store does not Exist"}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {"message": "Store already Exists"}, 404

		store = StoreModel(name)

		try:
			store.save_to_db()
		except:
			return {"message": "Error Occured"}

	def delete(self, name):
		store = StoreModel.find_by_name(name)

		if store:
			store.delete_from_db()
			return {"message": "Store deleted"}
		else:
			return {"message": "Store does not exists"}

class StoreList(Resource):
	def get(self):
		return ["stores" : [store.json() for store in StoreModel.query.all()]]