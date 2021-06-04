from datetime import timezone, timedelta

import dotenv
import pytest as pytest
from box import Box
from core import firestore_client
from google.cloud.firestore_v1 import Client, DocumentReference, DocumentSnapshot
from mockito import mock

PARIS_TZ = timezone(timedelta(hours=2))


@pytest.fixture(autouse=True)
def setup():
    dotenv.load_dotenv()


@pytest.fixture(autouse=False)
def db(when):
    ret = mock(Client)
    when(firestore_client).db().thenReturn(ret)
    return ret


def test_push_new_account_to_slack(when, db):
    from main import push_new_account_to_slack

    ressource = "pax/auth0|600a84b07038e20071c74950"

    pax_ref_mock = mock(spec=DocumentReference)
    pax_doc_mock = mock({"exists": True}, spec=DocumentSnapshot)
    pax_data_mock = {
        "name": "Name",
        "state": "REGISTERED",
        "preregistration_form_entry_url":
            "https://www.cognitoforms.com/forms/coworkingcoliving30%C3%A8mecielpreregistration/entries/237",
    }
    when(db).document(ressource).thenReturn(pax_ref_mock)
    when(pax_ref_mock).get().thenReturn(pax_doc_mock)
    when(pax_doc_mock).to_dict().thenReturn(pax_data_mock)

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
