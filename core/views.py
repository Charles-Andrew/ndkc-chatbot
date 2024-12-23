from core.messenger import send_message, verify_fb_token, invalid_input
from core.train import chatbot


def receive_message(request):
    if request.method == "GET":
        """
        Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.
        """
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(request=request, token_sent=token_sent)
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                if message.get("message"):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message["sender"]["id"]
                    if message["message"].get("text"):
                        response_sent_text = chatbot(message["message"]["text"])
                        send_message(recipient_id, response_sent_text)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message["message"].get("attachments"):
                        response_sent_nontext = invalid_input()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"
