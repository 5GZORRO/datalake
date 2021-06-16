set -x
# Usage: getinstancemetrics.sh <user-id> <instance-id> <catalog-server-url>
# The catalog-server-url was returned in availableResources in the registerUser API
curl -i -H "Content-Type: application/json" -X GET -d ' { "userId": '\"$1\"', "authToken": "blah" } ' $3/datalake/v1/catalog/instance/$2
