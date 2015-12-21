# report-PD-QA

This package implements a data validation function. The function validates the data stored in opendata.ca according to rules defined in their schema.

The main function of the data validation is defined as main() in datastore_validation.py. It sets up its running environment by reading env.json. It retrieves the data from opendata.ca and validates them by their schema.

The env.json specifies the parameters (e.g., api_key, the types of data, and the directories) used by the data validation. env.json.example is an example of such a file.

The schema files define the data structures of different data types. A schema file may contain the rules that the data validation uses to verify the correctness and meanfulness of the data.

The output from the data validation are stored in the files in two different directories: internal_report and external_report. These files are further organized according to the running time of the data validation. The internal_report stores the files for the purpose of internal usage, for example, those data generated in the middle of the running and the messages of errors occurring. The external_report stores the report files, e.g., a general csv file, and a csv file and a txt file for a department that has data.

This prackage also contains two files for unit testing. One file verifies the correctness of the validation, and another verifies the formats of output.
