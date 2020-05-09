# Use this function to create the database

from lib import *

def create_useful_database():
    """
    post : create a sqlite file with useful data if it doesn't already exist
    """
    if not path.exists("useful_data.sqlite"):
        # date list
        l = dates("data_inginious.sqlite")
        # create submissions table
        d = results("data_inginious.sqlite",l)
        create_submissions_table("useful_data.sqlite", d)
        # create courses table
        d = results_courses("data_inginious.sqlite",l)
        create_courses_table("useful_data.sqlite", d)
        #create LSINF1101-PYTHON table
        d = LSINF1101_PYTHON_tasks("data_inginious.sqlite", l)
        create_LSINF1101_PYTHON_table("useful_data.sqlite", d)
        #create LEPL1402 table
        d = LEPL1402_tasks("data_inginious.sqlite", l)
        create_LEPL1402_table("useful_data.sqlite", d)
        #create LSINF1252 table
        d = LSINF1252_tasks("data_inginious.sqlite", l)
        create_LSINF1252_table("useful_data.sqlite", d)
        print("useful_data.sqlite has been created well")
    else:
        print("useful_data.sqlite already exists")
        
if __name__ == 'main':
  create_useful_database()
  
  
