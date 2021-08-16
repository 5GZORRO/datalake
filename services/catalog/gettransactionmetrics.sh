set -x
# Usage: gettransactionmetrics.sh <user-id> <transaction-id> <catalog-server-url>
# The catalog-server-url was returned in availableResources in the registerUser API
curl -i -H "Content-Type: application/json" -X GET -d ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" } } ' $3/datalake/v1/catalog/transaction/$2
