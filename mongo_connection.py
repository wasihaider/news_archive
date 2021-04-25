from pymongo import MongoClient

#############################################

class MongoConnection:
	def __init__(self):
		self.client = MongoClient(
				host="localhost",
				port=27017,
				connect=False
			)

	#########################################

	def connect_articles_db(self):
		return self.client['articles']

	#########################################

	def connect_users_db(self):
		return self.client['users']

#############################################

# m = MongoConnection()
# db = m.connect_articles_db()
# col = db['article']
# cats = col.distinct('category')
# for cat in cats:
# 	col.update_many({'category': cat}, {'$set':{'category': cat.lower()}})