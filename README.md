# SimpleTestFrameWork
A generic test framework for creating jsons files according to given spec and values
-------------------------------------------------------------------------------------

>**3 files are required to run main.py**


1. Input values json -- 
  this file contains a JSON object containing all fields in the API spec and their respective test values. 
  For example : Consider an api setProfile() which takes the following json structure 
  
	  
		  {
		  
		      "profile_id" : 123,
		      "name" : "AkshayMathur",
		      "is_premium": : true,
		      "valid_period" : {
		                          "begin" : "2016",
		                          "end" : "2017"
		                        }
		  }
		  
 so for each outer key in this JSON provide a test value inside [] eg; 
  
		  {
		  
		      "profile_id" : [123, 0, -1, 0.3, 'integer'],
		      "name" : ["AkshayMathur", "NBSP&%$# special chars, ""],
		      "is_premium": : [true, false]
		      "valid_period" : [{
		                          "begin" : 2016,
		                          "end" : 2017
		                        },
		                        {
		                          "begin" : 2050,
		                          "end" : 2017
		                        }
		                        ]
		  }
		  
	Name this file setprofile.json and put it in InputValuesJson folder
  
2. Create a python function with name *evaluate* which takes all first level hierarchy params from this jSON. Now write the corresponding logic for test value with all asserts and their failure reasons. 
        for eg;
        
        def evaluate( profile_id=None, name=None, is_premium=None, valid_period=None):
          assert isinstance(profile_id, int), "profile id should be an integer"
          assert len(name) > 0, "Name cannot be empty" 
          if is_premium;
            assert profile_id > 500 , "premium memebers have profile ID > 500" 
          assert 'begin' in valid_period , "valid period must contain a begin attribute"
          assert 'end' in valid_period, "valid period must contain an end attribute"
          assert valid_period['begin'] < valid_period['end'] , "begin date should be before end date"
  
  Name this file setprofile.py and keep it in EvaluateFunctions 
  
3. Last copy the original schema required by the api 
          
	      {
      
          "profile_id" : 123,
          "name" : "AkshayMathur",
          "is_premium": : true,
          "valid_period" : {
                              "begin" : "2016",
                              "end" : "2017"
                            }
	      }
      
  to JsonSchema directory with name setprofile.json
      
  
4. Run the main file as

      python main.py -a setprofile
5. This would create a csv named setprofile_evaluated.csv conaining an exhautive list of test cases marked with Result (PASS/FAIL) with a reson of failure in REASON column.

6. Additionally this would also create a column containing proper json body according to the schema spec of the api, which can be used by any curl client to run and evaluate the each test case. 

7. Now for every api just call main :
	
	python main.py -a setprofile
	python main.py -a getprofile

