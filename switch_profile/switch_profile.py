#!/usr/bin/env python3

import pathlib
import re
import subprocess
import sys
from typing import Tuple

from PyInquirer import prompt
from examples import custom_style_2

credential_file = f"{pathlib.Path.home()}/.aws/credentials"
# credential_file = f"{pathlib.Path(__file__).parents[1]}/credentials_sample"
profile_default_title = "[default]"
profile_default_title_name = "default"

assume_role_key = 'custom_assume_role'
assume_role_profile_name = '[custom_assume_role]'


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
            if m and m.group(1) == assume_role_key:
                continue
            elif m and m.group(1) != profile_default_title_name:
                profile_title = line[1:] if line[0] == ";" else line
                profile_title = profile_title.replace("\n", "")
                profiles.update({profile_title: [line]})
            elif profile_title and profile_title in profiles:
                profiles[profile_title].append(line)

    return profiles


def change_default_profile(profiles: dict, profile_selected: str, profile_default_title: str) -> None:
    # Remove origin default profile title and do uncomment
    for profile, item in profiles.items():
        if item[1].find(profile_default_title) != -1 and item[0][0] == ";":
            profiles[profile][0] = profiles[profile][0][1:]
            del profiles[profile][1:2]

    # Append [default] title to choose profile
    profiles[profile_selected][0] = f";{profiles[profile_selected][0]}"
    profiles[profile_selected].insert(1, f"{profile_default_title}\n")


def write_aws_profiles(profiles: dict) -> None:
    with open(credential_file, "w") as file:
        for profile, item in profiles.items():
            file.write("".join(item))


def execute_assume_role(role: str) -> Tuple[str, bool]:
    bash_file = f"{pathlib.Path(__file__).parents[1]}/assume-role.sh"
    process = subprocess.Popen(['sh', bash_file, role],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        return stderr.decode("utf-8"), True

    return stdout.decode("utf-8"), False


def get_selected_profile_role_name(profile_content: list) -> str:
    for content in profile_content:
        if content.find("=") == -1:
            continue
        key, value = content.split("=")
        if str(key).strip() == assume_role_key:
            return str(value).strip()

    return ''


def add_assume_role_default_profile(
        profiles: dict,
        profile_default_title: str,
        assume_role_profile_name: str,
        assume_role_profile_content: str
) -> None:
    # Remove origin default profile title and do uncomment
    for profile, item in profiles.items():
        if item[1].find(profile_default_title) != -1 and item[0] == f";{assume_role_profile_name}":
            del profiles[profile]

        elif item[1].find(profile_default_title) != -1 and item[0][0] == ";":
            profiles[profile][0] = profiles[profile][0][1:]
            del profiles[profile][1:2]

    # Append assume role profile title to file
    content = [f";{assume_role_profile_name}\n", f"{profile_default_title}\n", assume_role_profile_content]
    profiles.update({assume_role_profile_name: content})


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
    is_assume_role = answers.get('assume_role')

    profile_selected = answers.get('profile')

    if profiles[profile_selected][1].find(profile_default_title) != -1:
        if is_assume_role is False:
            print('Selected profile is default already.')
            sys.exit(0)
    else:
        change_default_profile(profiles, profile_selected, profile_default_title)
        write_aws_profiles(profiles)

    if is_assume_role:
        role_name = (answers.get('role_name') if answers.get('role_name')
                     else get_selected_profile_role_name(profiles[profile_selected]))

        output, err = execute_assume_role(role_name)
        if err:
            print(output)
            sys.exit(0)

        add_assume_role_default_profile(profiles, profile_default_title, assume_role_profile_name, output)
        write_aws_profiles(profiles)

        print('Use "aws sts get-caller-identity" to identify who you are.\n')
