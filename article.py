from bson.objectid import ObjectId
from mongo_connection import MongoConnection
import time

class Article():
	def __init__(self, doc_id=""):
		self.doc_id = doc_id
		self.title = None
		self.content = None
		self.date = None
		self.category = None
		self.image = None
		self.conn = MongoConnection()

	def populate_data(self):
		if not self.doc_id:
			return
		db = self.conn.connect_articles_db()
		collection = db['article']

		doc = collection.find_one({
				'_id': ObjectId(self.doc_id)
			}, {'_id': 0})
		self.title = doc['title']
		self.content = doc['content']
		self.date = doc['date']
		self.category = doc['category']
		if 'image_src' not in doc:
			self.image = None
		else:
			self.image = doc['image_src']
		# self.image = "https://i.dawn.com/primary/2020/03/5e6967966d246.jpg"

	def to_dict(self, keys=None):
		dic = {}
		dic['doc_id'] = self.doc_id
		dic['title'] = self.title
		dic['content'] = self.content
		dic['date'] = self.date
		dic['category'] = self.category.capitalize()
		dic['image_src'] = self.image
		return dict((k, dic[k]) for k in keys) if keys else dic

	def add_comment(self, username, name, comment):
		db = self.conn.connect_articles_db()
		collection = db['comments']
		collection.insert({
				'username': username,
				'comment': comment,
				'full_name': name,
				'doc_id': self.doc_id,
				'time': int(time.time())
			})
		return True

	def get_comments(self):
		db = self.conn.connect_articles_db()
		collection = db['comments']

		comments = collection.find({
				'doc_id': self.doc_id
			}, {'_id': 0})
		return list(comments)
	