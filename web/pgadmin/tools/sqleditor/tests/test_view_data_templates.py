##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os
import re

from flask import Flask, render_template
from grappa import should
from jinja2 import FileSystemLoader

from config import PG_DEFAULT_DRIVER
from pgadmin.utils.driver import get_driver

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class TestViewDataTemplates:
    def test_insert_with_only_pk(self):
        """
        When Inserting table data with only Primary Key
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/insert.sql',
                                     data_to_be_saved=data_to_be_saved,
                                     primary_keys=None,
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     data_type={'text': 'text',
                                                'id': 'integer'},
                                     pk_names='id',
                                     has_oids=False)

            str(result).replace("\n", "") | should.be.equal(
                'INSERT INTO test_schema.test_table (id, text) VALUES'
                ' (%(id)s::integer, %(text)s::text) returning id;'
                .replace("\n", ""))

    def test_insert_with_multiple_pk(self):
        """
        When Inserting table data with multiple Primary Keys
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/insert.sql',
                                     data_to_be_saved=data_to_be_saved,
                                     primary_keys=None,
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     data_type={'text': 'text',
                                                'id': 'integer'},
                                     pk_names='id, text',
                                     has_oids=False)

            str(result).replace("\n", "") | should.be.equal(
                'INSERT INTO test_schema.test_table (id, text) VALUES'
                ' (%(id)s::integer, %(text)s::text) returning id, text;'
                .replace("\n", ""))

    def test_insert_with_one_pk_and_oid(self):
        """
        When Inserting table data with one Primary Key and OID
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/insert.sql',
                                     data_to_be_saved=data_to_be_saved,
                                     primary_keys=None,
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     data_type={'text': 'text',
                                                'id': 'integer'},
                                     pk_names='id',
                                     has_oids=True)

            str(result).replace("\n", "") | should.be.equal(
                'INSERT INTO test_schema.test_table (id, text) VALUES'
                ' (%(id)s::integer, %(text)s::text) returning oid;'
                .replace("\n", ""))

    def test_insert_with_only_oid(self):
        """
        When Inserting table data with OID
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/insert.sql',
                                     data_to_be_saved=data_to_be_saved,
                                     primary_keys=None,
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     data_type={'text': 'text',
                                                'id': 'integer'},
                                     pk_names='id',
                                     has_oids=True)

            str(result).replace("\n", "") | should.be.equal(
                'INSERT INTO test_schema.test_table (id, text) VALUES'
                ' (%(id)s::integer, %(text)s::text) returning oid;'
                .replace("\n", ""))

    def test_select_only_pk(self):
        """
        When Selecting table data with only Primary Key
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/select.sql',
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     primary_keys=OrderedDict(
                                         [('id', 'int4')]),
                                     has_oids=False)
            re.sub(' +', ' ', str(result).replace("\n", " ")) | should.be \
                .equal(
                """ SELECT * FROM test_schema.test_table WHERE id = %(id)s ;"""
            )

    def test_select_with_multiple_pk(self):
        """
        When Selecting table data with multiple Primary Keys
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/select.sql',
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     primary_keys=OrderedDict(
                                         [('id', 'int4'),
                                          ('text', 'text')]),
                                     has_oids=False)
            re.sub(' +', ' ', str(result).replace("\n", " ")) | should.be \
                .equal(
                """ SELECT * FROM test_schema.test_table """ +
                """WHERE id = %(id)s AND text = %(text)s ;"""
            )

    def test_select_with_one_pk_and_oid(self):
        """
        When Selecting table data with one Primary Key and OID
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/select.sql',
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     primary_keys=OrderedDict(
                                         [('id', 'int4')]),
                                     has_oids=True)
            re.sub(' +', ' ', str(result).replace("\n", " ")) | should.be \
                .equal(
                """ SELECT oid, * FROM test_schema.test_table """ +
                """WHERE oid = %(oid)s ;"""
            )

    def test_select_with_only_oid(self):
        """
        When Selecting table data with OID
        It returns the correct SQL
        """
        data_to_be_saved = OrderedDict()
        data_to_be_saved['id'] = '1'
        data_to_be_saved['text'] = 'just test'
        with FakeApp().app_context():
            result = render_template('sqleditor/sql/default/select.sql',
                                     object_name='test_table',
                                     nsp_name='test_schema',
                                     primary_keys=OrderedDict(
                                         [('id', 'int4')]),
                                     has_oids=True)
            re.sub(' +', ' ', str(result).replace("\n", " ")) | should.be \
                .equal(
                """ SELECT oid, * FROM test_schema.test_table WHERE """ +
                """oid = %(oid)s ;"""
            )


class FakeApp(Flask):
    def __init__(self):
        super(FakeApp, self).__init__("")
        driver = get_driver(PG_DEFAULT_DRIVER, self)
        self.jinja_env.filters['qtLiteral'] = driver.qtLiteral
        self.jinja_env.filters['qtIdent'] = driver.qtIdent
        self.jinja_env.filters['qtTypeIdent'] = driver.qtTypeIdent
        self.jinja_loader = FileSystemLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                'templates'
            )
        )
