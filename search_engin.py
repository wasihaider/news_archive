from preprocessor import Preprocessor
from mongo_connection import MongoConnection
from math import sqrt
from bson.objectid import ObjectId
from operator import itemgetter
from article import Article
import datetime, pytz, calendar

#############################################

class SearchEngine():
	def __init__(self):
		self.preprocessor = Preprocessor()
		self.con = MongoConnection()
		self.tfs = {}

	#########################################

	def parse_query(self, query):
		processed_query = self.preprocessor.get_preprocessed_words(query)
		return processed_query

	#########################################

	def get_tfs_and_idfs(self, word):
		database = self.con.connect_articles_db()
		tfs = database['inverted_index'].find_one({'term': word}, {'_id': 0})
		if tfs:
			idf = database['idfs'].find_one({'term': word}, {'_id': 0})
			tfs['idf'] = idf['idf']
			return tfs
		else:
			return False

	#########################################

	def calculate_tf_idf(self, query):
		tf_idfs = {}
		for word in query:
			self.tfs[word] = self.get_tfs_and_idfs(word)
			if self.tfs[word]:
				for location in self.tfs[word]['locations']:
					doc_id = location['doc_id']
					if doc_id not in tf_idfs:
						tf_idfs[doc_id] = {}
					tf_idfs[doc_id][word] = location['frequency'] * self.tfs[word]['idf']
			

		for doc_id, val in tf_idfs.items():
			words = val.keys()
			for word in query:
				if word not in words:
					tf_idfs[doc_id][word] = 0	

		return tf_idfs

	#########################################

	def calculate_query_tf_idf(self, query):
		query_length = len(query)
		word_count = {}
		for word in query:
			if word not in word_count:
				word_count[word] = 0
			word_count[word]+=1

		word_tfs = {}
		for word, count in word_count.items():
			word_tfs[word] = (count/query_length) * self.tfs[word]['idf']
		print(word_tfs)
		return word_tfs

	#########################################

	def calculate_consine_similarities(self, tf_idfs, query_tf_idf):
		cs_list = []
		for doc_id, tf_idf in tf_idfs.items():
			dot_product = 0
			query = 0   
			document = 0
			for word, value in tf_idf.items():
				dot_product += value * query_tf_idf[word]
				query += pow(query_tf_idf[word], 2)
				document += pow(value, 2)

			query = sqrt(query)
			document = sqrt(document)
			cs = {}
			cs['doc_id'] = doc_id
			cs['score'] = dot_product / (query * document)
			cs_list.append(cs)

		return cs_list

	#########################################

	def get_resulted_articles(self, cs):
		results = []
		
		for doc in cs:
			print(doc)
			art = Article(doc['doc_id'])
			art.populate_data()
			article = art.to_dict(['doc_id', 'title', 'image_src', 'category', 'date'])
			article['score'] = doc['score']
			results.append(article)

		return results

	#########################################

	def get_category_articles(self, cs, category):
		results = []
		
		for doc in cs:
			art = Article(doc['doc_id'])
			art.populate_data()
			article = art.to_dict(['category'])
			if article['category'] == category:
				results.append(doc)
			# results.append(article)

		return results

	#########################################

	def get_date_articles(self, cs, start, end):
		results = []
		
		for doc in cs:
			# print(doc)
			art = Article(doc['doc_id'])
			art.populate_data()
			article = art.to_dict(['date', 'title'])
			print(article['title'])
			if article['date'] >= start and article['date'] < end:
				results.append(doc)
			# results.append(article)

		return results

	#########################################

	def get_results_by_query(self, query, limit=10, page=1, accuracy=False, category=None, start_date=None, end_date=None):
		start = (page-1)*limit
		end = start+limit
		
		database = self.con.connect_articles_db()
		col = database['temporary']
		
		if page != 1:
			results = col.find_one({'query': query}, {'_id': 0, "results": 1})
			filtered = results['results']
			

					
		else:
			# print(type(query), " query: ", query)		
			parsed = self.parse_query(query)
			self.add_to_wordcloud(parsed)
			tf_idfs = self.calculate_tf_idf(parsed)
			
			if tf_idfs != {}:
				query_tf_idfs = self.calculate_query_tf_idf(parsed)
				cosine_similarity = self.calculate_consine_similarities(
						tf_idfs, query_tf_idfs)
				filtered = sorted(
					cosine_similarity, 
					key=itemgetter('score'),
					reverse=True
				)
				print("---->", query)
				if category != "null" and category is not None:
					print("HERE")
					filtered = self.get_category_articles(filtered, category)
				elif start_date != "null" and end_date != "null" and start_date is not None and end_date is not None:
					print("going")
					filtered = self.get_date_articles(filtered, start_date, end_date)
					print("Cumming")
				
				col.remove({"query": query})
				col.insert({"query": query, "results": filtered})
			else:
				return False
			
		
		if accuracy:
			articles = self.get_resulted_articles(filtered)
			return articles

			
		articles = self.get_resulted_articles(filtered[start:end])
		self.print_results(query, articles)
		count = len(filtered)
		total = count//10
		if count%10 > 0:
			total += 1
		return {
			'page': page,
			'total': total,
			'articles': articles
		}
		

	#########################################

	def get_results_by_category(self, category, limit=10, page=1):
		page = int(page)
		print("PAGE: ", page)
		skip = (page-1)*limit
		
		db = self.con.connect_articles_db()
		col = db['article']
		total = col.find({"category": category.lower()}).count()
		total_pages = total//limit
		if total%limit > 0:
			total_pages += 1 
		print(category.lower())
		docs = col.aggregate([
			{"$match": {"category": category.lower()}},
			{'$project': {
				'_id': {"$toString": "$_id"},
				'title': 1,
				'image_src': 1,
				'date': 1,
				'category': 1
			}},
			{'$sort': {"date": -1}},
			{"$skip": skip},
			{"$limit": limit}
		])
		return {
			'docs': list(docs),
			'total':total_pages,
			'current': page
		}
		# return list(docs)
		

	#########################################

	def get_results_by_date(self, start, end, limit=10, page=1):
		if start == "" and end=="":
			return {
			'docs': [],
			'total':0,
			'current': page
		}

		page = int(page)
		skip = (page-1)*limit

		tz = pytz.timezone('Asia/Karachi')
		utc = pytz.timezone('UTC')
		sd = datetime.datetime.strptime(start, '%Y-%m')
		tz_date = utc.localize(sd, is_dst=None)
		final_date = tz_date.astimezone(tz)
		query = tz.normalize(final_date.replace(hour=0,minute=0,second=0))
		sd_epoch = calendar.timegm(query.utctimetuple())
		print(int(sd_epoch))

		tz = pytz.timezone('Asia/Karachi')
		utc = pytz.timezone('UTC')
		ed = datetime.datetime.strptime(end, '%Y-%m')
		tz_date = utc.localize(ed, is_dst=None)
		final_date = tz_date.astimezone(tz)
		query = tz.normalize(final_date.replace(hour=0,minute=0,second=0))
		ed_epoch = calendar.timegm(query.utctimetuple())
		print(int(ed_epoch))

		db = self.con.connect_articles_db()
		col = db['article']

		total = col.find({'$and': [
				{'date': {'$gte': sd_epoch}},
				{'date': {'$lt': ed_epoch}}
			]}).count()
		total_pages = total//limit
		if total%limit > 0:
			total_pages += 1

		docs = col.aggregate([
			{"$match": {'$and': [
				{'date': {'$gte': sd_epoch}},
				{'date': {'$lt': ed_epoch}}
			]}},
			{'$project': {
				'_id': {"$toString": "$_id"},
				'title': 1,
				'image_src': 1,
				'date': 1,
				'category': 1
			}},
			{'$sort': {"date": -1}},
			{"$skip": skip},
			{"$limit": limit}
		])
		return {
			'docs': list(docs),
			'total':total_pages,
			'current': page
		}


	#########################################

	def get_most_recent_results(self, limit=10):
		db = self.con.connect_articles_db()
		col = db['article']

		cur = col.find({}, {
				"_id": 1, "title": 1, "image_src": 1
			}).sort("date", -1).limit(limit)
		docs = list(cur)
		for doc in docs:
			doc['_id'] = str(doc['_id'])
		return docs

	#########################################

	def print_results(self, query, articles):
		print("----------------------------")
		print("Results for query: ", query)
		print("----------------------------")
		print(' score \t\t\t title')
		for article in articles:
			print(article['score'], " - ", article['title'].replace("\n", ""))
		print("----------------------------")

	#########################################

	def add_to_wordcloud(self, words):
		database = self.con.connect_articles_db()
		collection = database['wordcloud']
		for word in words:
			collection.update(
				{"name": word}, 
				{"$inc": {"weight": 1}}, 
				upsert=True
			)
		return

	#########################################

	def get_word_cloud(self, limit=10):
		database = self.con.connect_articles_db()
		collection = database['wordcloud']
		data = collection.find({}, {"_id": 0})
		return list(data)

#############################################

# s = SearchEngine()
# s.get_results_by_query('cricket', page=3)

#############################################