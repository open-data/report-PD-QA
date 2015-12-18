import time
import re
import json
from schema import Schema

class Rule(object):

    def __init__(self, defined):

        if 'field name' in defined:
            self.field_name = defined['field name']
        else:
            self.field_name = None

        self.operation = defined['rule'][0]
        self.operator = defined['rule'][1]

        if len(defined['rule'])>2 :
            self.operand = defined['rule'][2]
        else:
            self.operand = ''

        self.jsonfiles={}

    def get_field_name(self):
        return self.field_name

    def validate(self, field_value):

        #uni-operation

        if self.operation == 'length':
            return eval('len(field_value)' + self.operator + self.operand)

        if self.operation == 'date':
            try:
                time.strptime(field_value, self.operator)
                return True
            except ValueError:
                return False

        if self.operation == 'match' :
            self.operator = '^' + self.operator + '$'
            match = re.match(self.operator, field_value)
            if match:
                return True
            else:
                return False

        if self.operation == 'string':
            return eval('field_value ' + self.operator + '\'' + self.operand + '\'')

        if self.operation == 'value':
            value = 0
            if field_value:
                value = float(field_value)
            return eval('value ' + self.operator + self.operand)

        if self.operation == 'array':

            operand_array = []

            jsonfile = re.search('jsonl', self.operand)

            if not jsonfile:
                operand_array = self.operand.split(',')

            else:
                #retrieve the array from the jsonl file
                if self.operand in self.jsonfiles :
                    operand_array = self.jsonfiles[self.operand]
                else:
                    try:
                        for line in open(Schema.get_schema_dir() + '/' + self.operand):
                            code_line = json.loads(line)
                            operand_array.append(code_line['id'])
                    except IOError:
                        raise

                    self.jsonfiles[self.operand] = operand_array

            return field_value in operand_array

        if self.operation == 'period':

            if '-' not in field_value:
                return False

            points = field_value.split('-')

            operand_array = self.operand.split('-')

            if len(points) < 3:
                return False

            for index in range(0,2):
                try:
                    time.strptime(points[index], operand_array[index])
                except ValueError:
                    return False

            operand_array[2] = '^' + operand_array[2] + '$'

            match = re.match(operand_array[2], points[2])

            if not match:
                return False

            return True









