# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import sys
sys.path.append(r"C:\Users\ASUS\Desktop\RASA\practise")

from excel_data import DataStore


class ActionSayNumber(Action):

    def name(self) -> Text:
        return "action_say_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        number=tracker.get_slot("number")
        if number:
            dispatcher.utter_message(text=f"I remember your number: {number}")
        else:
            dispatcher.utter_message(text="Sorry, I don\'t remember your number")

        return []

class ActionSayExcelInfo(Action):

    def name(self) -> Text:
        return "action_say_excel_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name=tracker.get_slot("user_name")
        number=tracker.get_slot("user_number")
        email=tracker.get_slot("user_email")
        occ=tracker.get_slot("user_occ")
        dispatcher.utter_message("Hi {0}, your contact {1}, your email {2}, occupation {3}".format(name,number,email,occ))
        DataStore(name,number,email,occ)
        dispatcher.utter_message(text="Successful")
        return []

class ActionSayInfo(Action):

    def name(self) -> Text:
        return "action_say_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name=tracker.get_slot("name")
        gender=tracker.get_slot("gender")
        number=tracker.get_slot("number")
        if number and name and gender:
            dispatcher.utter_message(text=f"Hi {name}, your gender: {gender} and your contact number: {number}")
        else:
            dispatcher.utter_message(text="Sorry, I don\'t remember you")

        return []

class ActionResetInfo(Action):

    def name(self) -> Text:
        return "action_reset_info"

    def run(self, dispatcher,
            tracker: Tracker,
            domain):
        
        return [
            SlotSet("name",None),
            SlotSet("number",None),
            SlotSet("gender",None)
        ]

class ValidateInfo(FormValidationAction):

    def name(self) -> Text:
        return "validate_info"

    def validate_number(self, slot_value: Any,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        number=tracker.get_slot("number")
        if (int(len(number))>10 or int(len(number))<10):
            dispatcher.utter_message(text="Invalid number")
            return {"number":None}
        return {"number":number}

class ActionSayWord(Action):

    def name(self) -> Text:
        return "action_word_say"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        word=tracker.get_slot("word")
        if not word:
            dispatcher.utter_message(text="Sorry, no word to find meaning")
            return []
        APP_ID = "f861b796"  # Replace with your actual App ID
        APP_KEY = "76b5f76735954139134d63fb2731bb6c"  # Replace with your actual App Key
        
        language = "en-us"

        url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{language}/{word.lower()}"

        headers={
            "app_id":APP_ID ,
            "app_key":APP_KEY
        }

        try:
            response=requests.get(url,headers=headers)
            response.raise_for_status()
            data=response.json()
            definitions=[]
            examples=[]
            for entry in data.get("results", []):
                for lexical_entry in entry.get("lexicalEntries", []):
                    for sense in lexical_entry.get("entries", [])[0].get("senses", []):
                        # Get definitions
                        if "definitions" in sense:
                            definitions.extend(sense["definitions"])

                        # Get examples
                        if "examples" in sense:
                            for example in sense["examples"]:
                                examples.append(example["text"])
            # Print extracted data
            print("Definitions:")
            for i, definition in enumerate(definitions, 1):
                dispatcher.utter_message(text=f"{i}. {definition}")

            dispatcher.utter_message(text="\nExamples:")
            for i, example in enumerate(examples, 1):
                dispatcher.utter_message(text=f"{i}. {example}")

        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        
        return []
