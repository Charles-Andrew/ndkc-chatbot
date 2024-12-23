import random
from django.conf import settings
from pymessenger.bot import Bot

ACCESS_TOKEN = settings.ACCESS_TOKEN
VERIFY_TOKEN = settings.VERIFY_TOKEN
bot = Bot(ACCESS_TOKEN)


def verify_fb_token(request, token_sent):
    """
    Take token sent by facebook and verify it matches the verify token you sent
    if they match, allow the request, else return an error
    """
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"


def invalid_input():
    sample_responses = [
        "Im sorry, I only accept text.",
        "Sorry, I dont process other types except for texts.",
        "I cant do anything with that Iam Sorry :(",
        "I am not designed to handle that kind of input, Sorry :(",
    ]
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    """
    Uses PyMessenger to send response to user
    sends user the text message provided via input response parameter
    """
    bot.send_text_message(recipient_id, response)
    return "success"

