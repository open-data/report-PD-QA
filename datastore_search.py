from package_search import PackageSearch
from report_internal_error import InternalErrorReporter

class DatastoreSearch(PackageSearch):

    def __init__(self, base_url, search_url):
        super(DatastoreSearch, self).__init__(base_url, search_url)

    def tables_in_resources(self, resources, api_key, package):

        tables={}

        for resource in resources:

            params={"resource_id":resource}

            try:
                result = self.get_request(self.search_url,params,api_key)
            except Exception as e:
                tables[resource]=dict([('HTTP_status', 'error'),
                                    ('HTTP_message', str(e))])
                continue

            if result['success'] == 'true' or result['success'] == True:
                tables[resource]=dict([('HTTP_status', 'success'),
                                    ('HTTP_message', 'request success'),
                                    ('resource_status', 'success'),
                                    ('records', result['result']['records'])])
            else:
                InternalErrorReporter.report_error('Retrieving the resources of package ' + package + ' fails with message as '
                                          + result['error']['message'])
                tables[resource]=dict([('HTTP_status', 'success'),
                                    ('HTTP_message', 'request success'),
                                    ('resource_status', 'fail'),
                                    ('resource_message', result['error']['message'])
                                    ])

        return tables
