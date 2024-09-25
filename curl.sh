#!/bin/bash

# This is a bash script to make an HTTP GET request using curl

URL='https://datastax-cluster-config-prod.s3.us-east-2.amazonaws.com/02315dc7-1da5-4054-8339-c6e0007d01f0-1/secure-connect-backorderdb.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2AIQRQ76XML7FLD6%2F20240914%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20240914T111828Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=12052de416f2cc8eb7b45b28125fc71df77edeab00bb5a7ff4e92e2df8488788'
RESPONSE=$(curl -o secure-connect-backorderdb.zip $URL)

# Check if the curl request was successful (HTTP 200)
if [ $RESPONSE -eq 200 ]; then
    echo "Request was successful!"
else
    echo "Request failed with status code: $RESPONSE"
fi
