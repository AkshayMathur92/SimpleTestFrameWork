"""Evaluate JSON based on given criteria"""
import sys
import getopt
from importlib.machinery import SourceFileLoader

def main(argv):
    """Main """
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
    eval_module.evaluate(**{'policy_name' : "hello", 'policy_description' : "world"})

main(sys.argv[1:])
