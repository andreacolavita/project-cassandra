# Project 1: Data Modeling with Cassandra

In this project we are helping our analytics team of *Sparkify* startup to analyze what songs the users are listening to.
We are creating a database in Cassandra, reading from CSV files on user activity on the app and storing it in in the Cassandra tables in order to answer the questions provided by the analytics team. 

## Data Source

### Event Data

The dataset ```event_data``` is available in the dedicated folder where the CSV files are partitioned by date. 

Here are examples of filepaths to two files in the dataset:
```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

Starting from the CVS files available in the ```event_data``` we are creating a new file ```event_datafile_new.csv``` to create a denormalized dataset. 

The image below is a screenshot of how the denormalized dataset looks like:

![Denormalized dataset]("images/image_event_datafile_new.jpg")


## Schema design and ETL pipeline

### Schema Design

As per NoSQL database schema design, we have one single table per query. It is fundamental to have the queries in advance to create the right tables to be queried.

```
Query 1:  Give me the artist, song title and song's length in the music app history that was heard during 
sessionId = 338, and itemInSession = 4
```

Table used: **music_app_history**


```
Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)
for userid = 10, sessionid = 182
```

Table used: **music_app_users**


```
Query 3: Give me every user name (first and last) in my music app history who listened 
to the song 'All Hands Against His Own'

```

Table used: **music_app_songs**


### ETL pipeline

In **etl.ipynb** there is the Jupyter Notebook used to build the ETL code testing it while developing. In **etl.py** there is the python file used to build the ETL pipeline with the code already developed in the Jupyter Notebook to extract, transform and load the data coming from CSV event files (```event_data```) and to store it into Cassandra db. 
