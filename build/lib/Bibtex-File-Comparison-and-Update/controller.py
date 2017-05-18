#!/usr/bin/env python
from . import model
import pymongo
from bibtexparser import *
from tkinter import *
class Controller():
    """ This class is used as an interface between the model and the view """    

    def __init__(self,v):
        """initialize view instance and compare the given files"""
        self.view = v
        self.compare_files()        

    def compare_files(self):
        """parse the two bibtex files using bibtex parser and create two bibtex databases replicate those two databases as mongo databases compare the records from the local file with records from the master file"""
        conn = connect_mongo()
        self.model = model.Model(conn,self.view.master_file.get(),self.view.local_file.get())
        list_add_prop = []
        list_if_equal = []
        (list_if_equal,list_add_prop) = compare_records(self.model.mongo_db.mongo_local,self.model.mongo_db.mongo_master)
        self.view.list_differences(list_if_equal,list_add_prop)

    def update(self,is_update,list_change,list_add):
        """ 
            Update the model and the local file with the user driven modifications and close the controller instance
            Args:
                is_update: Flag indicates if the user made any selections to update the current local file
                list_change: List of properties for each record that have different values on the master file and the local file
                list_add: List of properties for each record that are present on the master file but not on the local
        """    
        self.model.update(is_update,list_change,list_add)
        self.model.update_bibtexDB(is_update)
        self.file_update(is_update)
        self.close()

    def file_update(self,is_update):
        """
            Update the current local file with changes selected by the user
            Args:
                is_update: Flag indicates if the user made any selections to update the current local file            
        """
        if(is_update):
            open(self.view.local_file.get(), 'w').close()
            with open(self.view.local_file.get(), 'w') as bibtex_file:
                bibtex_str = bibtexparser.dumps(self.model.bibdb_local)
                bibtex_file.write(bibtex_str.encode('utf8'))


    def close(self):
        self.model.close()
        self.view.close()

def connect_mongo():
    """Connect to the pymongo client
        Raises:
            pymongo.errors.ConnectionFailure: If no mongo server is running
    """
    try:
        conn = pymongo.MongoClient()
        print("Connected Successfully")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDb")
        
def delete_id (elem):
    """Delete the property '_id' from the dictionary
        Args:
            elem: Dictionary
    """
    for each in elem:
        if(each[0]=="_id"):
            elem.remove(each)
    return elem

def compare_records(coll1,coll2):
    """Compares the records in the mongo db collection coll1 with the records in collection coll2 and prepares two lists
        Args:
            coll1: Local File MongoDb collection
            coll2: Master File MongoDb collection
        Returns:
            (list1,list2): list1 has records with properties having different values on the two colelctions 
                list2 has records with properties present in coll2 but not in coll1
    """
    tk=Tk()
    list_if_equal=[]
    list_add_prop=[]
    for element in coll1.find():
        cursor = coll2.find({"ID":element["ID"]})
        if(cursor.count()>0):
            for doc in cursor:
                master = doc  
            a = sorted(element.items())
            b = sorted(master.items())
            a= delete_id(a)
            b= delete_id(b)
            for idx,val in enumerate(b):
                value = None    
                for each in a:
                    if (each[0]==b[idx][0]):
                        value = each[1]
                        break
                if (value!=None):                       
                            #if the property exists with a different value 
                    if(b[idx][1]!=value):                            
                        e = (element["ID"],(b[idx][0],value,idx,IntVar()),(b[idx][0],b[idx][1],idx,IntVar()))
                        list_if_equal.append(e)
                else:
                    e = (element["ID"],(b[idx][0],b[idx][1],idx,IntVar()))
                    list_add_prop.append(e)
    tk.destroy() 
    return (list_if_equal,list_add_prop)