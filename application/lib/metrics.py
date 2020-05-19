# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:03:47 2020

@author: dropling
"""

import functools, logging, time, datetime

log_file_flag = False

def set_logging_file(string):
    global log_file_flag
    logging.basicConfig(filename=string+".log",level=logging.DEBUG)
    log_file_flag = True
# function taken from realpython.com/ decorators
def measure_run_time(func):
    # Measure runtime
    @functools.wraps(func)
    def wrapper_run_time(*args, **kwargs):
        if(log_file_flag):
            # Get the date
            date = str(datetime.date.today())
            
            # Execute function, measure run time
            start_time = time.perf_counter()
            return_value = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # Calculate run_time and log
            run_time = end_time - start_time
            logging.info(f"{func.__name__!r}, run_time, {date}, {run_time}")
            return return_value
        else:
            return func(*args, **kwargs)
    return wrapper_run_time

def debug(func):
    # Get function signatures and returns
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        if(log_file_flag):
            # Gather the signature information
            args_repr = [repr(a) for a in args]   
            kwargs_repr = [f"{k}:{v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            # Get the date
            date = str(datetime.date.today())
            
            # Log the call
            logging.info(f"{func.__name__!r}, call, {date}, {signature}")
            
            # Execute function
            return_value = func(*args, **kwargs)
            
            # Log return values
            logging.info(f"{func.__name__!r}, return, {date}, {return_value!r}")           
            return return_value
        else:
            return func(*args, **kwargs)
    return wrapper_debug

def debug_measure_run_time(func):
    # Get function signatures and returns while measuring and logging time
    @functools.wraps(func)
    def wrapper_dmrt(*args, **kwargs):
        if(log_file_flag):
            # Gather the signature information
            args_repr = [repr(a) for a in args]   
            kwargs_repr = [f"{k}:{v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            # Get the date
            date = str(datetime.date.today())
            
            # Log the call
            logging.info(f"{func.__name__!r}, call, {date}, {signature}")
            
            # Execute function, measure run time
            start_time = time.perf_counter()
            return_value = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # Calculate run_time and log
            run_time = end_time - start_time
            logging.info(f"{func.__name__!r}, run_time, {date}, {run_time}")
            
            # Log return values
            logging.info(f"{func.__name__!r}, return, {date}, {return_value!r}")           
            return return_value
        else:
            return func(*args, **kwargs)
    return wrapper_dmrt

@debug_measure_run_time
def test(string, integer):
    print(string)
    count = 0
    for i in range(integer):
        count += 1
    
    return string+" "+str(count)