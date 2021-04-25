from mongo_connection import MongoConnection

#############################################

class User():
	def __init__(self, username, password="", first_name="", last_name=""):
		self.username = username
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.full_name = first_name + " " + last_name
		self.conn = MongoConnection()
		self.db = self.conn.connect_users_db()
		self.col = self.db['users_data']

	#########################################

	def authenticate(self):
		col = self.col.find_one({
				'username': self.username,
				'password': self.password
			})
		return True if col else False

	#########################################

	def create_user(self):
		user = self.col.find_one({
				'username': self.username
			})
		if user:
			return 'Username already registred'
		self.col.insert({
				'username': self.username,
				'password': self.password,
				'full_name': self.full_name,
				'first_name': self.first_name,
				'last_name': self.last_name
			})

	#########################################

	def get_user(self):
		user = self.col.find_one({
				'username': self.username
			}, {'_id': 0, 'password': 0})
		return user

	#########################################

	def add_to_history(self, time, article_id):
		collection = self.db['user_history']
		collection.update(
				{'username': self.username, 'doc_id': article_id},
				{'$set': {'time': time}},
				upsert=True
			)

	#########################################

	def get_user_history(self):
		collection = self.db['user_history']
		history = collection.find({
			'username': self.username
			}, {'_id': 0})
		return list(history)

#############################################