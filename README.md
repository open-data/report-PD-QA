# report-PD-QA

This package implements a data validation function. The function validates the data stored in opendata.ca according to those rules defined in their schema.

The main function of the data validation is defined as main() in datastore_validation.py. The main() sets up the running environment using env.json. It retrieves the data from opendata.ca and validates them using their schema.

The env.json specifies the parameters (e.g., api_key, the types of data, and the directories) used by the data validation. env.json.example is an example of such a file.

The schema files define the column structures of different data types. A schema file contain the validation rules for each column. The data validation uses those rules to verify the correctness and meanfulness of data that are identified with those columns.

A column's data is correct or valid only in the case that it passes all of the validation cases defined for that column. A case may contain a simple proposition or a conditional one. A simple proposition contains a field name and a rule specification. The field name specifies to which column's data should the rule be applied. A field name may be absent. In this case, the validation applies the rule to the data in the current column. A simple proposition could be either true or false. The validation case contains a simple proposition is passed only in the case the proposition is true. Otherwise, the case is failed.
A conditional proposition contains antecedent and consequent. Both of them further contains simple propositions. An antecedent may contain mulitple simple propositions. It is true only in the case that all of its simple propositions are true. Then, the consequent will be further verified. The validation case is passed in the case that the conseqent is true as well. In the case the antecedent is false, the validation case is passed whatever.  A conditional proposition may be in unknown state, for example, the data of a column defined in an  antecedent's proposition is invalid. In this case, the validation case is in unknown state as well.
The output from the data validation are stored in the files in two different directories: internal_report and external_report. These files are further organized according to the running time of the data validation. The internal_report stores the files for the purpose of internal usage, for example, those data generated in the middle of the running and the messages of errors occurring. The external_report stores the report files, e.g., a general csv file, and a csv file and a txt file for a department that has data.

This prackage also contains two files for unit testing. One file verifies the correctness of the validation, and another verifies the formats of output.