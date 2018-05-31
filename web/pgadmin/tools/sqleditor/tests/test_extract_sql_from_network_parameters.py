##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should
from werkzeug.datastructures import ImmutableMultiDict

from pgadmin.tools.sqleditor import extract_sql_from_network_parameters
from pgadmin.utils.base_test_generator import BaseTestGenerator


class TestExtractSQLFromNetworkParameters(BaseTestGenerator):
    def test_single_string_payload(self):
        """
        When the request payload is a string
        It returns the sql information but no explain plan
        """

        result = extract_sql_from_network_parameters(
            '"some sql"',
            ImmutableMultiDict(),
            ImmutableMultiDict()
        )

        result | should.be.equal(dict(sql='some sql', explain_plan=None))

    def test_json_payload(self):
        """
        When the request payload is a json
        It returns the sql information and explain plan options
        """

        result = extract_sql_from_network_parameters(
            '{"sql": "some sql", "explain_plan": '
            '{"format": "json", "analyze": false, '
            '"verbose": false, "costs": false, '
            '"buffers": false, "timing": false}}',
            ImmutableMultiDict(),
            ImmutableMultiDict()
        )

        result | should.be.equal(dict(
            sql='some sql',
            explain_plan=dict(
                format='json',
                analyze=False,
                verbose=False,
                buffers=False,
                costs=False,
                timing=False
            )
        ))
