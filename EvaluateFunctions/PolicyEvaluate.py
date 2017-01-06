"""Evaluate function for policy"""
from datetime import datetime
import re


PERMISSIONS = ["OPEN_ONLINE","OPEN_OFFLINE","PRINT_HIGH","CHANGES_ALL_EXCEPT_EXTRACT_CONTENT","COPY"]
DESCRIPTION_REGEX = re.compile("^[^<>&\"/\\\\]+$")


def evaluate(policy_entries=None, policy_set_name=None, watermark_id=None, name=None,
             customizable=None, description=None, offline_lease_period=None,
             policy_set=None, validity_period=None):
    """evaluate function"""
    assert isinstance(customizable, bool), "customizable should be boolean"

    assert isinstance(offline_lease_period, int) ,"offline_lease_period should be integer"
    assert offline_lease_period > 0 and offline_lease_period < 10000 ,"offline_lease_period should be integer bw 0 - 1000 "

    assert isinstance(description, str) and len(description) < 250 and len(description) >= 0 ,"lenght of description should be bw 0 - 250"
    assert DESCRIPTION_REGEX.match(description) , "description should not contain <>$\"\\\\+"
    
    assert isinstance(name, str) and len(name) < 50, "name length should be integer bw 0-50"

    assert isinstance(validity_period, dict) , "validity_period should be a JSON object"
    if 'begin' in validity_period:
        assert 'end' in validity_period ,"if begin is present in validity period then end should be present"
        assert 'days' not in validity_period , " if begin is present in validity period then days should not be present"
        begin = datetime.strptime(validity_period['begin'], "%Y-%m-%dT%H:%M:%S.%fZ")
        end = datetime.strptime(validity_period['end'], "%Y-%m-%dT%H:%M:%S.%fZ")
        assert begin < end, "begin date should be less than end date"
    if 'days' in validity_period:
        assert 'begin' not in validity_period and 'end' not in validity_period, "if days in validity period present than begin or end should not be present"
        assert isinstance(validity_period['days'], int) , "days should be an integer"
        assert validity_period['days'] > 0 and validity_period['days'] < 10000 , "days in Validity period should be bw 0-10000"

    assert isinstance(policy_entries, list) , "policy_entries should be an array"
    assert len(policy_entries) > 0, "policy entry should not be empty"
    for perm_obj in policy_entries:
        assert isinstance(perm_obj, dict) , "policy_entries should contain only JSON objects"
        assert 'permissions' in perm_obj and 'principal' in perm_obj, "policy_entries should contain permissions object and principal object"
        assert isinstance(perm_obj['permissions'], list), "permission in policy_entries should be an array"
        assert len(perm_obj['permissions']) > 0, "permission object should not be empty"
        for permission in perm_obj['permissions']:
            assert permission in PERMISSIONS , " permission object should only contain OPEN_ONLINE ,OPEN_OFFLINE,PRINT_HIGH,CHANGES_ALL_EXCEPT_EXTRACT_CONTENT,COPY"
        assert 'type' in perm_obj['principal'] , "principal should contain a type attribute"
        assert perm_obj['principal']['type'] == "UserOrGroup" or perm_obj['principal']['type'] == "AnonymousUser" , "type should be UserOrGroup or AnonymousUser"
        if perm_obj['principal']['type'] == "AnonymousUser":
            assert len(policy_entries) == 1 , "is any entry has type AnonymousUser then only one object should be present in policy_entries"
        else:
            assert 'domain' in perm_obj['principal'], "domain attribute should be present in pricipal"
            assert 'name' in perm_obj['principal'], "name attribute should be present in principal"
