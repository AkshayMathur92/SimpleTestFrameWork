"""Script to generate all combinations from gives JSON"""
import sys
import getopt
import json
import csv
from itertools import product
import uuid
import copy
from ACPSTestFrameWork.all_pairs2 import all_pairs2 as pairwise


def read_json(inputfile):
    """Reads Json from the input file"""
    file_handle = open(inputfile)
    input_data = json.loads(file_handle.read())
    file_handle.close()
    return input_data

def write_csv(outputfile, out_data, mode):
    """Writes out_data to outputfile with file open mode"""
    file_handle = open(outputfile, mode, newline='')
    writer = csv.writer(file_handle, delimiter=',')
    for line in out_data:
        writer.writerow(line)
    file_handle.close()


def main(argv):
    """Main """
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(argv[0] + ' -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + ' -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    input_data = read_json(inputfile)
    if len(outputfile) == 0:
        outputfile = inputfile+'.csv'
    special_keys = []
    for key in list(input_data.keys()):
        if not isinstance(input_data[key], list):
            special_keys.append((key, input_data[key]))
            input_data.pop(key)
    header = [tuple(input_data.keys()) + tuple([x[0] for x in special_keys])]
    write_csv(outputfile, header, 'w+')
    output = []
    values = list(input_data.values())
    # for element in product(*input_data.values()):
    for element in pairwise(values, n = len(values)):
        output.append(element)
    new_output = []
    for key, value in special_keys:
        if value == '#UNIQUE':
            for row in output:
                new_output.append(tuple(row) + (uuid.uuid4(),))
    if len(new_output) > 0:
        write_csv(outputfile, new_output, 'a')
    else:
        write_csv(outputfile, output, 'a')

if __name__ == "__main__":
    main(sys.argv[1:])
