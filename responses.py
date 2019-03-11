from system_properties import WEBSITE_ROOT, DEFAULT_WEBSITE_ROOT
from commands import WELCOME_COMMAND, HELP_COMMAND, WEBSITE_LINK, DETAILS

WELCOME_MESSAGE = "Hi %s! I'm the Carrecognizer chatbot, send me images about cars and I can tell you the make and the model plus lot of other useful stuff"

ERROR_MESSAGE = "Sorry, I don't get this. The available commands are : " \
                + WELCOME_COMMAND + "\n" \
                + HELP_COMMAND + "\n" \
                + WEBSITE_LINK + "\n" \
                + DETAILS \
                + "\n Or send an image about a car"

NOT_IMPLEMENTED_YET = "Sorry, this function is not ready yet, try again later!"

HELP_RESPONSE = "The availabile commands are " \
                + WELCOME_COMMAND + " - Greetings!" \
                + WEBSITE_LINK + " - Get a link to the website" \
                + DETAILS + " - Get details about the last classification" \
                + "Or send an image about a car, and I will the you the make and the model plus lot more interesting stuff"

WEBSITE_RESPONSE = WEBSITE_ROOT if WEBSITE_ROOT is not None else DEFAULT_WEBSITE_ROOT

SUCCESSFUL_IMAGE_RECOGNITION_RESPONSE = "Nice car, it seems to be a %s %s."
ERROR_IMAGE_RECOGNITION_RESPONSE = "Sorry I didn't recognize this image, could you please send me an another from a different angle?"

CLASSIFICATION_STARTED = "Classification started, this can take some time.."
TO_MANY_ATTACHMENTS = "You send to many attachments, I will classify the first one!"
TO_LITTLE_ATTACHMENTS = "Wow I don't know how did you not sent any attachments.."
BAD_ATTACHMENT_TYPE = "Please send me image"
UNKNOWN_CLASSIFICATION_ERROR = "Oppsie, unexpected error occurred while classification"
AUTHENTICATION_ERROR = "Authentication failed"
