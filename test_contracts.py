import unittest
import json
from data_validator import DataValidator
from schema import Schema

class ValidationTests(unittest.TestCase):

    def setUp(self):

        Schema.set_schema_dir('schema')

        self.data_validator = DataValidator("contracts")
        self.record = {
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


    def test_ref_num(self):

        result = self.data_validator.validate(self.record)
        print 'result ' + json.dumps(result)
        self.assertEqual(result['ref_number']['status'], 'pass')

        self.record['ref_number']=''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['ref_number']['status'], 'fail')
        self.assertEqual(result['ref_number']['case'], 'not empty')


    def test_vendor_name(self):

        result = self.data_validator.validate(self.record)
        self.assertEqual(result['vendor_name']['status'], 'pass')

        self.record['vendor_name'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['vendor_name']['status'], 'fail')
        self.assertEqual(result['vendor_name']['case'],'not empty')



    def test_contract_date(self):

        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_date']['status'], 'pass')

        self.record['contract_date'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_date']['status'], 'fail')
        self.assertEqual(result['contract_date']['case'],'not empty')

        self.record['contract_date'] = '3425667'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_date']['status'], 'fail')
        self.assertEqual(result['contract_date']['case'],'format')

    def test_description_en(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_en']['status'], 'pass')

        self.record['description_en'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_en']['status'], 'fail')
        self.assertEqual(result['description_en']['case'],'not empty')

        self.record['contract_value'] = '3000'
        self.record['description_en']=' dfdggd'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_en']['status'], 'pass')

        self.record['description_en'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_en']['status'], 'pass')

    def test_description_fr(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_fr']['status'], 'pass')

        self.record['description_fr'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_fr']['status'], 'fail')
        self.assertEqual(result['description_fr']['case'],'not empty')

        self.record['description_fr'] = 'erttttt'
        self.record['contract_value'] = '3000'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_fr']['status'], 'pass')

        self.record['description_fr'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['description_fr']['status'], 'pass')

    def test_contract_period_start_no_code_G(self):

        #no commodity_type_code
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'unknown')

        self.record['commodity_type_code'] = 'G'

        #empty case
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'fail')
        self.assertEqual(result['contract_period_start']['case'],'empty')

        self.record['contract_period_start'] =''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'pass')


    def test_contract_period_start_S(self):
        self.record['commodity_type_code'] = 'S'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'pass')

        self.record['contract_period_start']=''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'fail')
        self.assertEqual(result['contract_period_start']['case'],'not empty')

        self.record['contract_period_start'] = '12345'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'fail')
        self.assertEqual(result['contract_period_start']['case'],'format')

        self.record['contract_value'] = '3000'
        result = self.data_validator.validate(self.record)
        print 'result: '+ json.dumps(result)
        self.assertEqual(result['contract_period_start']['case'],'format')

        self.record['contract_period_start'] = "2014-01-01"
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'pass')

        self.record['contract_period_start'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_period_start']['status'], 'pass')


    def test_delivery_date(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['delivery_date']['status'], 'pass')

        self.record['delivery_date'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['delivery_date']['status'], 'fail')
        self.assertEqual(result['delivery_date']['case'],'not empty')

        self.record['delivery_date'] = '123456'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['delivery_date']['status'], 'fail')
        self.assertEqual(result['delivery_date']['case'],'format')

        self.record['contract_value'] = '3000'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['delivery_date']['status'], 'fail')
        self.assertEqual(result['delivery_date']['case'],'format')

        self.record['contract_value'] = '3000'
        self.record['delivery_date'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['delivery_date']['status'], 'pass')


    def test_contract_value(self):

        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_value']['status'], 'pass')

        self.record['contract_value']=''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_value']['status'], 'fail')
        self.assertEqual(result['contract_value']['case'],'not empty')

        self.record['contract_value']='afdg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_value']['status'], 'fail')
        self.assertEqual(result['contract_value']['case'],'format')

    def test_original_value(self):

        result = self.data_validator.validate(self.record)
        self.assertEqual(result['original_value']['status'], 'fail')

        self.record['original_value']='1234'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['original_value']['status'], 'pass')

        self.record['original_value']='a1234'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['original_value']['status'], 'fail')
        self.assertEqual(result['original_value']['case'],'format')

    def test_amendment_value(self):

        result = self.data_validator.validate(self.record)
        self.assertEqual(result['amendment_value']['status'], 'fail')
        self.assertEqual(result['amendment_value']['case'],'not empty')


        self.record['amendment_value']='12345'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_value']['status'], 'pass')

        self.record['contract_value']='afdg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['contract_value']['status'], 'fail')
        self.assertEqual(result['contract_value']['case'],'format')


    def test_comments_en(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_en']['status'], 'pass')

        self.record['comments_en'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_en']['status'], 'fail')
        self.assertEqual(result['comments_en']['case'],'not empty')

        self.record['contract_value'] = '3000'
        self.record['comments_en'] = 'dgdffd'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_en']['status'], 'pass')

        self.record['comments_en'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_en']['status'], 'pass')

    def test_comments_fr(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_fr']['status'], 'pass')

        self.record['comments_fr'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_fr']['status'], 'fail')
        self.assertEqual(result['comments_fr']['case'],'not empty')

        self.record['comments_fr'] = 'erttttt'
        self.record['contract_value'] = '3000'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_fr']['status'], 'pass')

        self.record['comments_fr'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['comments_fr']['status'], 'pass')


    def test_additional_comments_en(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['additional_comments_en']['status'], 'pass')

        self.record['additional_comments_en'] = 'ffgdgdg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['additional_comments_en']['status'], 'pass')

    def test_additional_comments_fr(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['additional_comments_fr']['status'], 'pass')

        self.record['additional_comments_en'] = 'ffgdgdg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['additional_comments_fr']['status'], 'pass')

    def test_agreement_type_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['agreement_type_code']['status'], 'fail')
        self.assertEqual(result['agreement_type_code']['case'],'valid entry')

        self.record['agreement_type_code'] = 'w'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['agreement_type_code']['status'], 'fail')
        self.assertEqual(result['agreement_type_code']['case'],'valid entry')

        self.record['agreement_type_code'] = 'W'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['agreement_type_code']['status'], 'pass')


    def test_commodity_type_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_type_code']['status'], 'fail')
        self.assertEqual(result['commodity_type_code']['case'],'not empty')

        self.record['commodity_type_code'] = 'T'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_type_code']['status'], 'fail')
        self.assertEqual(result['commodity_type_code']['case'],'valid entry')

        self.record['commodity_type_code'] = 'S'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_type_code']['status'], 'pass')


    def test_commodity_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_code']['status'], 'fail')
        self.assertEqual(result['commodity_code']['case'],'not empty')

        self.record['commodity_code'] = 'T'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_code']['status'], 'fail')
        self.assertEqual(result['commodity_code']['case'],'valid entry')

        self.record['commodity_code'] = 'JX3610AA'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['commodity_code']['status'], 'pass')


    def test_country_of_origin(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['country_of_origin']['status'], 'fail')
        self.assertEqual(result['country_of_origin']['case'], 'not empty')

        self.record['country_of_origin'] = 'T'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['country_of_origin']['status'], 'fail')
        self.assertEqual(result['country_of_origin']['case'], 'valid entry')

        self.record['country_of_origin'] = 'AS'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['country_of_origin']['status'], 'unknown')

        self.record['aboriginal_business'] = 'True'
        self.record['commodity_type_code'] = 'S'
        self.record['country_of_origin'] = 'CA'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['country_of_origin']['status'], 'pass')

        self.record['country_of_origin'] = 'AS'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['country_of_origin']['status'], 'fail')
        self.assertEqual(result['country_of_origin']['case'],'not CA')


    def test_solicitation_procedure_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['solicitation_procedure_code']['status'], 'fail')
        self.assertEqual(result['solicitation_procedure_code']['case'], 'not empty')

        self.record['solicitation_procedure_code'] = 'T'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['solicitation_procedure_code']['status'], 'fail')
        self.assertEqual(result['solicitation_procedure_code']['case'], 'valid entry')

        self.record['solicitation_procedure_code'] = 'ac'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['solicitation_procedure_code']['status'], 'fail')
        self.assertEqual(result['solicitation_procedure_code']['case'], 'valid entry')

        self.record['solicitation_procedure_code'] = 'AC'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['solicitation_procedure_code']['status'], 'pass')


    def test_limited_tendering_reason_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['limited_tendering_reason_code']['status'], 'pass')

        self.record['limited_tendering_reason_code'] = '10'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['limited_tendering_reason_code']['status'], 'fail')
        self.assertEqual(result['limited_tendering_reason_code']['case'], 'valid entry')

        self.record['limited_tendering_reason_code'] = '21'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['limited_tendering_reason_code']['status'], 'pass')


    def test_derogation_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['derogation_code']['status'], 'pass')

        self.record['derogation_code'] = '00'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['derogation_code']['status'], 'pass')


        self.record['derogation_code'] = '21'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['derogation_code']['status'], 'fail')
        self.assertEqual(result['derogation_code']['case'], 'valid entry')


    def test_aboriginal_business(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['aboriginal_business']['status'], 'fail')
        self.assertEqual(result['aboriginal_business']['case'], 'not empty')

        self.record['aboriginal_business'] = 'True'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['aboriginal_business']['status'], 'pass')

        self.record['aboriginal_business'] = 'Ta'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['aboriginal_business']['status'], 'fail')
        self.assertEqual(result['aboriginal_business']['case'], 'valid entry')

    def test_intellectual_property_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['intellectual_property_code']['status'], 'unknown')

        self.record['intellectual_property_code'] = ''
        self.record['original_value'] = '26000'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['intellectual_property_code']['status'], 'fail')
        self.assertEqual(result['intellectual_property_code']['case'], 'not empty')

        self.record['intellectual_property_code'] = 'Ta'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['intellectual_property_code']['status'], 'fail')
        self.assertEqual(result['intellectual_property_code']['case'], 'valid entry')

        self.record['intellectual_property_code'] = 'B'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['intellectual_property_code']['status'], 'pass')

        self.record['intellectual_property_code'] = ' '
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['intellectual_property_code']['status'], 'pass')


    def test_potential_commercial_exploitation(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['potential_commercial_exploitation']['status'], 'unknown')

        self.record['intellectual_property_code'] = 'B'
        self.record['original_value'] = '26000'
        self.record['potential_commercial_exploitation'] = 'True'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['potential_commercial_exploitation']['status'], 'pass')

        self.record['potential_commercial_exploitation'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['potential_commercial_exploitation']['status'], 'fail')
        self.assertEqual(result['potential_commercial_exploitation']['case'], 'not empty')

        self.record['potential_commercial_exploitation'] = 'A'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['potential_commercial_exploitation']['status'], 'fail')
        self.assertEqual(result['potential_commercial_exploitation']['case'], 'valid entry')

    def test_former_public_servant(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'unknown')

        self.record['commodity_type_code'] = 'S'
        self.record['contract_value'] = '26000'
        self.record['former_public_servant'] ='False'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'pass')

        self.record['former_public_servant'] =''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'fail')
        self.assertEqual(result['former_public_servant']['case'], 'not empty')


    def test_former_public_servant(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'unknown')

        self.record['commodity_type_code'] = 'S'
        self.record['contract_value'] = '26000'
        self.record['former_public_servant'] ='False'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'pass')

        self.record['former_public_servant'] =''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['former_public_servant']['status'], 'fail')
        self.assertEqual(result['former_public_servant']['case'], 'not empty')

    def test_standing_offer(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer']['status'], 'pass')

        self.record['standing_offer'] = 'PWSOSA'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer']['status'], 'pass')

        self.record['standing_offer'] ='ddg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer']['status'], 'fail')
        self.assertEqual(result['standing_offer']['case'], 'valid entry')

    def test_standing_offer_number(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer_number']['status'], 'pass')

        self.record['standing_offer'] = 'PWSOSA'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer_number']['status'], 'fail')
        self.assertEqual(result['standing_offer_number']['case'], 'not empty')

        self.record['standing_offer_number'] = '1223'
        self.record['standing_offer'] = ''
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer_number']['status'], 'fail')
        self.assertEqual(result['standing_offer_number']['case'], 'empty')


        self.record['standing_offer'] = 'PWSOSA'
        self.record['standing_offer_number'] = '1223'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer_number']['status'], 'pass')


        self.record['standing_offer'] ='ddg'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['standing_offer_number']['status'], 'unknown')

    def test_document_type_code(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['document_type_code']['status'], 'fail')
        self.assertEqual(result['document_type_code']['case'], 'not empty')

        self.record['document_type_code'] = 'c'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['document_type_code']['status'], 'fail')
        self.assertEqual(result['document_type_code']['case'], 'valid entry')

        self.record['document_type_code'] = 'C'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['document_type_code']['status'], 'pass')


    def test_reporting_period(self):

        #mandatory
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['reporting_period']['status'], 'fail')
        self.assertEqual(result['reporting_period']['case'], 'not empty')

        self.record['contract_value'] = '3000'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['reporting_period']['status'], 'pass')

        self.record['reporting_period'] = '2015-2016-Q1'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['reporting_period']['status'], 'fail')
        self.assertEqual(result['reporting_period']['case'], 'empty')

        self.record['contract_value'] = '15000'
        self.record['reporting_period'] = '2015-2016-Q1'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['reporting_period']['status'], 'pass')

        self.record['reporting_period'] = 'abcdef'
        result = self.data_validator.validate(self.record)
        self.assertEqual(result['reporting_period']['status'], 'fail')
        self.assertEqual(result['reporting_period']['case'], 'format')


if __name__=='__main__':
    unittest.main()










