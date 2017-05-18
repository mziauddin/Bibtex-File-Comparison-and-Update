from controller import *
import unittest
class ControllerTest(unittest.TestCase):
    def test_compare_records(self):
        try:
#create a mongo database
            list1=[]
            list1.append({'title': 'Haskino: {H}askell and {A}rduino', 'booktitle': 'Practical Aspects of Declarative Languages', 'author': 'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', 'year': '2016', 'ENTRYTYPE': 'inproceedings'})
            list1.append({'numpages': '12', 'publisher': 'ACM', 'doi': '10.1145/2804302.2804311', 'keyword': 'Design Pattern, FFI, Monads, Remote Procedure Call', 'title': 'The Remote Monad Design Pattern', 'xxurl': 'https://www.youtube.com/watch?v=guMLPr6eBLo', 'booktitle': 'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', 'author': 'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', 'abstract': 'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': 'inproceedings', 'link': 'http://dl.acm.org/citation.cfm?id=2804311', 'location': 'Vancouver, BC, Canada', 'xurl': 'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', 'pages': '59--70', 'address': 'New York, NY, USA'})             ,
            
            list2=[]
            list2.append({'title': 'Haskino: {H}askell and {A}rduino', 'booktitle': 'Practical Aspects of Declarative Languages', 'author': 'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', 'year': '2015', 'ENTRYTYPE': 'inproceedings'})
            list2.append({'numpages': '12', 'publisher': 'ACM', 'doi': '10.1145/2804302.2804311', 'keyword': 'Design Pattern, FFI, Monads, Remote Procedure Call', 'title': 'The Remote Monad Design Pattern', 'xxurl': 'https://www.youtube.com/watch?v=guMLPr6eBLo', 'booktitle': 'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', 'author': 'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', 'abstract': 'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': 'inproceedings', 'link': 'http://dl.acm.org/citation.cfm?id=2804311', 'location': 'Vancouver, BC, Canada', 'xurl': 'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'year': '2015','ID': 'Gill:15:RemoteMonad', 'pages': '59--70', 'address': 'New York, NY, USA'})
            
            conn = connect_mongo()
            db = conn.bibtex_files            
            db.bibtex1.drop()
            db.bibtex2.drop()
            bibtex1 = db.bibtex1
            bibtex2 = db.bibtex2
            for e in list1:
                bibtex1.insert(e)
            for e in list2:
                bibtex2.insert(e)
            
            list1 = []
            list2 = []
            (list1,list2) = compare_records(bibtex1,bibtex2)
            assert len(list1)==1
            assert len(list2)==1
            
            
        except:
            print("Error")
            
    def test_delete_id(self):
            dict1 = dict()
            dict1.update({'title': 'Haskino: {H}askell and {A}rduino', 'booktitle': 'Practical Aspects of Declarative Languages','_id':'1234'})
            result = delete_id((list(dict1.items())))
            assert len(result)==2
            
            
        
if __name__ == "__main__":
    unittest.main()