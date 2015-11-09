from Tkinter import Tk,BOTH, Entry, IntVar
from ttk import *
import Tkinter, Tkconstants, tkFileDialog
from logging import root
import Tkinter as tk        
from Tkinter import *
from ttk import *
import Tkinter, Tkconstants, tkFileDialog
from Finder.Type_Definitions import column
import bibtexparser
import pymongo



class Model():

    
    def __init__(self,controller,mongoDb,bibtex_db):
        self.controller = controller
        self.database = mongoDb
        self.bibdatabase = bibtex_db
    def update_bibtexDB(self):

        for dict in self.bibdatabase.entries:
            dict.pop("_id")
            cursor = self.database.bibtex1.find({"ID":dict["ID"]})
            for doc in cursor:
                record = doc
            print doc
            for each in doc.items():
                if(each[0]!="_id" and each[0]!="lastModified"):
                    dict[each[0]]=each[1]
                
        self.controller.close()
class Controller():
    file1=""
    file2=""
    view = ""
    def connect_mongodb(self):
        try:
            conn = pymongo.MongoClient()
            print "Connected Successfully"
            return conn
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDb : %s" % e
    

    def delete_duplicates_from_collection(self,coll):
        for element in coll.find():
            for entry in element:
                if(entry =="ID"):
                    val = element[entry]
                    
            temp = element
            coll.remove({"ID":val})
            coll.insert(temp)
        

    def delete_id (self,elem):
        for each in elem:
            if(each[0]=="_id"):
                elem.remove(each)
        return elem

    
    def search_element_in_coll(self,element_01,coll):
        cursor = coll.find({"ID":element_01["ID"]})
        if(cursor.count()>0):
            for doc in cursor:
                element_02 = doc  
            a = sorted(element_01.items())
            b = sorted(element_02.items())
            a= self.delete_id(a)
            b= self.delete_id(b)
            if(a==b):
                return 0
            else:
                return 1

    def compare_no_of_att(self,a,b):
        compare = {}
        for idx,val in enumerate(a):
            compare[a[idx][0]] = 1
        for idx,val in enumerate(b):
            if(not(compare.has_key(b[idx][0]))):
                compare[b[idx][0]] = 1
        if(len(compare.items())==len(a)):
            return True
        else:
            return False
    
    def __init__(self,a,b,v):
            self.file1 = a
            self.file2 = b 
            self.view = v

    def parse_files(self):
        try:
            conn = pymongo.MongoClient()
            print "Connected Successfully"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDb : %s" % e
        
        
        db = conn.bibtex_files
        db.bibtex.drop()
        db.bibtex1.drop()
            # define collection where I'll insert my individual files data
        bibtex1 = db.bibtex1
            
        with open(self.file1) as bibtex1_file:
#             print self.file1
            bibtex1_str = bibtex1_file.read()
        
        self.bib_database1 = bibtexparser.loads(bibtex1_str)
            
        for entry_dict in self.bib_database1.entries:
#             print entry_dict
            bibtex1.insert(entry_dict)
            
        bibtex = db.bibtex
        with open(self.file2) as bibtex_file:

            bibtex_str = bibtex_file.read()
            
        bib_database2 = bibtexparser.loads(bibtex_str)
            
        for entry_dict in bib_database2.entries:
#             print entry_dict
            bibtex.insert(entry_dict)   
        
        self.model = Model(self,db,self.bib_database1)
        
        self.delete_duplicates_from_collection(db.bibtex1)  
        self.delete_duplicates_from_collection(db.bibtex) 
           
            # compare the elements from collection bibtex with the elements in collection bibtex1
        list = []
        for element in db.bibtex1.find():
            print element
            if(self.search_element_in_coll(element,db.bibtex)):
                list.append(element)
        if(len(list)>0):
            for element in list:
                cursor = db.bibtex.find({"ID":element["ID"]})
                if(cursor.count()>0):
                    for doc in cursor:
                        master = doc  
                    a = sorted(element.items())
                    b = sorted(master.items())
                    a= self.delete_id(a)
                    b= self.delete_id(b)
                    print a 
                    print b
                    print "\n"
                    list_add_prop = []
#                     if (len(a)==len(b)):
#                         print "Lengths are equal"
                    equal = self.compare_no_of_att(a,b)
                    list_if_equal = []
                    if (equal):
                        for idx,val in enumerate(a):
                            value = None
                
                            if(a[idx]!=b[idx]):
#                                     print "There's a difference in the below property for the record with the master file"
                                    e = (element["ID"],(a[idx][0],a[idx][1],idx,IntVar()),(b[idx][0],b[idx][1],idx,IntVar()))
                                    list_if_equal.append(e)
                    else:
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

            self.view.list_differences(list_if_equal,list_add_prop,self.model)
        else:
            print "No elements in list"


    def close(self):
        with open(self.file1, 'w') as bibtex_file:
            bibtex_str = bibtexparser.dumps(self.bib_database1)
            bibtex_file.write(bibtex_str.encode('utf8'))
        self.view.destroy()
        
        
class View(tk.Frame):
    count = 0
    model = ""
    def openmasterfile(self,event):
        master_file.set(tkFileDialog.askopenfilename()) 

    
    def openlocalfile(self,event):
        local_file.set(tkFileDialog.askopenfilename())

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        label_1 = Label(self, text = "First File")
        label_2 = Label(self, text = "Second File")
        
        master_file_entry = Entry(self, text=master_file)
        master_file_entry.bind("<Button-1>", self.openmasterfile)
        local_file_entry = Entry(self, text=local_file)
        local_file_entry.bind("<Button-1>", self.openlocalfile)
        label_1.grid(row = 0,sticky=E)
        label_2.grid(row = 1,sticky=E)
        master_file_entry.grid(row = 0, column = 1)
        local_file_entry.grid(row=1,column=1)
        ok_button = Button(self,text = "Submit",command = self.call_controller)
        ok_button.grid(columnspan=2)
    



    def call_controller(self):
        print master_file.get()
        controller = Controller(master_file.get(),local_file.get(),self)
        controller.parse_files()
        
        
    def print_list_buttons(self,list,list_add):

        
        for idx,val in enumerate(list):
            if (list[idx][2][3].get()):# + list[idx][1][2]
                result = self.model.database.bibtex1.update(
                        {"ID":list[idx][0]},
                        {"$set":{list[idx][1][0]:list[idx][2][1]},
                            "$currentDate": {"lastModified":True}
                        } 
                                              
                    )
                cursor = self.model.database.bibtex1.find({"ID":list[idx][0]})
                for doc in cursor:
                    print doc
        for idx,val in enumerate(list_add):
            if (list_add[idx][1][3].get()):# + list[idx][1][2]
                result = self.model.database.bibtex1.update(
                        {"ID":list_add[idx][0]},
                        {"$set":{list_add[idx][1][0]:list_add[idx][1][1]}}
                    )
                cursor = self.model.database.bibtex1.find({"ID":list_add[idx][0]})
                for doc in cursor:
                    print doc
        
        self.model.update_bibtexDB()
        
                    
    def list_differences(self,list,list2,ref):
        self.model = ref
        window = tk.Toplevel(self)
        window.grid()
        line = 0

        if(len(list)>0):
            current_elem = list[0][0]
            Label(window,text="There is a difference in the below properties for the master and local file").grid(columnspan=2)
            for idx,val in enumerate(list):
                line = line+1
                new_elem = list[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem).grid(row=line+1)
                    current_elem=new_elem
                    line = line +1
                Label(window,text=list[idx][1][0]+":").grid(row=line+1,column=0)
                Label(window, text=list[idx][1][1]).grid(row=line+1,column=1)
                Label(window,text=list[idx][2][0]+":").grid(row=line+1,column=2)
                Radiobutton(window, text=list[idx][2][1],variable=list[idx][2][3]).grid(row=line+1,column=3)
        line = line+2
        if(len(list2)>0):
            Label(window,text="Below property is not present in the local file").grid(row = line,columnspan=2)
            Label(window,text="Select properties you want to add").grid(row = line+1,columnspan=2)
            line = line +2
            current_elem = list2[0][0]    
            for idx,val in enumerate(list2):
                line = line+1
                new_elem = list2[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem).grid(row=line+1,columnspan=2)
                    current_elem=new_elem
                    line = line+1
                Label(window,text=list2[idx][1][0]+":").grid(row=line+1)
                Radiobutton(window, text=list2[idx][1][1],variable=list2[idx][1][3]).grid(row=line+1,column=1)

        
        Button(window, text="Done", command=lambda:self.print_list_buttons(list,list2)).grid(columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    master_file = StringVar()
    local_file = StringVar()
    
    view = View(root)
    view.pack(side="top", fill="both", expand=True)
    def close():
        root.destroy()
    root.mainloop()
