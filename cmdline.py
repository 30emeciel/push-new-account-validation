import logging
from dotmap import DotMap

log = logging.getLogger(__name__)

if __name__ == "__main__":
    # export GOOGLE_APPLICATION_CREDENTIALS="trentiemeciel.json"
    # get the token using postman
    from dotenv import load_dotenv
    load_dotenv()
    import main

    context = DotMap({
        "resource": "projects/trentiemeciel/databases/(default)/documents/pax/auth0|5fff7ebfb10fa3006fc74728"
    })
    main.from_firestore({}, context)
