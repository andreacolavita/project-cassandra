# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv
from sql_queries import *
from cassandra.cluster import Cluster

FileName = 'event_datafile_new.csv'
Folder = '/event_data'

def process_event_file(session, file):
    """
    Read the event_datafile_new.csv (file) and iterate it to store the required fields into the Cassandra tables. 
    
    INPUT:
    * session of Cassandra cluster
    * file name to store in the Cassandra tables
    """
    
    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        
        #Iterate the file to take artist, song, length, session_id, itemInSession and insert into music_app_history table
        for line in csvreader:
            session.execute(music_app_history_table_insert, (line[0], line[9], float(line[5]), int(line[8]), int(line[3])))
            
    
    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        
        #Iterate the file to take artist, song, firstname, lastname, session_id, itemInSession, user_id and 
        #insert into music_app_users table
        for line in csvreader:
            session.execute(music_app_users_table_insert, (line[0], line[9], line[1], line[4], int(line[8]), int(line[3]), int(line[10])))
 

    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        
        #Iterate the file to take firstname, lastname, session_id, itemInSession, user_id, song 
        #and insert into music_app_songs table
        for line in csvreader:
            session.execute(music_app_songs_table_insert, (line[1], line[4], int(line[8]), int(line[3]), int(line[10]), line[9]))

def process_data(folder):
    """
    Read and iterate the CSV files in the given folder and create event_datafile_new.csv file with the required columns
    that will be used to insert data into the Cassandra tables.
    
    INPUTS:
    * folder where CSV files are stored
    """
    
    # Get your current folder and subfolder event data
    filepath = os.getcwd() + folder

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
    
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 
    
    # for every filepath in the file path list 
    for f in file_path_list:
    
        # reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)

            # extracting each data row one by one and append it        
            for line in csvreader:
                #print(line)
                full_data_rows_list.append(line) 
            

    # creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open(FileName, 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


def main():
    # This should make a connection to a Cassandra instance your local machine 
    # (127.0.0.1)   
    cluster = Cluster()

    # To establish connection and begin executing queries, need a session
    session = cluster.connect()
    
    #Create a Keyspace if not exists
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS cassandra_project 
    WITH REPLICATION = 
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }""")
    
    #Set KEYSPACE to the keyspace specified above
    session.set_keyspace("cassandra_project")

    process_data(Folder)
    #print("data processed")
    process_event_file(session, FileName)
    #print("event file stored into Cassandra db")

    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()