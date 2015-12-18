from rule import Rule
from schema import Schema

class Data_Validator(object):

    """
    This is the definition of the class for validating the data stored in an array
    """
    def __init__(self,type):

        self.schema = Schema.get_specific_schema_with_type(type)

    def get_schema(self):
        return self.schema

    def validate(self, record):

        """
        :param record:
        :return: a list of validation_information
        """
        results = {}

        for column in self.schema:
            self.validate_column(record=record, results=results, column=column)

        return results

    def validate_column(self, record, results, column):

        column_key = column['datastore_id']

        if column_key in results:
            return

        result = {'status' : 'pass'}

        if column_key not in record:
            result = { 'status': 'fail',
                        'error':{
                                'not exist':{
                                 'type': 'Field does not exist',
                                 'msg': 'Field does not exist for row X,X,X'
                                 } } }
            results[column_key]=result
            return

        if  not column['validation']:
            results[column_key]=result
            return

        for case_index, case in enumerate(column['validation']):

            (case_key, case_value) = case.items()[0]

            field_rule =  column['business rules'][case_value]

            if 'proposition' in field_rule:
                if self.proposition_validation(rule_definition=field_rule['proposition'],
                                               record=record, column=column, results=results) != True :
                    result['status'] = 'fail'

            if 'antecedent' in field_rule:
                antecedent_valid = True

                for antecedent in field_rule['antecedent']:
                    antecedent_valid= self.proposition_validation(rule_definition=antecedent, record=record, results = results, column=column)
                    if antecedent_valid != True:
                        break

                if antecedent_valid == True:
                    if self.proposition_validation(rule_definition=field_rule['consequent'],
                                                   record=record, results=results, column=column) != True :
                        result['status'] = 'fail'

                if antecedent_valid == 'unknown':
                    result['status'] = 'unknown'
                    break

            if result['status'] == 'fail':
                result['case'] = case_key
                break

        results[column_key]=result

        return

    def find_column_with_field_name(self, searched_name):

        find_column = None

        for column in self.schema:
            if column['datastore_id'] == searched_name:
                find_column = column
                break

        return find_column


    def proposition_validation(self, rule_definition, column, record, results):

        column_key = column['datastore_id']

        rule = Rule(rule_definition)

        field_name = rule.get_field_name()

        if field_name == None:
            field_name = column_key
        else:
            #find the column with datastore_id == field_name
            condition_column = self.find_column_with_field_name(field_name)
            if not condition_column:
                return 'unknown'

            self.validate_column(column=condition_column, record=record, results=results)

            if results[field_name]['status'] != 'pass':
                return 'unknown'

        return rule.validate(record[field_name])











