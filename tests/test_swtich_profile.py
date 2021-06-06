import pathlib

import pytest

from switch_profile import switch_profile


def test_validate_aws_profiles_not_found():
    file = 'notExistsFile'
    with pytest.raises(IOError, match=r".*No such file or directory.*"):
        switch_profile.validate_aws_profile(file)


def test_validate_aws_profiles_has_default():
    file = str(pathlib.Path(__file__).parents[0]) + '/credentials_has_default'
    with pytest.raises(Exception, match=r".*Found 'default' profile, please rename it*"):
        switch_profile.validate_aws_profile(file)


def test_get_aws_profiles_not_found():
    file = 'notExistsFile'
    with pytest.raises(IOError, match=r".*No such file or directory.*"):
        switch_profile.get_aws_profiles(file)


def test_get_aws_profile_sample1():
    file = str(pathlib.Path(__file__).parents[0]) + '/credentials_sample_1'
    profiles = switch_profile.get_aws_profiles(file)
    assert list(profiles.keys()) == ['[test1]', '[test2]', '[assume]']
    assert profiles["[test1]"] == ["[test1]\n",
                                   "aws_access_key_id = AKI11111111111111111\n",
                                   "aws_secret_access_key = aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb\n",
                                   "\n"]
