set -x
# Usage: registerproduct.sh <user-id> <product-id> <server-url> <kafka_topic>
curl -i -H "Content-Type: application/json" -X POST -d ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" }, "productInfo": { "topic": '\"$4\"' } } ' $3/datalake/v1/stream_data/register/$2
