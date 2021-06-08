#!/usr/bin/env python3

import pathlib
import re
import sys

from PyInquirer import prompt
from examples import custom_style_2

# credential_file = f"{pathlib.Path.home()}/.aws/credentials"
credential_file = f"{pathlib.Path(__file__).parents[1]}/credentials_sample"
profile_default_title = "[default]"
profile_default_title_name = "default"


def validate_aws_profile(credential_file: str):
    with open(credential_file, "r") as file:
        lines = file.readlines()
        prev_line = ""
        for line in lines:

            m = re.match(r";?\[(\w+)\]", line)
            if m and m.group(1) == profile_default_title_name and (len(prev_line) < 1 or prev_line[0] != ";"):
                raise Exception("Found 'default' profile, please rename it.")

            prev_line = line


def get_aws_profiles(credential_file: str) -> dict:
    profiles = dict()
    profile_title = ""
    with open(credential_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            m = re.match(r";?\[(\w+)\]", line)
            if m and m.group(1) != profile_default_title_name:
                profile_title = line[1:] if line[0] == ";" else line
                profile_title = profile_title.replace("\n", "")
                profiles.update({profile_title: [line]})
            elif profile_title and profile_title in profiles:
                profiles[profile_title].append(line)

    return profiles


def write_aws_profiles(profiles: dict) -> None:
    with open(credential_file, "w") as file:
        for profile, item in profiles.items():
            file.write("".join(item))


if __name__ == '__main__':
    validate_aws_profile(credential_file)
    profiles = get_aws_profiles(credential_file)
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
            'when': lambda answers: answers['assume_role']
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
