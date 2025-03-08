import requests
import speech_recognition as sr
import pyttsx3
import re

#Taking user input
print("Starting the conversation")
r=sr.Recognizer();
bot_message=""
engine= pyttsx3.init()
while bot_message!="Bye":
    with sr.Microphone() as source:
        print("Please speak")    
        audio=r.listen(source)
        print("Got your message")
        try:
            message=r.recognize_google(audio)
            if re.search(r'\d', message):
                message= re.sub(r'(?<=\d) (?=\d)', '', message)
            print("You said {}".format(message))
        except:
            print("Sorry, cannot get your voice")

    if (len(message)==0):
        continue
    print("Sending....")
    try:
        response=requests.post("http://localhost:5005/webhooks/rest/webhook",
                    json={"message": message},
                    timeout=5)
        if response.status_code == 200:
                bot_messages = response.json()
                if bot_messages:
                    print("Bot says: ", end=" ")
                    for i in bot_messages:
                        bot_message=i.get("text","No response")
                        print(bot_message)
                        engine.say(bot_message)
                        engine.runAndWait()
                else:
                    print("Bot did not respond. Please try again.")
        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.Timeout:
        print(" Error: Request timed out. The server is not responding.")

    except requests.exceptions.ConnectionError:
        print(" Error: Could not connect to the Rasa server. Is it running?")

    except requests.exceptions.RequestException as e:
        print(f" Error: {e}")

