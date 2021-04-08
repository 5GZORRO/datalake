#!/bin/bash
tmpfile=$(mktemp)
echo "tmpfile = " $tmpfile
echo ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" }, "deploymentDefinition": '  >$tmpfile
cat $2 >>$tmpfile
echo ', "serviceDefinition": ' >>$tmpfile
cat $3 >>$tmpfile
echo '}' >>$tmpfile
curl -i -H "Content-Type: application/json" -X POST --data "@$tmpfile"  localhost:8080/datalake/v1/service
rm $tmpfile

