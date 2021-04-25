import re
from mongo_connection import MongoConnection
from preprocessor import Preprocessor
from bson.objectid import ObjectId
from math import log10

#############################################

class IndexDatabase:
    def __init__(self):
        self.con = MongoConnection()
        self.db = self.con.connect_articles_db()

    #########################################
    
    def get_all_articles(self):
        db = self.con.connect_articles_db()
        collection = self.db['article']
        articles = collection.find({'indexed': False})

        return list(articles)

    #########################################
    
    def add(self, term, location):
        self.db['inverted_index'].update(
                {'term': term},
                {'$addToSet': {'locations': location}},
                upsert=True
            )

    #########################################

    def mark_article_indexed(self, doc_id):
        self.db['article'].update(
                {'_id': ObjectId(doc_id)},
                {'$set': {'indexed': True}}
            )

    #########################################

    def update_term_idf(self, term, idf):
        print(term, ": ", idf)
        self.db['idfs'].update(
                {'term': term},
                {'$inc': {'idf': idf}}
            )

    #########################################

    def update_term_doc_frequency(self, term):
        self.db['idfs'].update(
                {'term': term},
                {'$inc': {'doc_with_term': 1}},
                upsert=True
            )

    #########################################

    def get_all_terms(self):
        terms = self.db['idfs'].find({}, {'_id': 0})
        return list(terms)

#############################################

class InvertedIndex:

    def __init__(self):
        self.db = IndexDatabase()
        self.preprocessor = Preprocessor()
        self.num_docs = 613
        
    #########################################

    def index_terms(self, terms, doc_id):
        term_dict = {}
        term_count = len(terms)
        for term in terms:
            term_frequency = term_dict[term]['frequency'] if term in term_dict else 0
            term_dict[term] = {
                'doc_id': doc_id,
                'frequency': term_frequency + 1
            }

        # Update the inverted index
        for term, location in term_dict.items():
            location['frequency'] /= term_count
            self.db.add(term, location)
            self.db.update_term_doc_frequency(term)

    #########################################

    def index_articles(self):
        articles = self.db.get_all_articles()
        self.num_docs = float(len(articles))
        for article in articles:
            print("Indexing article: ", article['title'])
            article['content'] += article['title']
            # content = " ".join(article['content'])
            clean_terms = self.preprocessor.get_preprocessed_words(article['content'])
            doc_id = str(article['_id'])
            self.index_terms(clean_terms, doc_id)
            self.db.mark_article_indexed(doc_id)

    #########################################

    def calculate_idfs(self):
        terms = self.db.get_all_terms()
        print("calculating idfs...")
        for term in terms:
            print(term['doc_with_term'])
            idf = 1.0 + log10(self.num_docs/term['doc_with_term'])
            print(term, ": ", idf)
            self.db.update_term_idf(term['term'], idf)


#############################################

if __name__ == '__main__':
    index = InvertedIndex()
    index.index_articles()
    index.calculate_idfs()
