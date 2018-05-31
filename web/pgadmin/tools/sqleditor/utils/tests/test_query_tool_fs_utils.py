##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import os

from grappa import should

from pgadmin.tools.sqleditor.utils.query_tool_fs_utils import \
    read_file_generator


class TestReadFileGeneratorForEncoding:
    def test_load_utf8_encoding(self):
        """
        When a user is trying to load the file with utf-8 encoding
        It returns 'SELECT 1'
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        complete_path = os.path.join(dir_path, 'test_file_utf8_encoding.sql')
        result = read_file_generator(complete_path, 'utf-8')
        next(result) | should.be.contain('SELECT 1')

    def test_load_other_encoding(self):
        """
        When user is trying to load the file with other encoding
        And trying to use utf-8 encoding to read it
        It returns 'SELECT 1'
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        complete_path = os.path.join(dir_path, 'test_file_other_encoding.sql')
        result = read_file_generator(complete_path, 'utf-8')
        next(result) | should.be.contain('SELECT 1')
