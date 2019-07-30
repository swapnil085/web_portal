from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost','port':9200}])

class CloudWatch():
    
    def __init__(self,index,type):
        self.index = index
        self.type = type

    def insert_document(self,body):
        try:
            res = es.index(index=self.index,doc_type=self.type,id=1,body=body)
            return res
        except:
            return False

