#!/usr/bin/env python3
# 05/04/2021
# Dev: Cody Yarger
# Assignment 08 - Relational Database - DataSet API
''' Test unit for social netowrk '''
# pylint: disable=C0103


from unittest import TestCase
from loguru import logger
import peewee as pw
from playhouse.dataset import DataSet
import users
import user_status


class UserDatabaseTest(TestCase):
    '''
        Tests for UserCollection methods
    '''
###############################################################################
# setUp and tearDown
###############################################################################

    def setUp(self):
        ''' Setup test database '''

        # instantiate database
        self.db = DataSet('sqlite:///:memory:')

        # ===========================================================================
        self.user_collection = self.db['Users']
        self.user_collection.insert(user_id='dummy',
                                    user_name='dummy',
                                    user_last_name='dummy',
                                    email='dummy'
                                    )
        self.user_collection.create_index(['user_id'], unique=True)
        self.user_collection.delete(user_id='dummy',
                                    user_name='dummy',
                                    user_last_name='dummy',
                                    email='dummy')

        # ===========================================================================
        self.status_collection = self.db['Status']
        self.status_collection.insert(status_id='dummy',
                                      user_id='dummy',
                                      status_text='dummy')

        self.status_collection.create_index(['status_id'], unique=True)
        self.status_collection.delete(status_id='dummy',
                                      user_id='dummy',
                                      status_text='dummy')

        # =======================================================================
        # Test user table data
        users_list = [
            ('id1', 'email1', 'name1', 'last1'),
            ('id2', 'email2', 'name2', 'last2'),
            ('id3', 'email3', 'name3', 'last3')
        ]

        # for users populate test database
        for user in users_list:
            # insert user data into db model
            try:
                self.user_collection.insert(user_id=user[0],
                                            user_name=user[1],
                                            user_last_name=user[2],
                                            email=user[3])
            except pw.IntegrityError:
                logger.info('Error populating user_collection')

        # =======================================================================
        # Test status table data
        statuses = [
            ('id1', 'status1', 'text1'),
            ('id2', 'ststus2', 'text2'),
            ('id3', 'ststus3', 'text3')]

        # for status populate test database
        for status in statuses:
            try:
                self.status_collection.insert(user_id=status[0],
                                              status_id=status[1],
                                              status_text=status[2])
            except pw.IntegrityError:
                logger.info('Error populating status_collection')

    def tearDown(self):
        ''' Teardown test database '''
        self.db.close()

# ###############################################################################
# # users.py tests
# ###############################################################################
    # @pysnooper.snoop()
    def test_add_user(self):
        ''' Test add user '''
        expected = users.add_user('id4', 'name4', 'last4', 'email4', self.user_collection)
        self.assertTrue(expected)

    def test_add_user_false(self):
        ''' Test add user false'''
        expected = users.add_user('id1', 'name4', 'last4', 'email4', self.user_collection)
        self.assertFalse(expected)

    def test_add_user_len_false(self):
        ''' Test add user false'''
        thirty = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        expected = users.add_user(thirty, 'name4', 'last4', 'email4', self.user_collection)
        self.assertFalse(expected)

    def test_modify_user(self):
        '''Test modify user'''
        expected = users.modify_user('id1', 'namex', 'lastx', 'emailx', self.user_collection)
        self.assertTrue(expected)

    def test_modify_user_false(self):
        ''' Test modify user false'''
        expected = users.modify_user('idx', 'namex', 'lastx', 'emailx', self.user_collection)
        self.assertFalse(expected)

    def test_modify_user_len_false(self):
        ''' Test modify user false'''
        thirty = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        expected = users.modify_user('idx', thirty, 'lastx', 'emailx', self.user_collection)
        self.assertFalse(expected)

    def test_delete_user(self):
        '''Test delete user'''
        expected = users.delete_user('id1', self.user_collection, self.status_collection)
        self.assertTrue(expected)

    def test_delete_user_false(self):
        ''' Test delete user false'''
        expected = users.delete_user('idx', self.user_collection, self.status_collection)
        self.assertFalse(expected)

    def test_search_user(self):
        '''Test search user'''
        expected = users.search_user('id1', self.user_collection)
        self.assertTrue(expected)

    def test_search_user_false(self):
        ''' Test search user false'''
        expected = users.search_user('idx', self.user_collection)
        self.assertFalse(expected)


# ###############################################################################
# # user_status.py tests
# ###############################################################################

    def test_add_status(self):
        '''Test add status'''
        expected = user_status.add_status('id1',
                                          'statusx',
                                          'text1',
                                          self.status_collection,
                                          self.user_collection)
        self.assertTrue(expected)

    def test_add_status_false(self):
        ''' Test add status false'''
        expected = user_status.add_status('idx',
                                          'status1',
                                          'text1',
                                          self.status_collection,
                                          self.user_collection)
        self.assertFalse(expected)

    def test_modify_status(self):
        '''Test modify status'''
        expected = user_status.modify_status('status1',
                                             'new_text',
                                             self.status_collection)
        self.assertTrue(expected)

    def test_modify_status_false(self):
        ''' Test modify status false'''
        expected = user_status.modify_status('statusx',
                                             'text1',
                                             self.status_collection)
        self.assertFalse(expected)

    def test_delete_status(self):
        '''Test delete status'''
        expected = user_status.delete_status('status1', self.status_collection)
        self.assertTrue(expected)

    def test_delete_status_false(self):
        ''' Test delete status false'''
        expected = user_status.delete_status('statusx', self.status_collection)
        self.assertFalse(expected)

    def test_search_status(self):
        '''Test search status'''
        expected = user_status.search_status('status1', self.status_collection)
        self.assertTrue(expected)

    def test_search_status_false(self):
        ''' Test search status false'''
        expected = user_status.search_status('statusx', self.status_collection)
        self.assertFalse(expected)
