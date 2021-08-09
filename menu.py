#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 08 - Relational Database - DataSet API

'''
    Provides a basic frontend
'''
import sys
from datetime import datetime
from playhouse.dataset import DataSet
import pysnooper
from loguru import logger
import main

log_file = datetime.now().strftime("log_%m_%d_%Y.log")
logger.add(log_file, level="INFO")


@pysnooper.snoop()
def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    if main.load_users(filename, user_collection):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


@pysnooper.snoop()
def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    if main.load_status_updates(filename, status_collection, user_collection):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


@pysnooper.snoop()
def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')

    if not main.add_user(user_id,
                         user_name,
                         user_last_name,
                         email,
                         user_collection
                         ):
        print("Error occurred while trying to add new user")
    else:
        print("User was successfully added")


@pysnooper.snoop()
def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')

    if user_collection.find_one(user_id=user_id):
        if not main.update_user(user_id,
                                user_name,
                                user_last_name,
                                email,
                                user_collection
                                ):

            print("Error occurred while trying to update user")
        print("User was successfully updated")
    else:
        print("Error occurred while trying to update user")


@pysnooper.snoop()
def search_user():
    '''
        Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    try:
        search = main.search_user(user_id, user_collection)
        print(f'User id: {search["user_id"]}')
        print(f'User name: {search["user_name"]}')
        print(f'User last name: {search["user_last_name"]}')
        print(f'User email: {search["email"]}')
    except TypeError:
        print("Error: User does not exist")


@pysnooper.snoop()
def delete_user():
    '''
        Deletes user from the database
    '''
    user_id = input('User ID: ')
    if user_collection.find_one(user_id=user_id):
        if not main.delete_user(user_id, user_collection, status_collection):
            print("Error occurred while trying to delete user")
        else:
            print("User was successfully deleted")
    else:
        print("Error occurred while trying to delete user")


@pysnooper.snoop()
def add_status():
    '''
        Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')

    if not main.add_status(user_id,
                           status_id,
                           status_text,
                           status_collection,
                           user_collection):
        print("Error occurred while trying to add new status")
    else:
        print("New status was successfully added")


@pysnooper.snoop()
def update_status():
    '''
        Updates information for an existing status
    '''
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if status_collection.find_one(status_id=status_id):
        if not main.update_status(status_id, status_text, status_collection):
            print("Error occurred while trying to update status")
        else:
            print("Status was successfully updated")
    else:
        print("Error occurred while trying to update status")


@pysnooper.snoop()
def search_status():
    '''
        Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    try:
        search = main.search_status(status_id, status_collection)
        print(f'User id: {search["user_id"]}')
        print(f'Status ID:: {search["status_id"]}')
        print(f'Status text: {search["status_text"]}')
    except TypeError:
        print("Error: Status ID does not exist")


@pysnooper.snoop()
def delete_status():
    '''
        Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if status_collection.find_one(status_id=status_id):
        if not main.delete_status(status_id, status_collection):
            print("Error occurred while trying to delete status")
        else:
            print("Status was successfully deleted")
    else:
        print("Error occurred while trying to delete status")


@pysnooper.snoop()
def quit_program():
    '''
        Quits program
    '''
    print("Exiting program")
    sys.exit()


if __name__ == '__main__':

    # instantiate database
    db = DataSet('sqlite:///socialnetwork.db')

    # ===========================================================================
    # instantiate Users tables
    user_collection = db['Users']
    user_collection.insert(user_id='dummy',
                           user_name='dummy',
                           user_last_name='dummy',
                           email='dummy'
                           )
    user_collection.create_index(['user_id'], unique=True)
    user_collection.delete(user_id='dummy',
                           user_name='dummy',
                           user_last_name='dummy',
                           email='dummy')

    # ===========================================================================
    status_collection = db['Status']
    status_collection.insert(status_id='dummy',
                             user_id='dummy',
                             status_text='dummy')

    status_collection.create_index(['status_id'], unique=True)
    status_collection.delete(status_id='dummy',
                             user_id='dummy',
                             status_text='dummy')
    # ===========================================================================

    # user menu
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            Q: Quit

                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
