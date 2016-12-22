"""Script to generate all CSV based on constraint spec"""
import sys
import getopt
import json
import csv
import ast
from collections import OrderedDict

def read_json(inputfile):
    """Reads Json from inputfile"""
    file_handle = open(inputfile)
    input_data = json.loads(file_handle.read(), object_pairs_hook=OrderedDict)
    file_handle.close()
    return input_data

def read_csv(inputfile):
    """Reads CSV from inputfile"""
    file_handle = open(inputfile)
    input_data = csv.DictReader(file_handle, delimiter=',', skipinitialspace=True)
    result = {}
    for row in input_data:
        for header, value  in row.items():
            try:
                if isinstance(value, str) and value.startswith('['):
                    result[header].append(ast.literal_eval(value))
                else:
                    result[header].append(value)
            except KeyError:
                result[header] = [value]
    return result

def write_csv(outputfile, out_data, mode):
    """Writes out_data to outputfile with file open mode"""
    file_handle = open(outputfile, mode, newline='')
    writer = csv.writer(file_handle, delimiter=',', skipinitialspace=True)
    for line in out_data:
        writer.writerow(line)
    file_handle.close()

def create_file(spec):
    """Iterate over keys to create files"""
    for key in spec:
        file_name = str(key) + ".csv"
        file_handle = open(file_name, 'w+')
        file_handle.close()
        yield file_name

def main(argv):
    """Main"""
    csvfile = ''
    jsonfile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:j:", ["csv=", "json="])
    except getopt.GetoptError:
        print(argv[0] + ' -c <csvfile> -j <jsonfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + ' -c <csvfile> -j <jsonfile>')
            sys.exit()
        elif opt in ("-c", "--csv"):
            csvfile = arg
        elif opt in ("-j", "--json"):
            jsonfile = arg

    input_attributes = read_csv(csvfile)
    all_attibutes = list(input_attributes.keys())
    spec = read_json(jsonfile)
    new_attributes = []
    for key in spec.keys():
        fixed_attributes = spec[key]['fixed']
        new_attributes.append([item for item in all_attibutes if item not in fixed_attributes])

    for file_name, attributes in zip(create_file(spec), new_attributes):
        header = [tuple(attributes)]
        write_csv(file_name, header, 'w+')
        output = ()
        for attribute in attributes:
            csv_data = read_csv(csvfile)
            if isinstance(csv_data[attribute][0], str) and csv_data[attribute][0].startswith('['):
                output += tuple([ast.literal_eval(csv_data[attribute][0])])
            else:
                output += tuple([csv_data[attribute][0]])
        write_csv(file_name, [output], 'a')
main(sys.argv[1:])
