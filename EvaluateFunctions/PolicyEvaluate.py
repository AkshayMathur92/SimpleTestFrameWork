"""Evaluate function for policy"""
from datetime import datetime
# is_tracked to be added

PERMISSIONS = ["OPEN_ONLINE","OPEN_OFFLINE","PRINT_HIGH","CHANGES_ALL_EXCEPT_EXTRACT_CONTENT","COPY"]

def evaluate(policy_entries=None, policy_set_name=None, watermark_id=None, name=None,
             customizable=None, description=None, offline_lease_period=None,
             policy_set=None, validity_period=None):
    """evaluate function"""
    assert isinstance(customizable, bool)
    assert isinstance(offline_lease_period, int) and offline_lease_period > 0 and offline_lease_period < 10000
    assert isinstance(description, str) and len(description) < 250
    assert isinstance(name, str) and len(name) < 50

    assert isinstance(validity_period, dict)
    if 'begin' in validity_period:
        assert 'end' in validity_period
        assert 'days' not in validity_period
        begin = datetime.strptime(validity_period['begin'], "%Y-%m-%dT%H:%M:%S.%fZ")
        end = datetime.strptime(validity_period['end'], "%Y-%m-%dT%H:%M:%S.%fZ")
        assert begin < end
    if 'days' in validity_period:
        assert 'begin' not in validity_period and 'end' not in validity_period
        assert isinstance(validity_period['days'], int)
        assert validity_period['days'] > 0 and validity_period['days'] < 10000

    assert isinstance(policy_entries, list)
    for perm_obj in policy_entries:
        assert isinstance(perm_obj, dict)
        assert 'permissions' in perm_obj and 'principal' in perm_obj
        assert isinstance(perm_obj['permissions'], list)
        assert len(perm_obj['permissions']) > 0
        for permission in perm_obj['permissions']:
            assert permission in PERMISSIONS
        assert 'type' in perm_obj['principal']
        assert perm_obj['principal']['type'] == "UserOrGroup" or perm_obj['principal']['type'] == "AnonymousUser"
        if perm_obj['principal']['type'] == "AnonymousUser":
            assert len(policy_entries) == 1
        else:
            assert 'domain' in perm_obj['principal']
            assert 'name' in perm_obj['principal']
