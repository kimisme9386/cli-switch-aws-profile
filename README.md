# Switch AWS Profile on local

[![Deploy](https://github.com/kimisme9386/cli-switch-aws-profile/actions/workflows/deploy.yml/badge.svg)](https://github.com/kimisme9386/cli-switch-aws-profile/actions/workflows/deploy.yml)

![demo-swtich-aws-profile](https://user-images.githubusercontent.com/7465652/125384155-0ebbff80-e3cb-11eb-893d-4bae4d252663.gif)

Choose one AWS profile to set default when you have multiple AWS profile.

Typically, the location of credential file is ` ~/.aws/credentials`

## Feature

- Switch AWS profile for setting default
- Assume role for getting credential base on choosing AWS profile

## prerequisites

- Python3
- jq

## Credential file examples

No Assume role

```
[test1]
aws_access_key_id = AKI11111111111111111
aws_secret_access_key = aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb

[test2]
aws_access_key_id = AKI22222222222222222
aws_secret_access_key = cccccccccccccccccccccccdddddddddddddddddd
```

Assume role

```
[test1]
aws_access_key_id = AKI11111111111111111
aws_secret_access_key = aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbb
custom_assume_role = ci-assume-role1
duration_seconds = 3600

[test2]
aws_access_key_id = AKI22222222222222222
aws_secret_access_key = cccccccccccccccccccccccdddddddddddddddddd
custom_assume_role = ci-assume-role2
duration_seconds = 3600
```

If custom_assume_role is specified, the question as `Input your role name to assume role` can be pressed enter to pass it directly.

`duration_seconds` setting same as the custom_assume_role.
