from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='switch-aws-profile',
    version='0.0.3',
    author='Chris Yang',
    author_email='kimisme9386@gmail.com',
    license='MIT',
    description='Switch AWS profile on local',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kimisme9386/cli-switch-aws-profile',
    py_modules=['switch_profile'],
    packages=find_packages(),
    install_requires=['pyinquirer==1.0.3'],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        awssp=switch_profile.app:main
    ''',
    package_dir={'switch_profile': 'switch_profile'},
    package_data={'switch_profile': ['scripts/*.sh']},
)
