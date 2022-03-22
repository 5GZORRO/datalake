set -x
# Usage: registertransaction.sh <user-id> <transaction-id> <server-url> <kafka_topic>
curl -i -H "Content-Type: application/json" -X POST -d ' { "userInfo": { "userId": '\"$1\"', "authToken": "blah" }, "transactionInfo": { "topic": '\"$4\"' } } ' $3/datalake/v1/stream_data/register/$2
