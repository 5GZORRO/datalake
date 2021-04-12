curl -i -H "Content-Type: application/json" -X DELETE -d \
	' { "userInfo" : { "userId": '\"$1\"', "authToken": "blah" }, "serviceId": '\"$2\"' } ' \
	localhost:8080/datalake/v1/service
