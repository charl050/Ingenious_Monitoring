# Ingenious_Monitoring
A dashboard using Flask to monitor UCL Ingenious stats


## First run

The original database with the name 'inginious.sqlite' is required. A another database must be created with the python script :
```bash
python create_database.py
```


To run the server, the two databases must be at the root directory of the server, like this:
 -  /inginious.sqlite
 -  /useful_data.sqlite
 
 
To start the server, simply excute the following command in terminal, in the root directory
```bash
python routes.py
```


