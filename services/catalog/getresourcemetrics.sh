curl -i -H "Content-Type: application/json" -X GET -d ' { "userId": '\"$1\"', "authToken": "blah" } ' localhost:8086/datalake/v1/catalog/resource/$2
