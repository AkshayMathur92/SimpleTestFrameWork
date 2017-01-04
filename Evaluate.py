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

def main(argv):
    """Main """
    result = []
    csvfile = ''
    functionfile = ''
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
    eval_module = SourceFileLoader("evaluate", functionfile).load_module()
    number = re.compile("[0-9]+$")
    boolean = re.compile("^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$")
    for row in read_csv(csvfile):
        new_row = {}
        for key, value in row.items():
            if isinstance(value, str) and (value.startswith('[') or value.startswith('{') or boolean.match(value)):
                new_row[key] = ast.literal_eval(value)
            elif isinstance(value, str) and number.match(value):
                new_row[key] = int(value)
            else:
                new_row[key] = value
        try:
            eval_module.evaluate(**new_row)
            result.append("PASS")
        except Exception:
            result.append("FAIL")

    print(result)
main(sys.argv[1:])
