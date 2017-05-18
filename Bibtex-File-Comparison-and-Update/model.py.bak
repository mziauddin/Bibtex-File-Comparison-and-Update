#!/usr/bin/env python
import bibtexparser
import Tkinter as tk        
from Tkinter import *
from ttk import *
import Tkinter, Tkconstants, tkFileDialog


class Model():
    """Creates and maintains the MongoDb and Bibtex databases"""
    def __init__(self,conn,master,local):
        """define  mongoDB database"""        
        self.mongo_db = conn.bibtex_files
        self.mongo_db.mongo_local.drop()
        self.mongo_db.mongo_master.drop()
        """ define collection where I'll insert my local files data"""
        mongo_local = self.mongo_db.mongo_local
        """ define collection where I'll insert my master files data"""
        mongo_master = self.mongo_db.mongo_master
        with open(local) as bibtex_file:
            bibtex_str = bibtex_file.read()
        """create bibtex database for local file"""
        self.bibdb_local = bibtexparser.loads(bibtex_str)             
        for entry_dict in self.bibdb_local.entries:
            mongo_local.insert(entry_dict)
        with open(master) as bibtex_file:
            bibtex_str = bibtex_file.read()
        """create bibtex database for master file"""
        bibdb_master = bibtexparser.loads(bibtex_str)             
        for entry_dict in bibdb_master.entries:
            mongo_master.insert(entry_dict)       
        delete_duplicates_from_collection(self.mongo_db.mongo_local)  
        delete_duplicates_from_collection(self.mongo_db.mongo_master) 

    def update_bibtexDB(self,is_update):
        """Update the bibtex database with the records from the mongo database
            Args:
                is_update:Flag indicates if the user made any selections to update the current local file
        """
        update_bibtex_mongoDB(is_update,self.bibdb_local,self.mongo_db.mongo_local)

    def update(self,is_update,list_change,list_add):
        """Update the mongodb collections
            Args:
                is_update:Flag indicates if the user made any selections to update the current local file
                list_change: List of properties for each record that have different values on the master file and the local file
                list_add: List of properties for each record that are present on the master file but not on the local
        """
        if(is_update):
            change_property_db(list_change,self.mongo_db.mongo_local)
            add_property_db(list_add,self.mongo_db.mongo_local)

        
    def close(self):
        self.mongo_db.mongo_local.drop()
        self.mongo_db.mongo_master.drop()


def change_property_db(list, db_coll):
    """Update the records in the database collection with the modified values from the list
        Args:
            list: List of properties for each record that have different values on the master file and the local file
            db_coll: database collection that will to be updated
    """
    for idx,val in enumerate(list):
        if (list[idx][2][3].get()):
            result = db_coll.update(
                    {"ID":list[idx][0]},
                    {"$set":{list[idx][1][0]:list[idx][2][1]},
                        "$currentDate": {"lastModified":True}
                    } 
                                          
                )
#     tk.destroy()
def add_property_db(list,db_coll):
    """Update the records in the database collection with the values from the list
        Args:
            list: List of properties for each record that are present on the master file but not on the local
            db_coll: database collection that will to be updated
    """
    for idx,val in enumerate(list):
            result = db_coll.update(
                    {"ID":list[idx][0]},
                    {"$set":{list[idx][1][0]:list[idx][1][1]}}
                )


def delete_duplicates_from_collection(coll):
    """ Deletes duplicates entries from the collection
        Args:
            coll: Mongo Database Collection
    """
    for element in coll.find():
        for entry in element:
            if(entry =="ID"):
                val = element[entry]
                
        temp = element
        coll.remove({"ID":val})
        coll.insert_one(temp)

def update_bibtex_mongoDB(is_update,bibdatabase,mongodb_coll):
    """Updates the bibtex database by comparing the properties for each record with records from the mongo database
        Args:
            is_update:Flag indicates if the user made any selections to update the current local file
            bibdatabase: Bibtex database that needs to be updated
            mongodb_coll:Mongo database collection 
    """
    if(is_update):  
        for dict in bibdatabase.entries:
            change = False 
            if dict.has_key("_id"):
                dict.pop("_id")
            cursor = mongodb_coll.find({"ID":dict["ID"]})
            if(cursor.count>0):
                for doc in cursor:
                    record = doc
                    change = True
                if change: 
                    for each in doc.items():
                        if(each[0]!="_id" and each[0]!="lastModified"):
                            dict[each[0]]=each[1]

