import time
import os

from report_with_type import ReportWithType
from report_internal_error import InternalErrorReporter

class Report(object):

    def __init__(self, internal_dir, external_dir):
        today_dir = '/r_'+time.strftime('%Y_%m_%d_%H_%M_%S')
        self.internal_dir = internal_dir + today_dir
        self.external_dir = external_dir + today_dir
        os.makedirs(self.internal_dir)
        self.log_dir = self.internal_dir+'/log'
        os.makedirs(self.log_dir)
        os.makedirs(self.external_dir)

    def get_log_dir(self):
        return self.log_dir

    def init_report_for_type(self,type):
        self.report_with_type = ReportWithType(self.internal_dir, self.external_dir, type)
        self.organizations = {}
        general_row = ['organization title','number of records','errors']
        self.report_with_type.write_general_csv(general_row)

    def report_package(self, id, value, type, schema):
        self.report_with_type.write_package_json({id:value})
        title= value['organization']['title'].partition('|')[0]
        if value['organization']['id'] in self.organizations:
            InternalErrorReporter.report_error('organization ' + title +' as ' + value['organization']['id']
                              + ' in the package' + id + ' exists already' )
        else:
            self.organizations[value['organization']['id']]= dict([('organization', value['organization']['title']),
                                                                   ('packages',[])])
        #organization_id: package_id
        self.organizations[value['organization']['id']]['packages'].append(id)
        #write a line in csv first
        self.report_with_type.report_tables(id, tables = value['results'], schema = schema, title = title)
        return

    def stop_report_for_type(self):
        self.report_with_type.report_organizations(self.organizations)
        self.report_with_type.close_general_csv()
        self.report_with_type.close_package_file()
        InternalErrorReporter.close_error_file()

    #used by the unit testing defined in test_report.py
    def generate_report(self, packages, type, schema):
        self.init_report_for_type(type)
        for key, value in packages.iteritems():
            self.report_package(id=key,value=value,type=type, schema=schema)
        self.stop_report_for_type()
