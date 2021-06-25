#!/usr/bin/env bash

ASSUME_ROLE_NAME=$1
DURATION_SECONDS=$2
sts_session_name=chris-mac-desktop

accountid=$(aws sts get-caller-identity | jq -r .Account)
temp_role=$(aws sts assume-role --role-arn arn:aws:iam::${accountid}:role/${ASSUME_ROLE_NAME} --role-session-name ${sts_session_name} --duration-seconds ${DURATION_SECONDS:=28800})
AWS_ACCESS_KEY_ID=$(echo $temp_role | jq -r .Credentials.AccessKeyId)
AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq -r .Credentials.SecretAccessKey)
AWS_SESSION_TOKEN=$(echo $temp_role | jq -r .Credentials.SessionToken)

if [ -z ${AWS_ACCESS_KEY_ID} ]; then
  exit 1
fi

echo 'aws_access_key_id = '${AWS_ACCESS_KEY_ID}
echo 'aws_secret_access_key = '${AWS_SECRET_ACCESS_KEY}
echo 'aws_session_token = '${AWS_SESSION_TOKEN}
echo 'assume_role_name ='${ASSUME_ROLE_NAME}
echo 'duration_seconds ='${DURATION_SECONDS}
