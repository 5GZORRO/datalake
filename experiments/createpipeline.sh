#!/bin/bash
tmpfile=$(mktemp)
echo "tmpfile = " $tmpfile
echo ' { "userInfo": { "userId": "user2", "authToken": "blah" }, "pipelineDefinition": '  >$tmpfile
cat $1 >>$tmpfile
echo '}' >>$tmpfile
curl -i -H "Content-Type: application/json" -X POST --data "@$tmpfile"  localhost:8080/datalake/v1/pipeline
rm $tmpfile

