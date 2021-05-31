import pytest
from switch_profile import switch_profile


def test_get_aws_profiles_not_found():
    file_name = 'notExistsFile'
    with pytest.raises(IOError, match=r".*No such file or directory.*"):
        switch_profile.get_aws_profiles(file_name)
