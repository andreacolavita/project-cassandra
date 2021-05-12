# Import Python packages 
import cassandra
from sql_queries import create_table_queries, drop_table_queries

def create_database():
    """
    Connect to the Cassandra cluster and get the session to create and set the keyspace (db)
    """
    # This should make a connection to a Cassandra instance your local machine 
    # (127.0.0.1)

    from cassandra.cluster import Cluster
    cluster = Cluster()

    # To establish connection and begin executing queries, need a session
    session = cluster.connect()
   
    #Create a Keyspace 
    try:
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS cassandra_project 
        WITH REPLICATION = 
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
    )

    except Exception as e:
        print(e)
    
    # Set the Keyspace
    try:
        session.set_keyspace("cassandra_project")
    except Exception as e:
        print(e)
    
    return session, cluster


def drop_tables(session):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        session.execute(query)

        
def create_tables(session):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        session.execute(query)

        
def main():
    """
    - Drops (if exists) and Create the database. 
    
    - Establishes connection with the database 
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    session, cluster = create_database()
    
    drop_tables(session)
    create_tables(session)

    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()