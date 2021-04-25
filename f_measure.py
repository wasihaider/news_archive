from search_engine import SearchEngine

class FMeasure(object):
	def __init__(self, query):
		self.query = query
		self.engine = SearchEngine()

	def calculate_accuracy():
		docs = self.engine.get_results_by_query(self.query, accuracy=True)
		related = 10
		total = len(docs)
		
		