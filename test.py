from train import chatbot

while True:
    x = input("You: ")
    y = chatbot(x)
    print(y)