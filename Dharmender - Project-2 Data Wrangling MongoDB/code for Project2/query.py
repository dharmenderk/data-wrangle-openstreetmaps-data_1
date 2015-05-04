#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run mongodb.py code to create database before run this program
@author: dharm7
"""
from pymongo import MongoClient
import pprint
from mongodb import load_data
import operator

def get_db(database):
    """This function insert data to MongoDB"""
    client = MongoClient('localhost:27017') #get client
    db = client[database] #build database
    return db

def get_query(data, db): 
    """This function measure number of all types of amenities"""
    queries = []
    stats = {}
    for index in range(len(data)): #setup all types of amenities in data
        #print data[index][u'name:ka']
        if "amenity" in data[index]:
            item = data[index]["amenity"]
            if item not in queries:
                queries.append(item)
    for query in queries: #calculate number of each type of amenity
        stats[str(query)] = db.las_vegas_map_dataset_R1.find({"amenity": query}).count() #query database after update
    sorted_stats = sorted(stats.items(), key=operator.itemgetter(1)) #sort by count
    print "Hotels: ", stats["hotel"]
    print "Malls: ", stats["mall"]
    return [sorted_stats[-i] for i in range(1, 11)] #display 10 amenities with most amount 

def get_pipeline():
    """This function build pipeline for queries"""
    #hotels as amenity
    pipeline1 = [{"$match": {"amenity": "hotel"}},
                 {"$project":{"_id": "$name", "cuisine": "$cuisine", "phone": "$phone"}}]
    
    #mall as amenity
    pipeline3 = [{"$match": {"amenity": "mall"}},
                 {"$project":{"_id": "$name", "cuisine": "$cuisine", "phone": "$phone"}}]  
      
    #top 5 contributors to the map    
    pipeline5 = [{"$match": {"created.user": {"$exists": 1}}},
                 {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}]
    
    return [pipeline1, pipeline3, pipeline5]

def output_result():
     """This function print output for queries"""
    
     db = get_db("las_vegas_map_dataset_R1")
     
     data = load_data("las-vegas_nevada.osm.json") 
     stats = get_query(data, db) #print number of each type of amenity
     print stats
     
     pipelines = get_pipeline()
     
     describ = ["Hotels as amenity: ", "Malls as amenity: ", "Top 5 contributors to the map: "] #query after database update (database:las_vegas_map_dataset_R1)
     for index in range(len(pipelines)):
         result = db.las_vegas_map_dataset_R1.aggregate(pipelines[index])
         print describ[index], len(result[u'result'])  
         pprint.pprint(result)  #print result of each pipeline
         print "\n"
    
def test():
    """This test is used for sample dataset"""
    db = get_db("sample_dataset")
    data = load_data("sample.osm.json"  )
    stats = get_query(data, db)
    pipelines = get_pipeline()
    result = db.sample.aggregate(pipelines[1])
    assert stats == {}
    assert result == {u'ok': 1.0, u'result': []}
    print "Pass tests"

    
if __name__ == "__main__":
    #test()
    output_result()