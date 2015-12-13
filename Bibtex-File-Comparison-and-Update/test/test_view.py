import unittest
from view import *
from controller import *
import os
class ViewTest(unittest.TestCase):

    def test_positive_create_local_repo(self):
        git_url = "git@github.com:mziauddin/Bibtex-File-Comparison-and-Update.git"
        branch = "master"
        path = os.getcwd()+"/"+"clone_remote"  
        repo = create_local_repo(git_url,path,branch)
        assert not repo.bare
        shutil.rmtree(path)

    def test_negative_create_local_repo(self):

        import sys
        from StringIO import StringIO

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
#this is a fake git url            
            git_url = "git@github.com:mziauddin/testing.git"
            branch = "master"
            path = os.getcwd()+"/"+"clone_remote"              
            create_local_repo(git_url,path,branch)
            output = out.getvalue().strip()
            assert output == 'Please make sure you have the correct access rights and the repository exists'
        finally:
            sys.stdout = saved_stdout
            
    def test_negative_extract_bib_files(self):
#this is a fake directory        
        path = os.getcwd()+"/"+"no_dir" 
        result = extract_bib_files(path)
        assert not result
        
    def test_positive_extract_bib_files(self):
#create a dir
    
        import os
        directory = os.getcwd()+"/"+"bib_files"
        if not (os.path.exists(directory)):
            os.mkdir(directory)
           
        filename1 = "test1.bib"
        with open(os.path.join(directory, filename1), 'wb') as temp_file:
            temp_file.write("")
        filename2 = "test2.bib"        
        with open(os.path.join(directory, filename2), 'wb') as temp_file:
            temp_file.write("")
        
        expected = [directory+"/"+filename1,directory+"/"+filename2]    
        result = extract_bib_files(directory)
        assert len(result)==2
        assert sorted(expected) == sorted(result)
        shutil.rmtree(directory)
        
    def test_commit_remote(self):
        git_url = "git@github.com:mziauddin/testing_gitpython.git"
        branch = "master"
        path = os.getcwd()+"/"+"clone_remote"  
        repo = create_local_repo(git_url,path,branch)
        filename1 = "test1.bib"
        with open(os.path.join(path, filename1), 'wb') as temp_file:
            temp_file.write("")
        commit_remote(repo,path+"/"+filename1)
            
if __name__ == "__main__":
    unittest.main()