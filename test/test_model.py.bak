from model import *
from controller import *
import unittest

class ModelTest(unittest.TestCase):
    def test_delete_duplicates(self):
            list1=[]
            list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
            list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,
            list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})                        

            conn = connect_mongo()
            db = conn.bibtex_files            
            db.bibtex1.drop()
            bibtex1 = db.bibtex1
            for e in list1:
                bibtex1.insert_one(e)
            delete_duplicates_from_collection(bibtex1)
            assert bibtex1.count()==2
    
    def test_change_record_db(self):

        list1=[]
        list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
        list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,
        conn = connect_mongo()
        db = conn.bibtex_files            
        db.bibtex1.drop()
        bibtex1 = db.bibtex1
        for e in list1:
            bibtex1.insert_one(e)
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2=[]
        list2.append(('Grebe:15:Haskino',('year','2016',1,rb),('year','2017',1,rb)))
        change_property_db(list2,bibtex1)
        cursor = bibtex1.find({"ID": "Grebe:15:Haskino"})
        for doc in cursor:
            master = doc          
        assert master["year"]=='2017'
        tk.destroy()
    def test_add_record_db(self):
        list1=[]
        list1.append({u'title': u'Haskino: {H}askell and {A}rduino', u'booktitle': u'Practical Aspects of Declarative Languages', u'author': u'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', u'year': u'2016', 'ENTRYTYPE': u'inproceedings'})
        list1.append({u'numpages': u'12', u'publisher': u'ACM', u'doi': u'10.1145/2804302.2804311', u'keyword': u'Design Pattern, FFI, Monads, Remote Procedure Call', u'title': u'The Remote Monad Design Pattern', u'xxurl': u'https://www.youtube.com/watch?v=guMLPr6eBLo', u'booktitle': u'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', u'author': u'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', u'abstract': u'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': u'inproceedings', u'link': u'http://dl.acm.org/citation.cfm?id=2804311', u'location': u'Vancouver, BC, Canada', u'xurl': u'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', u'pages': u'59--70', u'address': u'New York, NY, USA'})             ,
        conn = connect_mongo()
        db = conn.bibtex_files            
        db.bibtex1.drop()
        bibtex1 = db.bibtex1
        for e in list1:
            bibtex1.insert_one(e)
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2=[]
#(element["ID"],(b[idx][0],b[idx][1],idx,IntVar()))
        list2.append(('Grebe:15:Haskino',('object','Nothing',1,rb)))
        add_property_db(list2,bibtex1)
        cursor = bibtex1.find({"ID": "Grebe:15:Haskino"})
        for doc in cursor:
            master = doc          
        assert master["object"]=='Nothing'
        tk.destroy()
    def test_update_bibtexDB(self):
        str ="""@inproceedings{Grebe:15:Haskino,
          year={2016},
          booktitle={Practical Aspects of Declarative Languages},
          title={Haskino: {H}askell and {A}rduino},
          author={Grebe, Mark and Gill, Andy}
        }
        """        
        conn = connect_mongo()
        db = conn.bibtex_files            
        db.bibtex1.drop()
        bibtex1 = db.bibtex1

        bib_database = bibtexparser.loads(str)
        for entry_dict in bib_database.entries:
            bibtex1.insert(entry_dict)

        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)


        list2=[]
        list2.append(('Grebe:15:Haskino',('object','Nothing',1,rb)))
        add_property_db(list2,bibtex1)
        update_bibtex_mongoDB(True,bib_database,bibtex1)
        cursor = bibtex1.find({"ID": "Grebe:15:Haskino"})
        for doc in cursor:
            master = doc          
        assert master["object"]=='Nothing'        
        for elem in bib_database.entries:
            result = elem
        assert result['object']=='Nothing'  
        tk.destroy()
if __name__ == "__main__":
    unittest.main()

