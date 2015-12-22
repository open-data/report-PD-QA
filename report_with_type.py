import os
import csv
import json
from report_internal_error import InternalErrorReporter

class ReportWithType(object):

    def __init__(self, internal_dir, external_dir, type):

        self.internal_dir = internal_dir + '/' + type
        os.makedirs(self.internal_dir)
        self.external_dir = external_dir + '/' + type
        os.makedirs(self.external_dir)
        InternalErrorReporter.setup(self.internal_dir)

        try:
            self.package_fs= open(self.internal_dir + '/'+ type +'.jsonl', 'w')
            self.general_csv_fs= open(self.external_dir +'/' + type + '_general.csv', 'wb')
            self.general_csv_writer = csv.writer(self.general_csv_fs, delimiter=',')
        except IOError:
            print 'file open error'
            raise

    def write_general_csv(self, row):
        self.general_csv_writer.writerow(row)

    def write_package_json(self, record):
        line = json.dumps(record)
        self.package_fs.write(line + '\n')

    def close_general_csv(self):
        self.general_csv_fs.close()

    def close_package_file(self):
        self.package_fs.close()

    def report_tables(self, package_id, tables, title, schema):

        for table_k, table_v in tables.iteritems():

            if (table_v['HTTP_status'] != 'success'):
                InternalErrorReporter.report_error("http_error: " + title + ' with package id as ' + package_id
                      + ' has ' + table_v['HTTP_message']
                      + ' with resource id as ' + table_k)
                continue

            result = table_v['result']

            general_row = [title, result['records_message']]

            if (result['records_status']=='validated'):
                #write to the department csv file
                department_csv_file = self.external_dir + '/'+ title+'.csv'
                try:
                    department_csv_fs = open(department_csv_file, 'wb')
                    department_csv_writer = csv.writer(department_csv_fs, delimiter=',')
                    department_error_fs = open(self.external_dir+ '/' +title + 'error.txt','w')
                except IOError:
                    print "file open error " + department_csv_file
                    continue

                # the header is the labeld of the fields contained in the schema
                # one row for one record
                header_row=[]

                department_error = {}

                for column in schema:
                    header_row.append(column['label'].encode('utf-8'))
                    department_error[column['datastore_id']] = {}

                department_csv_writer.writerow(header_row)

                print "records: " + json.dumps(result['records_detail'])

                for record in result['records_detail']:

                    department_row = []

                    department_row.append(record['Reference Number Key'])

                    column_index = 0

                    for column in schema:
                        column_key = column['datastore_id']

                        if column_key not in record:
                            print('the column '+ column_key + ' is not exist in record')
                            continue

                        if record[column_key]['status']== 'fail':
                            case = record[column_key]['case']
                            if case not in department_error[column_key]:
                                department_error[column_key][case] = []
                            department_error[column_key][case].append(record['Reference Number Key'])
                            department_row.append(column['validation errors'][case]['type'])
                        else:
                            department_row.append(record[column_key]['status'])
                        column_index += 1
                    department_csv_writer.writerow(department_row)

                department_csv_fs.close()
                self.write_error(department_error_fs, department_error,schema, general_row)
                department_error_fs.close()
            self.write_general_csv(general_row)

    def write_error(self, department_error_fs, department_error, schema, general_row):
        for column in schema:
            column_key = column['datastore_id']
            if department_error[column_key]:
               for error_key, error_rows in department_error[column_key].iteritems():
                   msg = column['validation errors'][error_key]
                   row = json.dumps(error_rows)
                   error_msg = msg['msg'][0].encode('utf-8') + row + msg['msg'][1].encode('utf-8')
                   department_error_fs.write(error_msg+'\n\n')
                   general_line = column['label'].encode('utf-8') + ' has ' + str(len(error_rows)) + ' records with ' + msg['type'].encode('utf-8')
                   general_row.append(general_line)

    def report_organizations(self, organizations):
        try:
            with open(self.internal_dir + '/organization.json', 'w') as org_fs:
                json.dump(organizations,org_fs)
        except IOError:
            raise

    def get_internal_dir(self):
        return self.internal_dir

