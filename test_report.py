import unittest
import json
from schema import Schema
from report import Report

class ReportTests(unittest.TestCase):

    def setUp(self):

        Schema.set_schema_dir('schema')

        self.schema = Schema.get_specific_schema_with_type('contracts')

        internal_dir = 'report/internal'
        external_dir = 'report/external'

        with open('data/contracts.json') as data_fs:
            self.packages = json.load(data_fs)

        self.reporter = Report(internal_dir, external_dir)


    def test_report(self):
        result = self.reporter.generate_report(self.packages, 'contracts',self.schema)


if __name__=='__main__':
    unittest.main()










