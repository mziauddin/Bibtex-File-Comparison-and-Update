from Tkinter import *
from logging import root
import Tkinter as tk        
import tkFileDialog
import bibtexparser
import pymongo



class Model():
#initialize controller, mongo database and bibtex database in the model class
    def __init__(self,controller,mongoDb,bibtex_db):
        self.controller = controller
        self.database = mongoDb
        self.bibdatabase = bibtex_db
#Update the bibtex database with the records from the mongo database
    def update_bibtexDB(self,flag):
        if(flag):
            for dict in self.bibdatabase.entries:
                dict.pop("_id")
                cursor = self.database.bibtex1.find({"ID":dict["ID"]})
                for doc in cursor:
                    record = doc
                for each in doc.items():
                    if(each[0]!="_id" and each[0]!="lastModified"):
                        dict[each[0]]=each[1]
        self.controller.close(flag)

class Controller():
#when inserting the parsed bibtex file records into mongo Db, duplicate records get created. Deleting duplicates
#from the given collection
    def delete_duplicates_from_collection(self,coll):
        for element in coll.find():
            for entry in element:
                if(entry =="ID"):
                    val = element[entry]
                    
            temp = element
            coll.remove({"ID":val})
            coll.insert(temp)
        
#delete the attribute _id from the record for comparison
    def delete_id (self,elem):
        for each in elem:
            if(each[0]=="_id"):
                elem.remove(each)
        return elem

#initialize the file values and the view instance
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
        
#define  mongoDB database        
        db = conn.bibtex_files
# define collection where I'll insert my local files data
        bibtex1 = db.bibtex1
            
        with open(self.file1) as bibtex1_file:
            bibtex1_str = bibtex1_file.read()
#create bibtex database for local file        
        self.bib_database1 = bibtexparser.loads(bibtex1_str)
            
        for entry_dict in self.bib_database1.entries:
            bibtex1.insert(entry_dict)
# define collection where I'll insert my master files data            
        bibtex = db.bibtex
        with open(self.file2) as bibtex_file:

            bibtex_str = bibtex_file.read()
#create bibtex database for master file                    
        bib_database2 = bibtexparser.loads(bibtex_str)
            
        for entry_dict in bib_database2.entries:
            bibtex.insert(entry_dict)   
        
        self.model = Model(self,db,self.bib_database1)
        
        self.delete_duplicates_from_collection(db.bibtex1)  
        self.delete_duplicates_from_collection(db.bibtex) 
           
# list_add_prop if property does not exist in local file
# list_if_equal if property exist but different values in local file and master file
        list_add_prop = []
        list_if_equal = []
        
        for element in db.bibtex1.find():
            cursor = db.bibtex.find({"ID":element["ID"]})
            if(cursor.count()>0):
                for doc in cursor:
                    master = doc  
                a = sorted(element.items())
                b = sorted(master.items())
                a= self.delete_id(a)
                b= self.delete_id(b)
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

    def close(self,flag):
        if(flag):
            open(self.file1, 'w').close()
            with open(self.file1, 'w') as bibtex_file:
                bibtex_str = bibtexparser.dumps(self.bib_database1)
                bibtex_file.write(bibtex_str.encode('utf8'))
        self.view.close()
        
        
class View(tk.Frame):
    count = 0
    model = ""
    def openmasterfile(self,event):
        master_file.set(tkFileDialog.askopenfilename()) 

    def openlocalfile(self,event):
        local_file.set(tkFileDialog.askopenfilename())

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        label_1 = Label(self, text = "Local File")
        label_2 = Label(self, text = "Master File")
        
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
        controller = Controller(master_file.get(),local_file.get(),self)
        controller.parse_files()
        
    def close(self):
        self.destroy()
        root_close()
        
    def print_list_buttons(self,list,list_add):
        if(self.update):
        
            for idx,val in enumerate(list):
                if (list[idx][2][3].get()):# + list[idx][1][2]
                    result = self.model.database.bibtex1.update(
                            {"ID":list[idx][0]},
                            {"$set":{list[idx][1][0]:list[idx][2][1]},
                                "$currentDate": {"lastModified":True}
                            } 
                                                  
                        )

            for idx,val in enumerate(list_add):
                if (list_add[idx][1][3].get()):# + list[idx][1][2]
                    result = self.model.database.bibtex1.update(
                            {"ID":list_add[idx][0]},
                            {"$set":{list_add[idx][1][0]:list_add[idx][1][1]}}
                        )
        
        self.model.update_bibtexDB(self.update)
        
                    
    def list_differences(self,list,list2,ref):

        def onFrameConfigure(canvas):
    #'''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.model = ref
        
        new_window = tk.Toplevel(self)
        canvas = tk.Canvas(new_window, borderwidth=0, background="#ffffff")
        window = tk.Frame(canvas, background="#ffffff") 
        vsb = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)   
        hsb = tk.Scrollbar(new_window, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand = hsb.set,yscrollcommand=vsb.set)
        
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="top", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=window, anchor="nw")     
        
        window.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

        line = 0

        if(len(list)>0):
            current_elem = list[0][0]
            Label(window,text="There is a difference in the below properties for the master and local file",font=("Times", 16),foreground="Blue").grid(columnspan=2,sticky=W,padx=2,pady=2)
            for idx,val in enumerate(list):
                line = line+1
                new_elem = list[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem,font=("Times", 14,"bold")).grid(row=line+1,sticky=W,padx=1,pady=1)
                    current_elem=new_elem
                    line = line +1
                Label(window,text=list[idx][1][0]+":").grid(row=line+1,column=0,sticky=W,padx=1,pady=1)
                Label(window, text=list[idx][1][1]).grid(row=line+1,column=1,sticky=W,padx=1,pady=1)
                Label(window,text=list[idx][2][0]+":").grid(row=line+1,column=2,sticky=W,padx=1,pady=1)
                Radiobutton(window, text=list[idx][2][1],variable=list[idx][2][3]).grid(row=line+1,column=3,sticky=W,padx=1,pady=1)

        line = line+2

        if(len(list2)>0):
            Label(window,text="Below property is not present in the local file",font=("Times", 16),foreground="Blue").grid(row = line,columnspan=2,sticky=W,padx=1,pady=1)
            Label(window,text="Select properties you want to add",font=("Times", 16),foreground="Blue").grid(row = line+1,columnspan=2,sticky=W,padx=1,pady=1)
            line = line +2
            current_elem = list2[0][0]    
            for idx,val in enumerate(list2):
                line = line+1
                new_elem = list2[idx][0]
                if(new_elem!=current_elem or idx==0):
                    Label(window,text="ID:"+current_elem,font =("Times", 14,"bold")).grid(row=line+1,columnspan=2,sticky=W,padx=1,pady=1)
                    current_elem=new_elem
                    line = line+1
                Label(window,text=list2[idx][1][0]+":").grid(row=line+1,sticky=W,padx=1,pady=1)
                Radiobutton(window, text=list2[idx][1][1],variable=list2[idx][1][3]).grid(row=line+1,column=1,sticky=W,padx=1,pady=1)
        
        self.update = True
        if(len(list)==0 and len(list2)==0):
            Label(window,text="No differences between the two files",font=("Times", 16),foreground="Blue").grid(row = line,columnspan=2,sticky=W,padx=1,pady=1)
            self.update = False
        Button(window, text="Done", command=lambda:self.print_list_buttons(list,list2)).grid(columnspan=2,sticky=W,padx=1,pady=1)

if __name__ == "__main__":
    root = tk.Tk()
    master_file = StringVar()
    local_file = StringVar()
    
    view = View(root)
    view.pack(side="top", fill="both", expand=True)
    def root_close():
        root.destroy()
    root.mainloop()
