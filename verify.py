from schema import Schema
from data_validator import Data_Validator
import json

def experiemnt():
    raise Exception('HTTP GET http://registry.statcan.gc.ca/api/action/datastore_search error with code 404')

def main():
    Schema.set_schema_dir('schema')

    data_validator = Data_Validator("contracts")
    record = {
          "comments_en": "For a contract with task authorizations, the realized amount of the contract is contingent on the number of task authorizations issued and may be less than the amount proactively disclosed, dependent on the operational requirements of the department.",
          "intellectual_property_code": "",
          "potential_commercial_exploitation": "",
          "limited_tendering_reason_code": "",
          "description_fr": "672 ",
          "agreement_type_code": "",
          "country_of_origin": "",
          "standing_offer_number": "",
          "original_value": "",
          "aboriginal_business": "",
          "contract_date": "2014-01-01",
          "additional_comments_fr": "",
          "derogation_code": "",
          "former_public_servant": "",
          "contract_value": "33380339.31",
          "document_type_code": "",
          "standing_offer": "",
          "contract_period_start": "2014-01-01",
          "reporting_period": "",
          "amendment_value": "",
          "description_en": "672 - Computer Equipment - Servers",
          "commodity_code": "",
          "commodity_type_code": "",
          "comments_fr": "Pour",
          "_id": 1,
          "ref_number": "700280890",
          "solicitation_procedure_code": "",
          "additional_comments_en": "",
          "vendor_name": "HEWLETT-PACKARD (CANADA) CO.",
          "delivery_date": "2016-03-31"
        }

    record['contract_value'] = '3000'
    #result = data_validator.validate(record)
    #print "results" + json.dumps(result)
    try:
        experiemnt()
    except Exception as e:
        a = str(e)
        print 'error '+ a



if __name__ == '__main__':
    main()
