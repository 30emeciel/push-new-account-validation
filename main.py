from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import google
from os import environ
import requests
from dotmap import DotMap
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "trentiemeciel",
})


log = logging.getLogger(__name__)


db = firestore.Client()
slack = WebClient(token=environ['SLACK_BOT_TOKEN'])


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

    push_new_account_to_slack(resource_string)


def push_new_account_to_slack(docpath):
    pax_ref = db.document(docpath)
    pax_doc = pax_ref.get()
    assert pax_doc.exists
    pax_data = DotMap(pax_doc.to_dict(), _dynamic=False)
    if pax_data.state != "REGISTERED":
        log.info(f"pax {pax_data.sub} has 'state' set to REGISTERED, ignoring")
        return

    text = f"""\
*{pax_data.name}* vient juste de se préinscrire 😋!\n
Tu peux voir les informations de sa préinscription avec <{pax_data.preregistration_form_entry_url}|ce lien>\n
Tu peux récupérer le mot de passe du compte CognitoForms du 30ème Ciel dans \
<https://docs.google.com/document/d/16VcFJkATwBJe9EmOKfD0peiIzY6bK2bJDTO7x9D6Qxo/edit?usp=sharing|ce document>"""
    slack.chat_postMessage(
        channel='null',
        text=text,
        link_names=False,
        attachments=[]
    )

