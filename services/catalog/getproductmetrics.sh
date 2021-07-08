set -x
# Usage: getproductmetrics.sh <user-id> <product-id> <catalog-server-url>
# The catalog-server-url was returned in availableResources in the registerUser API
curl -i -H "Content-Type: application/json" -X GET -d ' { "userId": '\"$1\"', "authToken": "blah" } ' $3/datalake/v1/catalog/product/$2
