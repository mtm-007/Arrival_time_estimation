curl --location 'http://localhost:6789/api/runs'\
--header 'Authorization: Bearer 0584dd355b4046d299869eccc96bd2fe'\
--header 'Content-Type: application/json'\
--header 'Cookie: lng=eng'\
--data '{
    "run": {
        "pipeline_uuid": "predict",
        "block_uuid": "inference",
        "variables": {
            "inputs": [
                {
                    "DOLocationID": "239",
                    "PULocationID": "236",
                    "trip_distance": 1.98
                },
                {
                    "DOLocationID": 170,
                    "PULocationID": 65,
                    "trip_distance": 6.54
                }
            ]
        }
    }
}'


curl --location 'http://localhost:6789/api/runs' \
--header 'Authorization: Bearer 0584dd355b4046d299869eccc96bd2fe' \
--header 'Content-Type: application/json' \
--header 'Cookie: lng=eng' \
--data '{
"run": {
"pipeline_uuid": "predict",
"block_uuid": "inference",
"variables": {
"inputs": [
{
"DOLocationID": "239",
"PULocationID": "236",
"trip_distance": 1.98
},
{
"DOLocationID": 170,
"PULocationID": 65,
"trip_distance": 6.54
}
]
}
}
}'