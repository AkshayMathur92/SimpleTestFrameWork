"""Evaluate function for policy"""
from datetime import datetime
import re

# Rev: These should be documented
CONSTRAINTS = ["CHANGEABLE","NOT_CHANGEABLE","NOT_APPLICABLE"]
PERMISSIONS = ["OPEN_ONLINE","OPEN_OFFLINE","PRINT_HIGH","CHANGES_ALL_EXCEPT_EXTRACT_CONTENT","COPY"]
DESCRIPTION_REGEX = re.compile("^[^<>&\"/\\\\]+$")
POLICY_TYPES = ["CUSTOMIZABLE","NON_CUSTOMIZABLE","AD_HOC"]
POLICY_SETS = ["Test_PolicySet_Combination_1","Test_PolicySet_Combination_2","Test_PolicySet_EXTERNAL","Test_PolicySet_INTERNAL"]
LDAP_USERS = ["saggarwa", "stanwar", "ashukla", "amathur"]
LOCAL_DOMAIN_USERS = ["ACPSTEST USER","ACPSTESTExternalGroup USER"]
DOMAINS = ["AdobeLDAP", "Test_LOCAL_DOMAIN"]

def evaluate(description=None, offline_lease_period=None, is_tracked=None, name=None,policy_type=None, parent_policy_id=None,
            policy_set=None, validity_period=None, permissions=None, principals=None, watermark_id=None):
    """evaluate function"""

    assert isinstance(description,str) , "description constraints must be string"
    assert len(description) < 250 , "lenght of description should <250"
    assert len(description) >= 0 ,"lenght of description should >0"
    assert DESCRIPTION_REGEX.match(description) , "description should not contain <>$\"\\\\+"

    assert isinstance(offline_lease_period['value'] , int), "offline_lease_period must be integer"
    assert offline_lease_period['value'] > 0, "offline_lease_period should be integer greater than 0"
    assert offline_lease_period['value'] < 10000 ,"offline_lease_period should be integer less than 1000"

    assert isinstance(is_tracked['value'], bool), "is_tracked must be bool"

    # assert len(name) < 50, "name length should be bw 0-50"

    assert isinstance(policy_type, str), "policy_type must be string"
    assert policy_type in POLICY_TYPES, "policy_type can only be CUSTOMIZABLE NON_CUSTOMIZABLE AD_HOC"

    # Rev: Environment specific
    assert isinstance(policy_set, str), "policy_set must be string"
    assert policy_set in POLICY_SETS, "policy_set can only be Test_PolicySet_Combination_1 Test_PolicySet_Combination_2 Test_PolicySet_EXTERNAL Test_PolicySet_INTERNAL"

    # Discuss when parent policy is null
    if parent_policy_id.lower() == "null":
        assert isinstance(parent_policy_id, str), "policy id must be string"
        assert policy_type != "AD_HOC", "policy_type should be CUSTOMIZABLE NON_CUSTOMIZABLE if parent_policy_id is null"
    else:
        assert policy_type == "AD_HOC", "parent policy should only be present when policy_type is adhoc"
    
    assert isinstance(permissions['value'], list), "permissions value must be list"
    for permission in permissions['value']:
        assert permission in PERMISSIONS, "permission can only be OPEN_ONLINE OPEN_OFFLINE PRINT_HIGH CHANGES_ALL_EXCEPT_EXTRACT_CONTENT COPY"

    assert isinstance(validity_period['value'], dict), "validity_period should be a JSON object"
    if 'begin' in validity_period['value']:
        assert 'end' in validity_period['value'] ,"if begin is present in validity period then end should be present"
        assert 'days' not in validity_period['value'] , " if begin is present in validity period then days should not be present"
        begin = datetime.strptime(validity_period['value']['begin'], "%Y-%m-%dT%H:%M:%S.%fZ")
        end = datetime.strptime(validity_period['value']['end'], "%Y-%m-%dT%H:%M:%S.%fZ")
        assert begin < end, "begin date should be less than end date"
    if 'days' in validity_period['value']:
        assert 'begin' not in validity_period['value'] and 'end' not in validity_period['value'], "if days in validity period present than begin or end should not be present"
        assert isinstance(validity_period['value']['days'], int) , "days should be an integer"
        assert validity_period['value']['days'] > 0 and validity_period['value']['days'] < 10000 , "days in Validity period should be bw 0-10000"

    for principal in principals['value']:
        assert isinstance(principal, dict) , "principals should contain only JSON objects"
        assert 'type' in principal , "principal should contain a type attribute"
        assert principal['type'] == "UserOrGroup" or principal['type'] == "AnonymousUser" , "type should be UserOrGroup or AnonymousUser"
        if principal['type'] == "AnonymousUser":
            assert len(principals['value']) == 1 , "if any entry has type AnonymousUser then only one object should be present in principals"
        else:
            assert 'domain' in principal, "domain attribute should be present in pricipal"
            assert 'name' in principal, "name attribute should be present in principal"
    
    #Environment specific tests goes here.

    for pricipal in principals['value']:
        if 'domain' and 'name' in principal:
            assert principal['domain'] in DOMAINS, "invalid domain entry"
            if principal['domain'] == DOMAINS[0]:
                assert principal['name'] in LDAP_USERS, "principal should be LDAP user"
                assert policy_set != "Test_PolicySet_EXTERNAL", "this policy set can only used for external users ony"
            if principal['domain'] == DOMAINS[1]:
                assert principal['name'] in LOCAL_DOMAIN_USERS, "principal should be Local User"
                assert policy_set != "Test_PolicySet_INTERNAL", "this policy set can only used for internal users only"