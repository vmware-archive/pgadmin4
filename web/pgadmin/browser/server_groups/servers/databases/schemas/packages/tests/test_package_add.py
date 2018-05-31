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

from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils import server_utils as server_utils
from pgadmin.utils.base_test_generator import BaseTestGenerator
from pgadmin.utils.tests_helper import convert_response_to_json, \
    assert_json_values_from_response
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils


@pytest.mark.skip_databases(['gpdb', 'pg'])
class TestPackageAdd:
    @pytest.mark.usefixtures('require_database_connection')
    def test_package_add(self, context_of_tests):
        """
        When the package add request is send to the backend
        it returns 200 status
        """
        url = '/browser/package/obj/'

        tester = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        db_name = server_data['db_name']

        schema_name = server_data['schema_name']
        schema_id = server_data['schema_id']

        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        package_name = "pkg_%s" % str(uuid.uuid4())[1:8]
        data = \
            {
                "name": package_name,
                "owner": server["username"],
                "pkgacl": [],
                "pkgbodysrc": "PROCEDURE p1() is \n"
                              "begin \n"
                              "dbms_output.put_line('Test_pkg.Proc...'); "
                              "\nEND\t;",
                "pkgheadsrc": "PROCEDURE p1();",
                "schema": schema_id
            }

        response = tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(server_id) + '/' +
            str(db_id) + '/' +
            str(schema_id) + '/',
            data=json.dumps(data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        assert_json_values_from_response(
            json_response,
            'package',
            'pgadmin.node.package',
            False,
            'icon-package',
            package_name
        )
