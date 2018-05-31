##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import print_function

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.tests_helper import ClientTestBaseClass
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as cast_utils


@pytest.mark.skip_databases(['gpdb'])
class TestCastsGet(ClientTestBaseClass):
    @pytest.fixture(autouse=True)
    def setUp(self, the_real_setup):
        """ This function will create cast."""
        self.default_db = self.server["db"]
        self.database_info = parent_node_dict['database'][-1]
        self.db_name = self.database_info['db_name']
        self.server["db"] = self.db_name
        self.source_type = 'money'
        self.target_type = 'bigint'
        self.cast_id = cast_utils.create_cast(self.server, self.source_type,
                                              self.target_type)

    def test_get_cast_node(self):
        """When a cast exits
         When GET request is sent to the backend,
         It retrieves the information about it
          And return 200 status"""
        url = '/browser/cast/obj/'
        self.server_id = self.database_info["server_id"]
        self.db_id = self.database_info['db_id']
        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")
        response = self.tester.get(
            url + str(utils.SERVER_GROUP) + '/' + str(
                self.server_id) + '/' +
            str(self.db_id) + '/' + str(self.cast_id),
            content_type='html/json')
        response.status_code | should.be.equal.to(200)
        json_response = self.response_to_json(response)
        (json_response | should.have.key('pronspname') >
         should.be.equal.to(None))
        (json_response | should.have.key('srcnspname') >
         should.be.equal.to('pg_catalog'))
        (json_response | should.have.key('trgnspname') >
         should.be.equal.to('pg_catalog'))
        (json_response | should.have.key('description') >
         should.be.equal.to(None))
        (json_response | should.have.key('proname') >
         should.be.equal.to('binary compatible'))
        (json_response | should.have.key('syscast') >
         should.be.equal.to(False))
        (json_response | should.have.key('trgtyp') >
         should.be.equal.to('bigint'))
        (json_response | should.have.key('castfunc') >
         should.be.equal.to(0))
        (json_response | should.have.key('castcontext') >
         should.be.equal.to('IMPLICIT'))
        (json_response | should.have.key('srctyp') >
         should.be.equal.to('money'))
        (json_response | should.have.key('name') >
         should.be.equal.to('money->bigint'))

    def tearDown(self):
        """This function disconnect the test database and drop added cast."""
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        cast_utils.drop_cast(connection, self.source_type,
                             self.target_type)
        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
        self.server['db'] = self.default_db
