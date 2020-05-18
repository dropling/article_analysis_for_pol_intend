# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:21:12 2020

@author: marku
"""

import psycopg2 as pg2
import datetime

"""
To do:
    get_author_ID (maybe just use one mod. function for source and author)
    Comment stuff
"""

class Sql_manager():
    
    
    conn = None
    cur = None
    database = None
    user = None
    pw = None
    
    # Initialization script, save options, open connection
    def  __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.pw = password
        
        if(self.open_connection() == False):
            # Log.log('Sql_manager: Initialization failed!')
            raise Exception('Initialization failed!')
    
    # Check if options valid type, try open connection
    def open_connection(self):
        if(self.check_connection_settings_content_on_type()):
            try:
                self.conn = pg2.connect(database = self.database,
                                        user = self.user,
                                        password = self.pw)
                self.cur = self.conn.cursor()
            except:
                return False
        return True
    
    # Check if the options are not None and type String
    def check_connection_settings_content_on_type(self):
        for setting in [self.database, self.user, self.pw]:
            if(not setting):
                return False
            if(not type(setting) == str):
                return False
        return True
    
    # Check if connection is active, try to close.
    # Return False if closing not successful. Otherwise return True
    def close_connection(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                return False
            self.cur = None
            self.conn = None
        return True
    
    # Get the source_ID. If source not found, insert new source, repeat once
    # Return source_ID if found. Return None if failed.
    def get_source_ID(self, source):
    
        # Create flag to avoid being trapped in loop
        flag = 0
        
        while(True):
            
            try:
                # Try to read the source_ID necessary for the article insertion statement into article_data
                self.cur.execute(f"SELECT source_ID FROM source_data WHERE source like '{source}'")
            except:
                # If an error occurs, rollback the connection and return None as an error hint
                self.conn.rollback()
                return None
            
            # Fetch the results from the query
            result = self.cur.fetchall()
            
            # If the right number of values (1) was received, return the cleaned value from the list of tuples [()]
            # If no value was read, create new entry with source. Since while is still running, there will be repeat
            # If more than one or zero values were received or something unforeseen, return None
            if(len(result) == 1):
                return result[0][0]
            elif(len(result) == 0):
                
                # If flag was set, inserting a new entry was not successful
                if(flag == 1):
                    return None
                
                # insert_new_source() returns either True or False depending on the success of the insertion
                if(not self.insert_new_source(source)):
                    
                    # If insertion failed: return None
                    return None
                
                # Set flag to avoid being trapped in loop
                flag = 1
            else:
                return None
    
    # Insert a new source. If successful return True, otherwise False
    def insert_new_source(self, source, source_name = None):
    
        # Check if the source and source name are available to fill another field
        if(source_name and source):
            
            # Execute query. If failed, return False, if successfull (No error was detected) return True
            try:
                self.cur.execute(f"INSERT INTO source_data(source_name,source_page) VALUES('{source_name}','{source}')")
                self.conn.commit()
            except:
                self.conn.rollback()
                return False
            
            return True
        
        # Source name is not available but source is
        elif(not source_name and source):
            
            # Execute query. If failed, return False, if successfull (No error was detected) return True
            try:
                self.cur.execute(f"INSERT INTO source_data(source_page) VALUES('{source}')")
                self.conn.commit()
            except:
                self.conn.rollback()
                return False
            
            return True
        
        # None is or error
        else:
            pass
        return False
    
    # Steps for the insertion of the article data:
    # Get source_ID, Insert_information
    def insert_article_data(self, source, article_title, article_text, author_name = None):
        source_ID = self.get_source_ID(source)
        author_ID = None
        dl_timestamp = self.get_date()
        input_data_variables = f"source_ID,"
        input_data = f"'{source_ID}',"
        
        if(not source_ID):
            return None
        
        if(author_name):
            author_ID = self.get_author_ID(author_name)
        
        # source_ID,author_name, article_title, article_text, dl_timestamp        
               
        def create_var_dict():
            var_dict = {}
            
            if(source_ID):
                var_dict['source_ID'] = source_ID
            if(author_name):
                var_dict['author_name'] = author_name 
            if(author_ID):
                var_dict['author_ID'] = author_ID 
            if(article_title):
                var_dict['article_title'] = article_title
            if(article_text):
                var_dict['article_text'] = article_text
            if(dl_timestamp):
                var_dict['dl_timestamp'] = dl_timestamp
                
            return var_dict
        
        for key, value in self.create_var_dict():
            input_data_variables += f",'{key}'"
            input_data += f",'{value}'"
            
        self.cur.execute(f"INSERT INTO article_data({input_data_variables}) VALUES({input_data})")
        self.conn.commit()
        
    def get_date(self):
        current_date = datetime.datetime.now()
        return str(current_date.year)+'-'+str(current_date.month)+'-'+str(current_date.day)