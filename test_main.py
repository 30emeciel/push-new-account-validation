from unittest import TestCase

import dotenv
from box import Box


class Test(TestCase):
    def setUp(self) -> None:
        dotenv.load_dotenv()

    def test_push_new_account_to_slack(self):
        from main import push_new_account_to_slack

        ressource = "pax/auth0|600a84b07038e20071c74950"

        event = {
            "oldValue": {
                "createTime": "2021-03-05T19:54:37.991311Z",
                "fields": {
                    "arrival_date": {"timestampValue": "2021-03-15T23:00:00Z"},
                    "created": {"timestampValue": "2021-03-05T19:54:37.978Z"},
                    "departure_date": {"timestampValue": "2021-03-19T23:00:00Z"},
                    "kind": {"stringValue": "COLIVING"},
                    "number_of_nights": {"integerValue": "4"},
                    "state": {"stringValue": "PENDING_REVIEW"}
                },
                "name": "projects/trentiemeciel/databases/(default)/documents/pax/auth0|600a84b07038e20071c74950",
                "updateTime": "2021-03-05T21:56:55.248879Z"
            },
            "updateMask": {"fieldPaths": ["state"]},
            "value": {
                "createTime": "2021-03-05T19:54:37.991311Z",
                "fields": {
                    "arrival_date": {"timestampValue": "2021-03-15T23:00:00Z"},
                    "created": {"timestampValue": "2021-03-05T19:54:37.978Z"},
                    "departure_date": {"timestampValue": "2021-03-19T23:00:00Z"},
                    "kind": {"stringValue": "COLIVING"},
                    "number_of_nights": {"integerValue": "4"},
                    "state": {"stringValue": "CANCELED"}
                },
                "name": "projects/trentiemeciel/databases/(default)/documents/pax/auth0|600a84b07038e20071c74950",
                "updateTime": "2021-03-05T21:56:55.248879Z"
            }
        }
        push_new_account_to_slack(ressource, Box(event))
