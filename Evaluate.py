"""Evaluate JSON based on given criteria"""
import sys
import getopt
import csv
import ast
import re
from importlib.machinery import SourceFileLoader

def read_csv(file):
    "readind csv rowwise"
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            yield row
def read_csv_header(file):
    "read csv header"
    header = []
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        header = reader.fieldnames
    return header

def write_csv_header(outputfile, fieldname, mode):
    """Writes out_data to outputfile with file open mode"""
    file_handle = open(outputfile, mode)
    writer = csv.DictWriter(file_handle, fieldnames=fieldname, delimiter=',', lineterminator='\n')
    writer.writeheader()
    file_handle.close()

def main(argv):
    """Main """
    csvfile = ''
    functionfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:f:", ["csvfile=", "functionfile="])
    except getopt.GetoptError:
        print(argv[0] + ' -c <csvfile> -f <functionfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + ' -c <csvfile> -f <functionfile>')
            sys.exit()
        elif opt in ("-c", "--csvfile"):
            csvfile = arg
        elif opt in ("-f", "--functionfile"):
            functionfile = arg
    outputfile = csvfile + '_evaluated_.csv'
    header = read_csv_header(csvfile)
    header.append('RESULT')
    header.append('REASON')
    write_csv_header(outputfile, header, 'w+')
    file_handle = open(outputfile, 'a')
    writer = csv.DictWriter(file_handle, fieldnames=header, delimiter=',', lineterminator='\n')
    eval_module = SourceFileLoader("evaluate", functionfile).load_module()
    number = re.compile("[0-9]+$")
    boolean = re.compile("^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$")
    for row in read_csv(csvfile):
        new_row = {}
        for key, value in row.items():
            if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                new_row[key] = ast.literal_eval(value)
            elif boolean.match(value):
                new_row[key] = bool(value)
            elif isinstance(value, str) and number.match(value):
                new_row[key] = int(value)
            else:
                new_row[key] = value
        try:
            eval_module.evaluate(**new_row)
            new_row['RESULT'] = "PASS"
        except AssertionError as err:
            new_row['RESULT'] = "FAIL"
            new_row['REASON'] = err
        writer.writerow(new_row)
main(sys.argv[1:])
