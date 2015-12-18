import requests
import json
from report import Report

class PackageSearch(object):

    def __init__(self, base_url, search_url):
        self.search_url = base_url+search_url


    def get_request(self, url, params, api_key=None):
        if (api_key is None):
            r=requests.get(url, params=params)
        else:
            r=requests.get(url,params=params, headers={'Authorization':api_key})

        if (r.status_code == requests.codes.ok):
            r_json = r.json()
            return r_json
        else:
            message = 'HTTP GET ' + url + 'error with code ' + r.status_code
            print (message)
            raise Exception(message)

    def get_number(self, type):

        params = {'q':type,'rows': 1, 'start': 1}

        try:
            received=self.get_request(self.search_url, params)
        except Exception:
            raise

        if (received is None):
            print "The url for package search is wrong"
            return None

        if (received['success']):
            print received['result']
            return received['result']['count']

    def packages_with_type(self, reporter, rows = 30, start = 1, type = 'contracts'):

        packages={}

        params = {'q':type,'rows': rows, 'start': start}

        try:
            received = self.get_request(self.search_url,params)
        except Exception:
            raise

        if (received['success']=='true' or received['success']==True):
            for result in received['result']['results']:
                organization = dict([
                        ('id',result['organization']['id'].encode('utf-8')),
                        ('title', result['organization']['title'].encode('utf-8'))
                ])

                resources = []

                for resource in result['resources']:
                    resources.append(resource['id'].encode('utf-8'))

                package = dict([
                        ('organization',organization),
                        ('resources',resources)
                ])

                packages[result['id']]= package
        else:
            #write a line in the error file
            reporter.report_error('Retrieving ' + str(rows) + ' packages starting from ' + str(start)
                                  + ' fails with message as ' + received['error']['message'])

        print json.dumps(packages)

        num_of_retrieved = len(packages.keys())

        if num_of_retrieved < rows:
            reporter.report_error('Retrieved ' + str(num_of_retrieved) + ' packages from ' + str(start)
                                  + '. The number is less than that defined as ' + str(rows))

        return packages

