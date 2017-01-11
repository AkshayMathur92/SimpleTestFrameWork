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


def read_csv_header(file):
    "read csv header"
    header = []
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        header = reader.fieldnames
    return header

def create_json(schema, args):
    """generate copy of schema with new values in args"""
    schema = json.loads(copy.deepcopy(schema))
    for key in schema:
        if key in args:
            if type(schema[key]) == type(args[key]):
                schema[key] = args[key]
                if args[key].lower() == "null":
                    schema[key] = None
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
    headers = read_csv_header(csvfile)
    headers.append('json')
    write_header(outputfile, headers, 'w+')
    with open(specfile, 'r') as sfile:
        spec = sfile.read().replace('\n', '')
    file_handle = open(csvfile, 'r')
    input_data = csv.DictReader(file_handle, delimiter=',', skipinitialspace=True)
    unique = set()
    for row in input_data:
        res = {}
        for header, value  in row.items():
            res[header] = value
            res.update({'json' : json.dumps(create_json(spec, args=res))})
        if len(res['REASON']) == 0 or res['REASON'] not in unique:
            unique.add(res['REASON'])
            write_csv(outputfile, res, headers, 'a')
    file_handle.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
