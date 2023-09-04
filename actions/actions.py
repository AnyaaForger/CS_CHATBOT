# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted

from store_read_data import DataRead, DataStore, StoreDataDB, ReadDataDB, ReadDataMembershipType
from decimal import Decimal

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class FormDataCollection(Action):
    def name(self) -> Text:
        return "action_data_collection"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        number = tracker.get_slot("number")
        email = tracker.get_slot("email")
        city = tracker.get_slot("city")
        print(name, number, email,city)
        # if not phone:
        #     dispatcher.utter_message(text="Sorry I don't have your phone number!")
        # else:
        dispatcher.utter_message(text=f"Hey {name}, here are the information that you provided. Do you want to save it?\nName: {name}, \nNumber: {number},\nEmail: {email},\nCity: {city}")

        return []

class ActionSaveData(Action):

    def name(self) -> Text:
        return "action_save_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        number = tracker.get_slot("number")
        email = tracker.get_slot("email")
        city = tracker.get_slot("city")
        print("Action Save Data...")
        # DataStore(name, number, email, city)
        StoreDataDB(name, number, email, city, "prospect_member")
        dispatcher.utter_message(text="Data Anda sudah berhasil kami simpan. Selanjutnya bagaimana saya bisa membantu Anda?")

        return []
    
class ActionReadData(Action):

    def name(self) -> Text:
        return "action_read_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("READ DATA: ")
        # print(tracker.latest_message['entities'][0]['value'])
        # print(tracker.latest_message['entities'][1]['value'])
        # output = DataRead(tracker.latest_message['entities'][0]['value'],
        #                   tracker.latest_message['entities'][1]['value'])
        output = ReadDataDB(tracker.latest_message['entities'][0]['value'],
                            tracker.latest_message['entities'][1]['value'],
                            "personal_data")
        print(output)
        dispatcher.utter_message(text="This is the data that you asked for, \n{}".format(",".join(output)))

        return []
    
class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"
    
    def run(self, dispatcher, tracker, domain):
        print("Reset Slot...")
        return [AllSlotsReset()]
    
class ActionReadMembershipType(Action):

    def name(self) -> Text:
        return "action_read_membership_type"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("READ DATA: ")
        membership_type = tracker.latest_message['entities'][0]['value']
        output = ReadDataMembershipType(membership_type, "gym_membership")
        print("output: ")
        print(output)
        if(len(output) >= 4):
            id, name, price, session = output
            print(float(price))
            dispatcher.utter_message(text=f"Pilihan yang sangat bagus! Keanggotaan {name} kami mencakup seluruh akses ke fasilitas gym kami, kelas eksklusif, dan jam operasional yang lebih lama.\nDengan harga Rp{price}/bulan dan sesi gratis dengan coach selama {session} jam.")
        else:
            dispatcher.utter_message(text=f"Tipe membership {membership_type} belum tersedia di gym kami...")
        
        return []
    
class ActionRestart(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]