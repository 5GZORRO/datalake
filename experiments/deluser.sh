curl -i -H "Content-Type: application/json" -X DELETE -d ' { "userId": '\"$1\"', "authToken": "blah" } ' localhost:8080/datalake/v1/user
