
import json
import logging
from report import Report
from schema import Schema
from data_validator import Data_Validator
from package_search import PackageSearch
from datastore_search import DataStoreSearch

REPORT_DIR ='report'
ENV_FILE = 'env.json'
REGISTRY_BASE_URL='http://registry.statcan.gc.ca/api/action/'
PACKAGE_SEARCH='package_search'
DATASTORE_SEARCH='datastore_search'
env={}

def perform_validation(tables, data_validator):

    for key, entry in tables.iteritems():

        if (entry['HTTP_status'] == 'error'):
            break

        records_detail=[]

        if len(entry['records'])!=0:
            #validate each record
            print "orignial records: " + json.dumps(entry['records'])

            for record in entry['records']:

                #verify the case that a field in the schema is not in the record
                records_detail.append(data_validator.validate(record))

            print json.dumps(records_detail)

            result= dict([
                ('records_status', 'validated'),
                ('records_message', str(len(entry['records'])) + ' records'),
                ('records_detail', records_detail)])

        else:
            result = dict([('records_status', 'error'),
            ('records_message', 'no record')])

        entry['result']=result

        del entry['records']

    return

def config_env():
    global env
    # read the env.json file
    try:
        file_stream = open(ENV_FILE)
        env = json.load(file_stream)
        file_stream.close()
    except IOError:
        print "Error: env.json file is not defined"
        return

    if 'api_key' not in env:
        print "api_key should be defined"

    if 'types' not in env:
        print "types are as contracts"
        env['types']=[]
        env['types'].append("contracts")

    print 'your key is ' + env['api_key']

    if 'schema_directory' not in env:
        env['schema_directory'] = 'schema'

    if 'schema_file' not in env:
        env['schema_file'] = 'recombinant_tables.yaml'

    print 'Default environment:' + json.dumps(env)

    if 'internal_report_dir' not in env:
        env['internal_report_dir']='internal_report'

    if 'external_report_dir' not in env:
        env['external_report_dir']='external_report'

    return

def main():

    global env

    config_env()

    Schema.set_schema_dir(env['schema_directory'])
    Schema.set_general_schema(env['schema_file'])

    #create report directory and structure

    reporter = Report(env['internal_report_dir'], env['external_report_dir'])

    log_dir = reporter.get_log_dir()

    logging.basicConfig(filename=log_dir+'/validation.log', level=logging.DEBUG)

    package_search = PackageSearch(REGISTRY_BASE_URL, PACKAGE_SEARCH)
    datastore_search = DataStoreSearch(REGISTRY_BASE_URL,DATASTORE_SEARCH)

    rows = 30

    for type in env['types']:

        # retrieve the information of tables in registry using package_search api
        num_of_retrieval = package_search.get_number(type)//rows + 1

        data_validator = Data_Validator(type)
        start = 1

        reporter.init_report_for_type(type)

        for iteration in range(0,num_of_retrieval):

            try:
                packages = package_search.packages_with_type(type = type,rows= 30, start = start)
            except Exception:
                print (Exception.message)
                continue
            # validate each dataset
            for key,value in packages.iteritems():

                tables = datastore_search.tables_in_resources(value['resources'],env['api_key'])

                perform_validation(tables, data_validator)

                packages[key]['results'] = tables

                reporter.report_package(id=key, value=packages[key],type=type, schema=data_validator.get_schema())

            start +=rows

        reporter.stop_report_for_type()
    return

if __name__=='__main__':
    main()
