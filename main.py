"""Main for TestFramework"""
import sys
import getopt
from ACPSTestFrameWork.GenerateCombinations import main as generatecombination
from ACPSTestFrameWork.Evaluate import main as evaluate
from ACPSTestFrameWork.JsonGenerator import main as jsongenerator

def main(argv):
    """Main """
    apiname = ''
    functionfile = ''
    inputvaluesfile = ''
    jsonschemafile = ''
    testcasesfile = ''
    jsoncasesfile = ''
    try:
        opts, args = getopt.getopt(argv, "ha:")
        if len(opts) < 1:
            raise getopt.GetoptError("see -h")
    except getopt.GetoptError:
        print('python main.py -a <ApiName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(argv[0] + ' -a <ApiName>')
            sys.exit()
        elif opt in ("-a", "--ApiName"):
            apiname = arg.lower()
            inputvaluesfile = './InputValuesJson/'+ apiname + '.json'
            functionfile = './EvaluateFunctions/' + apiname + '.py'
            jsonschemafile = './JsonSchema/' + apiname +'.json'
    print('Generating all test cases')
    generatecombination(("-i", inputvaluesfile, "-o", './ACPSTestFrameWork/temp/' + apiname +'_combinations.csv'))
    print('Evaluating all test cases')
    evaluate(("-c", './ACPSTestFrameWork/temp/' + apiname +'_combinations.csv', "-f", functionfile,"-o", "./output/"+apiname+"_evaluated.csv"))
    print('Creating Json for all test cases')
    jsongenerator(("-c",'./output/' + apiname +'_evaluated.csv', "-s", jsonschemafile, "-o", "./output/"+apiname+"_json.csv"))


if __name__ == "__main__":
    main(sys.argv[1:])
