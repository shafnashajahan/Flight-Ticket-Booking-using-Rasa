# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import sys
import numpy as np
sys.path.append('..')
from Flights_API import amadeus

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
# from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class Actionsayname(Action):

    def name(self) -> Text:
        return "action_sayname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # text = tracker.latest_message['text']

        current_name = next(tracker.get_latest_entity_values("name"), None)
        # print(current_name)

        if not current_name:
            msg = f"Name not recognized. Please enter properly"
            # print(msg)
            dispatcher.utter_message(text = msg)
            return []
        
        msg = f"Hey {current_name}. Nice to see you!"
        # print(msg)
        dispatcher.utter_message(text = msg)

        return [SlotSet("name", current_name)]
        # return [SlotSet("name", text)]

class Actiondisplay(Action):

    def name(self) -> Text:
        return "action_display"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")

        if not name:
            msg = f"oops. Please enter properly"
            # print(msg)
            dispatcher.utter_message(text = msg)
            return []
        
        msg = f"Repeated: Your name is {name}. Nice to see you!"
        # print(msg)
        dispatcher.utter_message(text = msg)

        return []

class Actionshowpreview(Action):
    def name(self) -> Text:
        return "action_show_preview"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        all_names_list = tracker.get_slot("all_names")
        contact_number = int(tracker.get_slot("contact_number"))
        originLocationName = tracker.get_slot("from_location")
        destinationLocationName = tracker.get_slot("to_location")
        departureDate = tracker.get_slot("departureDate")
        returnDate = tracker.get_slot("returnDate")
        adults = int(tracker.get_slot("adults"))
        nonStop = tracker.get_slot("nonStop")
        budget = int(tracker.get_slot("maxPrice"))

        budget = str(budget)
        num_of_tickets = str(adults)
        nonStop = str(nonStop).lower()
        

        final_response = amadeus.run(
            originLocationName = originLocationName,
        destinationLocationName = destinationLocationName,
        departureDate = departureDate,
        returnDate = returnDate,
        adults = adults,
        nonStop = nonStop,
        maxPrice = budget)

        preview_message = f'We have received the info for {num_of_tickets} tickets as requested by you\n'
        preview_message += 'These are names of ticket holders\n'
        # all_names = all_names.split(';')
        # all_names_list = all_names.split(';')
        # all_names_list.pop()
        for i, name in enumerate(all_names_list):
            preview_message += f'{i+1}. {name}\n'
        preview_message += f'\ncontact number : {contact_number}\n'
        preview_message += '\nHere is the preview for the complete journey of any one of you\n'
        # #for loop
        # for ticket_id in range(0, num_of_tickets):
        for ticket_id in range(0,1):
            num_of_directions = len(final_response['data'][ticket_id]['direction'])
            for direction in range(num_of_directions):
                num_of_segments = len(final_response['data'][ticket_id]['direction'][direction]['segment'])
                for segment in range(num_of_segments):
                    segment_response = final_response['data'][ticket_id]['direction'][direction]['segment'][segment]
                    sr = segment_response
                    origin, destination, origin_iata_code, destination_iata_code, departure_date, departure_time, \
                        arrival_date, arrival_time, price, flight_code, aircraft_code, duration, \
                            num_of_stops, cabin, origin_airportname, destination_airportname, origin_GMT, destination_GMT, \
                                numberOfBookableSeats, gate_number, seat_number = \
                    sr['origin'], sr['destination'], sr['origin_iata_code'], sr['destination_iata_code'], sr['departure_date'], sr['departure_time'], \
                        sr['arrival_date'], sr['arrival_time'], np.round(sr['price'], 1), sr['flight_code'], sr['aircraft_code'], sr['duration'], \
                            sr['num_of_stops'], sr['cabin'],sr['origin_airportname'], sr['destination_airportname'], sr['origin_GMT'], sr['destination_GMT'], \
                                sr['numberOfBookableSeats'], sr['gate_number'], sr['seat_number']
                    preview_message += f'Segment {segment + 1}\n'
                    preview_message += f'origin            : {origin}\n'
                    preview_message += f'destination       : {destination}\n'
                    preview_message += f'departure_date    : {departure_date}\n'
                    preview_message += f'departure_time    : {departure_time}\n'
                    preview_message += f'arrival_date      : {arrival_date}\n'
                    preview_message += f'arrival_time      : {arrival_time}\n'
                    # preview_message += f'price             : {price}\n'
                    preview_message += f'flight_code       : {flight_code}\n'
                    preview_message += f'aircraft_code     : {aircraft_code}\n'
                    preview_message += f'duration          : {duration}\n'
                    # preview_message += f'num_of_stops      : {num_of_stops}\n'
                    preview_message += f'cabin             : {cabin}\n'
                    preview_message += f'origin_GMT        : {origin_GMT}\n'
                    preview_message += f'destination_GMT   : {destination_GMT}\n'
                    preview_message += f'gate_number       : {gate_number}\n'
                    preview_message += f'seat_number       : {seat_number}\n'
                    preview_message += f'origin_airportname: {origin_airportname}\n'
                    preview_message += f'origin_iata_code  : {origin_iata_code}\n'
                    preview_message += f'destination_airportname: {destination_airportname}\n'
                    preview_message += f'destination_iata_code  : {destination_iata_code}\n'
                    preview_message += f'numberOfBookableSeats  : {numberOfBookableSeats}\n\n'
        
        preview_message += f'Total number of stops in your journey : {num_of_stops}\n'
        preview_message += f'Your grand total is Rs. {price}'
        
        dispatcher.utter_message(text=preview_message)
        
        confirm_message = "Congrats.!!! Payment successfull"

        return[SlotSet('confirm_message', confirm_message)]

class ActionAskFullName(Action):
    def name(self) -> Text:
        return "action_ask_full_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        all_names_list = tracker.get_slot("all_names")
        adults = int(tracker.get_slot("adults"))
        
        if adults == 1:
            dispatcher.utter_message(text="Please provide your full name")
        elif all_names_list == None:
            dispatcher.utter_message(text=f"Please provide full name of Passenger 1")
        else:
            dispatcher.utter_message(text=f"Please provide full name of Passenger {len(all_names_list) + 1}")
            
        return[]

class ActionSetBeginStatusTrue(Action):
    def name(self) -> Text:
        return "action_set_begin_status_true"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return[SlotSet("begin_status", True)]

class Actionqueryfresh(Action):

    def name(self) -> Text:
        return "action_query_fresh"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
    

class Actiongetnames(Action):
    def name(self) -> Text:
        return "action_get_names"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num_of_tickets = tracker.get_slot("adults")
        num_of_tickets = int(num_of_tickets)
        full_name = tracker.get_slot("full_name")

        all_names_list = tracker.get_slot("all_names")
        if all_names_list == None:
            all_names_list = []

        all_names_list.append(full_name)        

        # all_names_list = all_names.split(';')
        # all_names_list.pop()
        print("all names", all_names_list, "\nnum tickets", num_of_tickets)
        traveller_no = len(all_names_list)
        if traveller_no == num_of_tickets:
            return[SlotSet("full_name", None), SlotSet("all_names", all_names_list), SlotSet("stored_all_names", True)]
        else:
            return[SlotSet("full_name", None), SlotSet("all_names", all_names_list), SlotSet("stored_all_names", False)]
