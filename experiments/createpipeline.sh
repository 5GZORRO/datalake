#!/bin/bash
tmpfile=$(mktemp)
echo "tmpfile = " $tmpfile
echo ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" }, "pipelineDefinition": '  >$tmpfile
cat $2 >>$tmpfile
echo '}' >>$tmpfile
curl -i -H "Content-Type: application/json" -X POST --data "@$tmpfile"  localhost:8080/datalake/v1/pipeline
rm $tmpfile

