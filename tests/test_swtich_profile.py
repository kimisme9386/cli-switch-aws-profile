import pathlib

import pytest

from switch_profile import app


def test_validate_aws_profiles_not_found():
    file = 'notExistsFile'
    with pytest.raises(IOError, match=r".*No such file or directory.*"):
        app.validate_aws_profile(file)


def test_validate_aws_profiles_has_default():
    file = str(pathlib.Path(__file__).parents[0]) + '/credentials_has_default'
    with pytest.raises(Exception, match=r".*Found 'default' profile, please rename it*"):
        app.validate_aws_profile(file)


def test_get_aws_profiles_not_found():
    file = 'notExistsFile'
    with pytest.raises(IOError, match=r".*No such file or directory.*"):
        app.get_aws_profiles(file)


def test_get_aws_profile_sample1():
    file = str(pathlib.Path(__file__).parents[0]) + '/credentials_sample_1'
    profiles = app.get_aws_profiles(file)
    assert list(profiles.keys()) == ['[test1]', '[test2]', '[assume]']
    assert profiles["[test1]"] == ["[test1]\n",
                                   "aws_access_key_id = AKI11111111111111111\n",
                                   "aws_secret_access_key = aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb\n",
                                   "\n"]


def test_change_default_profile():
    file = str(pathlib.Path(__file__).parents[0]) + '/credentails_change_default'
    profiles = app.get_aws_profiles(file)
    app.change_default_profile(profiles, '[chris]', '[default]')
    assert list(profiles.keys()) == ['[chris]', '[wondercore]', '[assume]']
    assert profiles["[chris]"] == [";[chris]\n",
                                   "[default]\n",
                                   "aws_access_key_id = AKI11111111111111111\n",
                                   "aws_secret_access_key = aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb\n",
                                   "\n"]
    assert profiles["[wondercore]"] == ["[wondercore]\n",
                                        "aws_access_key_id = AKI22222222222222222\n",
                                        "aws_secret_access_key = cccccccccccccccccccccccdddddddddddddddddd\n",
                                        "\n"]
