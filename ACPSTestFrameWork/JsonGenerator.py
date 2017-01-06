"""Create JSON based on given spec"""
import sys
import getopt
import csv
import json
import copy
import ast

def read_csv(file):
    "readind csv rowwise"
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            yield row

def write_csv(outputfile, out_data, fieldname, mode):
    """Writes out_data to outputfile with file open mode"""
    file_handle = open(outputfile, mode)
    writer = csv.DictWriter(file_handle, fieldnames=fieldname, delimiter=',', lineterminator='\n')
    writer.writerow(out_data)
    file_handle.close()

def write_header(outputfile, fieldname, mode):
    """Writes out_data to outputfile with file open mode"""
    file_handle = open(outputfile, mode)
    writer = csv.DictWriter(file_handle, fieldnames=fieldname, delimiter=',', lineterminator='\n')
    writer.writeheader()
    file_handle.close()

def create_json(schema, args):
    """generate copy of schema with new values in args"""
    schema = json.loads(copy.deepcopy(schema))
    for key in schema:
        if key in args:
            if type(schema[key]) == type(args[key]):
                schema[key] = args[key]
            else:
                schema[key] = ast.literal_eval(args[key])
    return schema

def main(argv):
    """Main """
    csvfile = ''
    specfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "c:s:o:", ["csvfile=", "specfile=", "outputfile="])
        for opt, arg in opts:
            if opt == '-h':
                print(argv[0] + ' -c <csvfile> -s <specfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-c", "--csvfile"):
                csvfile = arg
            elif opt in ("-s", "--specfile"):
                specfile = arg
            elif opt in ("-o", "--outputfile"):
                outputfile = arg
    except getopt.GetoptError:
        print(argv[0] + ' -c <csvfile> -s <specfile> -o <outputfile>')
    spec = ""
    with open(specfile, 'r') as sfile:
        spec = sfile.read().replace('\n', '')
    input_data = csv.DictReader(open(csvfile, 'r'), delimiter=',', skipinitialspace=True)
    write_header(outputfile, ['json','RESULT'], 'w')
    for row in input_data:
        res = {}
        for header, value  in row.items():
            res[header] = value
        created_json = create_json(spec, args=res)
        write_csv(outputfile, {'json' : json.dumps(created_json), 'RESULT' : row['RESULT']}, ['json', 'RESULT'], 'a')

if __name__ == "__main__":
    main(sys.argv[1:])
