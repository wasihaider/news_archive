from flask import request, render_template, Flask
from flask_cors import  CORS, cross_origin
from article import Article
from user import User
from search_engin import SearchEngine
import json, time
import datetime, pytz, calendar

#############################################

app = Flask(__name__)
app.config['CORS_HEADERS'] = "Content-Type"
cors = CORS(app, resources={
		r"/": {"origin": "*"},
		r"/article": {"origin": "*"},
		r"/search/query": {"origin": "*"},
		r"/add/comment": {"origin": "*"},
		r"/get/comment": {"origin": "*"},
		r"/most/recent/articles": {"origin": "*"},
		r"/search/query": {"origin": "*"},
		r"/signin": {"origin": "*"},
		r"/signup": {"origin": "*"},
		r"/search/date": {"origin": "*"},
		r"/search/category": {"origin": "*"},
		r"/categories": {"origin": "*"},
	})

#############################################

@app.route('/')
def index():
	try:
		import hashlib
		REQUEST_IP = request.remote_addr
		print(request.path)
		return "<h1>HELLO THERE</h1>"
	except Exception as e:
		print("Exception in rendering template: ", str(e))

#############################################

@app.route("/article", methods=['POST'])
def get_article():
	try:
		body = request.json
		date = int(time.time())
		doc_id = body['id']
		if body['username']:
			user = User(username=body['username'])
			user.add_to_history(date, doc_id)
		doc = Article(doc_id)
		doc.populate_data()
		return json.dumps(doc.to_dict()), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in getting article: ", str(e))
		return json.dumps({"message": "Some thing went wrong"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/add/comment", methods=['POST'])
def add_comment():
	try:
		body = request.json
		print(body)
		doc_id = body['doc_id']
		doc = Article(doc_id)
		# user = User(username=body['username']).get_user()
		# if user['full_name'] != "":
		# 	name = user['full_name']
		# else:
		# 	name = user['username']

		doc.add_comment(body['username'], body['username'], body['comment'])
		return json.dumps({"message": "SUCCESS"}), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in adding comment: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/get/comment", methods=['POST'])
def get_comment():
	try:
		body = request.json
		print(body)
		doc_id = body['doc_id']
		doc = Article(doc_id)
		return json.dumps(doc.get_comments()), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in adding comment: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/most/recent/articles", methods=['POST'])
def most_recent_articles():
	try:
		s = SearchEngine()
		docs = s.get_most_recent_results()
		return json.dumps(docs), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in adding comment: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/search/query", methods=['POST'])
def search_query():
	try:
		body =  request.json
		search_query = body['query']
		category = None
		sd_epoch = None
		ed_epoch = None
		if body['category'] != "null" and body['category'] is not None:
			category = body['category']
		if body['start_date'] != "null" and body['end_date'] != "null" and body['start_date'] is not None and body['end_date'] is not None:
			start_date = body['start_date']
			end_date = body['end_date']

			tz = pytz.timezone('Asia/Karachi')
			utc = pytz.timezone('UTC')
			sd = datetime.datetime.strptime(start_date, '%Y-%m')
			tz_date = utc.localize(sd, is_dst=None)
			final_date = tz_date.astimezone(tz)
			query = tz.normalize(final_date.replace(hour=0,minute=0,second=0))
			sd_epoch = calendar.timegm(query.utctimetuple())

			tz = pytz.timezone('Asia/Karachi')
			utc = pytz.timezone('UTC')
			ed = datetime.datetime.strptime(end_date, '%Y-%m')
			tz_date = utc.localize(ed, is_dst=None)
			final_date = tz_date.astimezone(tz)
			query = tz.normalize(final_date.replace(hour=0,minute=0,second=0))
			ed_epoch = calendar.timegm(query.utctimetuple())
			
		s = SearchEngine()
		docs = s.get_results_by_query(search_query, page=int(body['page']), category=category, start_date=sd_epoch, end_date=ed_epoch)
		data = s.get_word_cloud()
		final = {
			'docs': docs,
			'wordcloud': data
		}
		return json.dumps(final), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in search by query: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/signin", methods=['POST'])
def signin():
	try:
		body =  request.json
		user = User(username=body['username'], password=body['password'])
		success = user.authenticate()
		return json.dumps({"success": success}), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in login: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/signup", methods=['POST'])
def signup():
	try:
		body =  request.json
		user = User(
				username=body['username'], 
				password=body['password'], 
				first_name=body['first_name'], 
				last_name=body['last_name']
		)
		success = user.create_user()
		return json.dumps({"success": success}), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in search by query: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/search/category", methods=['POST'])
def search_category():
	try:
		s = SearchEngine()
		body = request.json
		results = s.get_results_by_category(
			category=body['category'], 
			limit=10, 
			page=body['page']
		)
		return json.dumps(results), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in search by category: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/search/date", methods=['POST'])
def search_date():
	try:
		s = SearchEngine()
		body = request.json
		
		results = s.get_results_by_date(
			start=body['start_date'], 
			end=body['end_date'],
			limit=10, 
			page=body['page']
		)
		return json.dumps(results), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in search by date: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

@app.route("/categories", methods=['POST'])
def categories():
	try:
		body = request.json
		from mongo_connection import MongoConnection
		m = MongoConnection()
		db = m.connect_articles_db()
		col = db['article']
		data = col.distinct('category')
		categories = []
		for d in data:
			categories.append(d.capitalize())
		return json.dumps(categories), 200, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in getting categories: ", str(e))
		return json.dumps({"message": "ERROR"}), 503, {"Content-Type": "application/json"}

#############################################

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)

#############################################