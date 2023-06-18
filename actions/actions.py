# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from pythonScript import usrModel
import random
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, FollowupAction, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher



"""
This is the custom action for 'repeat' intent. 
If the user is not paying attention, asks the robot to speak again, repeating the previous output.
"""
class ActionRepeat(Action):
    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):
        name_slot = tracker.get_slot('PERSON')
        memoryList = "$Set the user as *%s*$ @Set the user as *%s*@ &Set the user as *%s*&" % (name_slot, name_slot, name_slot)
        text = "$Hi! Welcome to cognitive exercises! Are you ready?$ @Hi! Welcome! Ready to start?@ &Hi! Are you ready?&"
        for event in tracker.events:
            if (event.get("event") == "bot") and (event.get("event") is not None):
                text = event.get("text")
        if text == memoryList:
            text = "$Hi! Welcome to cognitive exercises! Are you ready?$ @Hi! Welcome! Ready to start?@ &Hi! Are you ready?&"
        dispatcher.utter_message(text)
        return []


"""
This is the custom action for 'set_usr' intent. 
At the beginning of the test, when the tester tells the robot the name of the user he wants to test, 
store that username as a slot.
"""
class ActionSetUser(Action):

    def name(self) -> Text:
        return "set_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_slot = tracker.get_slot('PERSON')
        user = None
        for eachUser in usrModel.usrModel:
            if eachUser['name'] == name_slot:
                dispatcher.utter_message(text="$Set the user as *"+ name_slot + "*$ @Set the user as *"+ name_slot + "*@ &Set the user as *"+ name_slot + "*&")
                user = name_slot


        if name_slot is None:
            dispatcher.utter_message(text="&I can not extract the name. Tell me your name?&@I can not extract the name. Tell me your name?@ &I can not extract the name. Tell me your name?&")
            return []

        if user is None:
            dispatcher.utter_message(text="&You are not in our user database.&@You are not in our user database.@ &You are not in our user database.&")
            return [SlotSet("PERSON", True)]

        return []



"""
This is the custom action if the user finishes Math test. 
Submit the form and reset all slots.
"""
class ActionSubmitMathForm(Action):

    def name(self) -> Text:
        return "Submit_math_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        string_out = "$Ok. Thanks for taking this math test!$ @Thanks for the math test!@ &Thanks!&"
        dispatcher.utter_message(text=string_out)
        return [SlotSet("math_answer", None), SlotSet("NUMBER", None), SlotSet("quit", None)]



"""
This is the custom action to generate math questions if the user chooses a math test. 
Generate the math question based on the cognitive exercise level.
"""
class AskForNUMBERAction(Action):
    def name(self) -> Text:
        return "action_ask_NUMBER"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        name_slot = tracker.get_slot('PERSON')
        cogLevel = 0
        for eachUser in usrModel.usrModel:
            if eachUser['name'] == name_slot:
                cogLevel = eachUser['cognitive']
        if cogLevel == 2:
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
            answer = num1 + num2
            string_out = "$What is the result of %s plus %s?$ @The result of %s plus %s?@ &%s plus %s?&" % (num1, num2, num1, num2,num1,num2)
            dispatcher.utter_message(text=string_out)
            return [SlotSet("math_answer", answer)]
        elif cogLevel ==1:
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
            answer = num1 * num2
            string_out = "$What is the result of %s times %s?$ @The result of %s times %s?@ &%s times %s?&" % (num1, num2,num1,num2,num1,num2)
            dispatcher.utter_message(text=string_out)
            return [SlotSet("math_answer", answer)]
        else:
            num1 = random.randint(7, 10)
            num2 = random.randint(7, 10)
            answer = num1 * num2
            string_out = "$What is the result of %s times %s?$ @The result of %s times %s?@ &%s times %s?&" % (num1, num2,num1,num2,num1,num2)
            dispatcher.utter_message(text=string_out)
            return [SlotSet("math_answer", answer)]


"""
This is a custom action that verifies that all required slots in the math form are filled.
Validate the answer user has given.
Validate if user wants to quit.
"""
class ValidateMathForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_math_form"

    def validate_NUMBER(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        answer = int(tracker.get_slot('math_answer'))
        number = int(slot_value)
        if number == answer:
            string_out = "$Correct! You win this game!$ @Correct!You win!@ &You win!&"
            dispatcher.utter_message(text=string_out)
        else:
            string_out = "$sorry you lost the game.$ @Sorry You lost!@ &You lost!&"
            dispatcher.utter_message(text=string_out)
        return {"NUMBER": number}

    def validate_quit(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value:
            dispatcher.utter_message(text="$Great! Let us continue!$ @OK! let us go!@ &OK!&")
            return {"NUMBER": None, "quit": None}
            # return {"quit": True}
        else:
            return {"quit": False}

"""
This is the custom action if the user finishes memory test. 
Submit the form and reset all slots.
"""
class ActionSubmitMemoryForm(Action):

    def name(self) -> Text:
        return "Submit_memory_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        string_out = "$Ok. Thanks for taking this memory test!$ @Thanks for participating!@ &OK! Thanks!&"
        dispatcher.utter_message(text=string_out)
        return [SlotSet("color_answer", None), SlotSet("COLOR", None), SlotSet("quit", None)]



"""
This is the custom action to generate memory questions if the user chooses a memory test. 
"""
class AskForCOLORAction(Action):
    def name(self) -> Text:
        return "action_ask_COLOR"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        answer_set = {'left':'red','right':'blue'}
        flag = random.randint(0, 1)
        if flag == 0:
            string_out = "$What is the color on the left?$ @What is the left color?@ &Left color?&"
            dispatcher.utter_message(text=string_out)
            return [SlotSet("color_answer", 'red')]
        else:
            string_out = "$What is the color on the right?$ @What is the right color?@ &Right color?&"
            dispatcher.utter_message(text=string_out)
            return [SlotSet("color_answer", 'blue')]


"""
This is a custom action that verifies that all required slots in the memory form are filled.
Validate the answer user has given.
Validate if user wants to quit.
"""
class ValidateMemoryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_memory_form"

    def validate_COLOR(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        answer = str(tracker.get_slot('color_answer'))
        color = str(slot_value)
        if color == answer:
            string_out = "$Correct! You win this game!$ @Correct!You win!@ &You win!&"
            dispatcher.utter_message(text=string_out)
        else:
            string_out = "$sorry you lost the game.$ @Sorry You lost!@ &You lost!&"
            dispatcher.utter_message(text=string_out)
        return {"COLOR": color}

    def validate_quit(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value:
            dispatcher.utter_message(text="$Great! Let us continue!$ @OK! let us go!@ &OK!&")
            return {"COLOR": None, "quit": None}
            # return {"quit": True}
        else:
            return {"quit": False}

"""
This is a custom action for force quitting.
If the user doesn't want to play anymore, clean all the slots and quit the form.
"""
class ActionCleanAll(Action):

    def name(self) -> Text:
        return "clean_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        string_out = "$Ok. Thanks for taking this test!$ @OK! Thanks for today! See you!@ &OK! See you!&"
        dispatcher.utter_message(text=string_out)

        return [SlotSet("math_answer", None), SlotSet("NUMBER", None), SlotSet("quit", None),SlotSet("color_answer", None), SlotSet("COLOR", None)]
