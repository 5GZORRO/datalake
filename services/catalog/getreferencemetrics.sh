set -x
curl -i -H "Content-Type: application/json" -X GET -d ' { "userId": '\"$1\"', "authToken": "blah" } ' $3/datalake/v1/catalog/reference/$2
