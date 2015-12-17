import json
import time
import os
import csv
import logging

from report_with_type import ReportWithType

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

    def close_package_file(self):
        self.package_fs.close()

    def init_report_for_type(self,type):
        self.report_with_type = ReportWithType(self.internal_dir, self.external_dir, type)
        self.organizations = []
        general_row = ['organization title','number of records','errors']
        self.report_with_type.write_general_csv(general_row)

    def report_package(self, id, value, type, schema):

        self.report_with_type.write_package_json({id:value})

        title= value['organization']['title'].partition('|')[0]

        if value['organization']['id'] in self.organizations:
            print "organization exists already" + title +' ' + value['organization']['id']
            return

        self.organizations.append(value['organization']['id'])

        #write a line in csv first
        self.report_with_type.report_tables(id, tables = value['results'], schema = schema, title = title)

        return

    def stop_report_for_type(self):

        self.report_with_type.close_general_csv()

        self.report_with_type.close_package_file()

    def generate_report(self, packages, type, schema):

        self.init_report_for_type(type)

        for key, value in packages.iteritems():
            self.report_package(id=key,value=value,type=type, schema=schema)

        self.stop_report_for_type()

