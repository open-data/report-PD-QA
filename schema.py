import json
import yaml

class Schema(object):

    schema_dir = ''

    general_schema = {}

    @classmethod
    def set_schema_dir(cls, schema_dir):
        cls.schema_dir = schema_dir

    @classmethod
    def get_schema_dir(cls):
        return cls.schema_dir

    @classmethod
    def set_general_schema(cls, file_name):

        try:
            schema_fs = open(cls.schema_dir + '/'+ file_name)
        except IOError:
            print "Error: schema file is not defined"
            raise

        completed_list = yaml.load(schema_fs)

        for dataset in completed_list:

            cls.general_schema[dataset['dataset_type']] = dataset['fields']


    @classmethod
    def get_general_schema_with_type(cls, type):
        if not cls.general_schema:
            raise ValueError("the general schema has not been configured yet")

        if not  cls.general_schema[type]:
            raise ValueError("the type does not have a schema defined")

        return cls.general_schema[type]

    @classmethod
    def get_specific_schema_with_type(cls,type):

        try:
            schema_fs = open(cls.schema_dir+'/' + type +'.yaml')
        except IOError:
            print "Error: schema file is not defined"
            raise

        schema_for_type = yaml.load(schema_fs)

        return schema_for_type[0]['fields']




