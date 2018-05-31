##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

import pytest
from grappa import should

from pgadmin.utils.base_test_generator import BaseTestGenerator, \
    PostgresVersion
from regression.python_test_utils import test_utils as utils
from . import utils as resource_groups_utils


@pytest.mark.skip_databases(['pg'])
@pytest.mark.skip_if_postgres_version({'below_version': PostgresVersion.v94},
                                      'Resource groups are not supported '
                                      'by PG9.3 '
                                      'and PPAS9.3 and below.')
class TestResourceGroupsAdd(BaseTestGenerator):
    def test_add_new_resource_group(self, request, context_of_tests):
        """
        When request to add a resource group is valid
        It returns success
        """
        request.addfinalizer(self.tearDown)

        url = '/browser/resource_group/obj/'
        server_info = context_of_tests["server_information"]
        server_id = server_info["server_id"]

        http_client = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.resource_group = "test_resource_group_add%s" % \
                              str(uuid.uuid4())[1:8]
        data = {"name": self.resource_group,
                "cpu_rate_limit": 0,
                "dirty_rate_limit": 0}

        response = http_client.post(url + str(utils.SERVER_GROUP) +
                                    "/" + str(server_id) + "/",
                                    data=json.dumps(data),
                                    content_type='html/json')

        response.status_code | should.be.equal(200)

    def tearDown(self):
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        resource_groups_utils.delete_resource_group(connection,
                                                    self.resource_group)
