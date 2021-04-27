import logging

from box import Box
from core.firestore_client import db
from core.slack_message import send_slack_message
from core.tpl import render

log = logging.getLogger(__name__)


def from_firestore(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    resource_string = context.resource

    # print out the resource string that triggered the function
    log.debug(f"Function triggered by change to: {resource_string}.")
    # now print out the entire event object
    # print(str(data))

    push_new_account_to_slack(resource_string, Box(event))


def push_new_account_to_slack(docpath, event):

    if "state" not in event.updateMask.fieldPaths:
        log.info("state hasn't changed, ignoring")
        return

    pax_ref = db.document(docpath)
    pax_doc = pax_ref.get()
    assert pax_doc.exists
    pax = Box(pax_doc.to_dict())
    if pax.state != "REGISTERED":
        log.info(f"pax {pax.sub} has 'state' set to REGISTERED, ignoring")
        return

    data = {
        "pax": pax
    }
    slack_message = render("preregistration_completed_fr.txt", data)
    send_slack_message(slack_message)

