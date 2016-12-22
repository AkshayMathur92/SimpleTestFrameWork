"""Script to generate all combinations from gives JSON"""
import sys
import getopt
import json
import csv
from itertools import product
from collections import OrderedDict


def read_json(inputfile):
    """Reads Json from the input file"""
    file_handle = open(inputfile)
    input_data = json.loads(file_handle.read(), object_pairs_hook=OrderedDict)
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
    header = [tuple(input_data.keys())]
    write_csv(outputfile, header, 'w+')
    output = []
    for element in product(*input_data.values()):
        output.append(element)
    write_csv(outputfile, output, 'a')

main(sys.argv[1:])
