#!/bin/sh

set -euo pipefail

sam deploy \
        --stack-name serverless-template-python-ci \
        --template-file ci.yaml \
        --capabilities CAPABILITY_IAM \
        --no-fail-on-empty-changeset

echo
echo Stack deployed as serverless-template-python-ci
echo
