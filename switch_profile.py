#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

from pprint import pprint
from typing import Match

from PyInquirer import prompt, Separator

from examples import custom_style_2
import re
from pathlib import Path
import sys

# credential_file = f"{Path.home()}/.aws/credentials"
credential_file = "./credentials_sample"
profile_default_title = "[default]"


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


def validate_aws_profile():
    try:
        profile_title = ""
        with open(credential_file, "r") as file:
            lines = file.readlines()
            prev_line = ""
            for line in lines:
                m = re.match(r";?\[(\w+)\]", line)
                if m and m.group(0) == profile_default_title and prev_line[0] != ";":
                    raise Exception(
                        f"Found 'default' profile, please rename it.")

                prev_line = line

    except IOError:
        raise Exception(f"{credential_file} is not found.")


def get_aws_profiles() -> dict:

    profiles = dict()
    try:
        profile_title = ""
        with open(credential_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                m = re.match(r";?\[(\w+)\]", line)
                if m and m.group(0) != profile_default_title:
                    profile_title = line[1:] if line[0] == ";" else line
                    profile_title = profile_title.replace("\n", "")
                    profiles.update({profile_title: [line]})
                elif profile_title and profile_title in profiles:
                    profiles[profile_title].append(line)
    except IOError:
        raise Exception(f"{credential_file} is not found.")

    return profiles


def write_aws_profiles(profiles: dict) -> None:
    try:
        with open(credential_file, "w") as file:
            for profile, item in profiles.items():
                file.write("".join(item))
    except IOError:
        raise Exception(f"{credential_file} is not found.")


validate_aws_profile()
profiles = get_aws_profiles()
if len(profiles.keys()) < 1:
    raise Exception(f"Can't not found any aws credential in {credential_file}")

questions = [
    {
        'type': 'list',
        'name': 'profile',
        'message': 'Choose one AWS Profile to set default',
        'choices': profiles.keys(),
    },
    {
        'type': 'confirm',
        'name': 'assume_role',
        'message': 'Do you want to assume role for this profile?(Default false)',
        'default': False,
    },
    {
        'type': 'input',
        'name': 'role_name',
        'message': 'Input your role name to assume role?',
    },
]

answers = prompt(questions, style=custom_style_2)

profile_selected = answers.get('profile')

if profiles[profile_selected][1].find(profile_default_title) != -1:
    print('Selected profile is default already.')
    sys.exit(0)

# Remove origin default profile title and do uncomment
for profile, item in profiles.items():
    if item[1].find(profile_default_title) != -1 and item[0][0] == ";":
        profiles[profile][0] = profiles[profile][0][1:]
        del profiles[profile][1:2]

# Append [default] title to choose profile
profiles[profile_selected][0] = f";{profiles[profile_selected][0]}"
profiles[profile_selected].insert(1, f"{profile_default_title}\n")

write_aws_profiles(profiles)
