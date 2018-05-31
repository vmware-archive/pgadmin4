##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should

from pgadmin.browser.server_groups.servers.databases \
    .external_tables.mapping_utils import \
    map_column_from_database, map_table_information_from_database, \
    is_web_table, format_options, map_execution_location, map_format_type


class TestMappingUtils(object):
    def test_map_column_from_database(self):
        """
        When retrieving columns from table
        It returns only the name and type
        """
        result = map_column_from_database(
            column_information=dict(
                name='some name',
                cltype='some type',
                other_column='some other column'
            )
        )

        result | should.be.equal.to(dict(name='some name', type='some type'))

    def test_map_table_information_from_database_using_uri(self):
        """
        When retrieving information from web table using uri
        It returns all fields
        """
        result = map_table_information_from_database(
            table_information=dict(
                urilocation='{http://someurl.com}',
                execlocation=['ALL_SEGMENTS'],
                fmttype='b',
                fmtopts='delimiter \',\' null \'\' escape \'"\' quote \'"\'',
                command=None,
                rejectlimit=None,
                rejectlimittype=None,
                errtblname=None,
                errortofile=None,
                pg_encoding_to_char='UTF8',
                writable=False,
                options=None,
                distribution=None,
                name='some_table_name',
                namespace='some_name_space'
            )
        )

        result | should.be.equal.to(dict(
            uris=['http://someurl.com'],
            isWeb=True,
            executionLocation=dict(type='all_segments', value=None),
            formatType='custom',
            formatOptions='delimiter = $$,$$,escape = $$"$$,'
                          'null = $$$$,quote = $$"$$',
            command=None,
            rejectLimit=None,
            rejectLimitType=None,
            errorTableName=None,
            erroToFile=None,
            pgEncodingToChar='UTF8',
            writable=False,
            options=None,
            distribution=None,
            name='some_table_name',
            namespace='some_name_space'
        ))

    def test_map_table_information_from_database_using_cmd(self):
        """
        When retrieving information from web table using cmd
        It returns all fields
        """
        result = map_table_information_from_database(
            table_information=dict(
                urilocation=None,
                execlocation=['ALL_SEGMENTS'],
                fmttype='b',
                fmtopts='delimiter \',\' null \'\' escape \'"\' quote \'"\'',
                command='cat /tmp/places || echo \'error\'',
                rejectlimit=None,
                rejectlimittype=None,
                errtblname=None,
                errortofile=None,
                pg_encoding_to_char='UTF8',
                writable=False,
                options=None,
                distribution=None,
                name='some_table_name',
                namespace='some_name_space'
            )
        )

        result | should.be.equal.to(dict(
            uris=None,
            isWeb=True,
            executionLocation=dict(type='all_segments', value=None),
            formatType='custom',
            formatOptions='delimiter = $$,$$,escape = $$"$$,'
                          'null = $$$$,quote = $$"$$',
            command='cat /tmp/places || echo \'error\'',
            rejectLimit=None,
            rejectLimitType=None,
            errorTableName=None,
            erroToFile=None,
            pgEncodingToChar='UTF8',
            writable=False,
            options=None,
            distribution=None,
            name='some_table_name',
            namespace='some_name_space'
        ))

    def test_map_table_information_from_none_web_table(self):
        """
        When retrieving information from none web table
        It returns all fields
        """
        result = map_table_information_from_database(
            table_information=dict(
                urilocation='{gpfdist://filehost:8081/*.csv}',
                execlocation=['ALL_SEGMENTS'],
                fmttype='b',
                fmtopts='delimiter \',\' null \'\' escape \'"\' quote \'"\'',
                command=None,
                rejectlimit=None,
                rejectlimittype=None,
                errtblname=None,
                errortofile=None,
                pg_encoding_to_char='UTF8',
                writable=False,
                options=None,
                distribution=None,
                name='some_table_name',
                namespace='some_name_space'
            )
        )

        result | should.be.equal.to(dict(
            uris=['gpfdist://filehost:8081/*.csv'],
            isWeb=False,
            executionLocation=dict(type='all_segments', value=None),
            formatType='custom',
            formatOptions='delimiter = $$,$$,escape = $$"$$,'
                          'null = $$$$,quote = $$"$$',
            command=None,
            rejectLimit=None,
            rejectLimitType=None,
            errorTableName=None,
            erroToFile=None,
            pgEncodingToChar='UTF8',
            writable=False,
            options=None,
            distribution=None,
            name='some_table_name',
            namespace='some_name_space'
        ))

    def test_is_web_table_with_http(self):
        """
        When url starts with http
        And command is None
        It returns true
        """
        result = is_web_table(
            uris='{http://someurl.com}',
            command=None
        )

        result | should.be.true

    def test_is_web_table_with_https(self):
        """
        When url starts with https
        And command is None
        It returns true
        """
        result = is_web_table(
            uris='{https://someurl.com}',
            command=None
        )

        result | should.be.true

    def test_is_web_table_with_s3(self):
        """
        When url starts with s3
        And command is None
        It returns false
        """
        result = is_web_table(
            uris='{s3://someurl.com}',
            command=None
        )

        result | should.be.false

    def test_is_web_table_with_command_no_url(self):
        """
        When url is None
        And command is not none
        It returns true
        """
        result = is_web_table(
            uris=None,
            command='Some command'
        )

        result | should.be.true

    def test_map_execution_location_with_host(self):
        """
        When value is "HOST: 1.1.1.1",
        It returns {type: "host", value: "1.1.1.1"}'
        """
        result = map_execution_location(
            execution_location=['HOST: 1.1.1.1']
        )

        result | should.be.equal.to(dict(type='host', value='1.1.1.1'))

    def test_map_execution_location_per_host(self):
        """
        When value is "PER_HOST",
        It returns {type: "per_host", value: None"}'
        """
        result = map_execution_location(
            execution_location=['PER_HOST']
        )

        result | should.be.equal.to(dict(type='per_host', value=None))

    def test_map_execution_location_master(self):
        """
        When value is "MASTER_ONLY",
        It returns {type: "master_only", value: None"}'
        """
        result = map_execution_location(
            execution_location=['MASTER_ONLY']
        )

        result | should.be.equal.to(dict(type='master_only', value=None))

    def test_map_execution_location_segment_id(self):
        """
        When value is "SEGMENT_ID: 1234",
        It returns {type: "segment", value: 1234"}'
        """
        result = map_execution_location(
            execution_location=['SEGMENT_ID: 1234']
        )

        result | should.be.equal.to(dict(type='segment', value='1234'))

    def test_map_execution_location_total_segs(self):
        """
        When value is "TOTAL_SEGS: 4",
        It returns {type: "segments", value: 4"}'
        """
        result = map_execution_location(
            execution_location=['TOTAL_SEGS: 4']
        )

        result | should.be.equal.to(dict(type='segments', value='4'))

    def test_map_execution_location_all_segments(self):
        """
        When value is "ALL_SEGMENTS",
        It returns {type: "all_segments", value: None"}'
        """
        result = map_execution_location(
            execution_location=['ALL_SEGMENTS']
        )

        result | should.be.equal.to(dict(type='all_segments', value=None))

    def test_map_format_type_with_c(self):
        """
        When value is "c",
        It returns csv
        """
        result = map_format_type(format_type='c')

        result | should.be.equal.to('csv')

    def test_map_format_type_with_unexpected_value(self):
        """
        When value is "unexpected value",
        It returns csv
        """
        result = map_format_type(format_type='something strange')

        result | should.be.equal.to('csv')

    def test_map_format_type_with_b(self):
        """
        When value is "b",
        It returns custom
        """
        result = map_format_type(format_type='b')

        result | should.be.equal.to('custom')

    def test_map_format_type_with_a(self):
        """
        When value is "a",
        It returns avro
        """
        result = map_format_type(format_type='a')

        result | should.be.equal.to('avro')

    def test_map_format_type_with_p(self):
        """
        When value is "p",
        It returns parquet
        """
        result = map_format_type(format_type='p')

        result | should.be.equal.to('parquet')

    def test_format_options_with_none(self):
        """
        When passing None
        It returns None
        """
        result = format_options(format_type='avro', options=None)

        result | should.be.none

    def test_format_options_with_empty_string(self):
        """
        When passing empty string
        It returns empty string
        """
        result = format_options(format_type='parquet', options='')

        result | should.be.equal.to('')

    def test_format_options_with_formatter_fixedwidth(self):
        """
        When passing option 'fixedwidth_in' null ' '
        It returns "formatter = $$fixedwidth_in$$,null = $$ $$"
        """
        result = format_options(
            format_type='custom',
            options="formatter 'fixedwidth_in' null ' '"
        )

        result | \
            should.be.equal.to('formatter = $$fixedwidth_in$$,null = $$ $$')

    def test_format_options_with_formatter_fixedwidth_comma(self):
        """
        When passing option 'fixedwidth_in' comma ''' null ' '
        It returns "formatter = $$fixedwidth_in$$,comma = $$\'$$,null = $$ $$"
        """
        result = format_options(
            format_type='custom',
            options="formatter 'fixedwidth_in' comma ''' null ' '"
        )

        result | should.be.equal.to(
            "comma = $$'$$,"
            "formatter = $$fixedwidth_in$$,"
            "null = $$ $$"
        )

    def test_format_options_with_formatter_preserve_blanks(self):
        """
        When passing option 'fixedwidth_in' null ' ' preserve_blanks
        'on' comma '\''
        It returns "formatter = $$fixedwidth_in$$,
        null = $$ $$,preserve_blanks = $$on$$,comma = $$'$$"'
        """
        result = format_options(
            format_type='custom',
            options="formatter 'fixedwidth_in' "
                    "null ' ' "
                    "preserve_blanks 'on' "
                    "comma '''"
        )

        result | should.be.equal.to(
            "comma = $$'$$,formatter = $$fixedwidth_in$$,"
            "null = $$ $$,"
            "preserve_blanks = $$on$$"
        )

    def test_format_options_with_text(self):
        """
        When passing format type is text
        it returns escaped string
        """
        result = format_options(
            format_type='text',
            options="something 'strange' other '''"
        )

        result | should.be.equal.to(
            "other $$'$$ something $$strange$$"
        )

    def test_format_options_with_csv(self):
        """
        When passing format type is csv
        it returns escaped string
        """
        result = format_options(
            format_type='csv',
            options="something 'strange' other '''"
        )

        result | should.be.equal.to("other $$'$$ something $$strange$$")
