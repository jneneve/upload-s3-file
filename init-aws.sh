#!/bin/bash

set -e

# Creat local S3 bucket using AWS CLI
awslocal s3api create-bucket --bucket localstack-bucket