#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2
import re
from pathlib import Path
import sys

# credential_file = f"{Path.home()}/.aws/credentials"
credential_file = "./credentials_sample"


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


def get_aws_profile_list() -> list:

    profile_titles = []
    try:
        with open(credential_file, "r") as file:
            lines = file.readlines()
            re_profile = re.compile("\[.+\]")
            for line in lines:
                if re_profile.match(line):
                    profile_titles.append(line)
    except IOError:
        raise Exception(f"{credential_file} is not found.")

    return profile_titles


questions = [
    {
        'type': 'list',
        'name': 'profile',
        'message': 'Choose one AWS Profile to set default',
        'choices': get_aws_profile_list()
    },
    {
        'type': 'confirm',
        'name': 'assume_role',
        'message': 'Do you want to assume role for this profile?(Default false)',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'default': False,
    },
    {
        'type': 'input',
        'name': 'role_name',
        'message': 'Input your role name to assume role?',
    },
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)
