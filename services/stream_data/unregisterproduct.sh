set -x
# Usage: unregisterproduct.sh <user-id> <product-id> <server-url>
curl -i -H "Content-Type: application/json" -X POST -d ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" } } ' $3/datalake/v1/stream_data/unregister/$2
