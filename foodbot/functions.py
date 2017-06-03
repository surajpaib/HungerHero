import json
import requests
from models import UserInfo
ACCESS_TOKEN = 'EAABZBdLhMSq4BAPd6MDLtdPpsjOP5wTpxab8C9SxZAQ1RZCzQoZC8CyU4234ZBnTQCrMAqXug725dnvDsQ4DKysWbTq4JjA7LiMAzVXPn9lG3azK0l7InBeVRCyr7kqX3ZBzcSCBaKfiqMyptzertGym4j7efofc7ZAXMYmHZA5XugZDZD'
def get_recipient_id(body):
    for entry in body['entry']:
        for message in entry['messaging']:
            return message['sender']['id']

def get_started(recipient_id,body,send_message):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "postback" in message:
                if message["postback"]["payload"]=="start":

                    s = UserInfo()
                    s.name = recipient_id
                    s.lat = 0
                    s.long = 0
                    s.counter = 0
                    s.save()
                    post_message(recipient_id, 'Please enter your location via attachment button')



def get_location(recipient_id, body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                if "attachments" in message["message"]:
                    for attachment in message["message"]["attachments"]:
                        if attachment["type"] == 'location':
                            lat = attachment["payload"]["coordinates"]["lat"]
                            long = attachment["payload"]["coordinates"]["long"]

                            ## Send location to the Message Center Backend
                            # if
                            # message = 'Sorry, we cannot service your area at the moment. We sincerely apologize'
                            return lat, long


def generic_template(recipient_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
  "recipient":{
    "id":recipient_id
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"Thanks for volunteering to donate!",
        "buttons":[
          {
            "type":"postback",
            "title":"Donate",
            "payload":"donate"
          }
        ]
      }
    }
  }
})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())


def check_template(recipient_id, body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                if "attachments" in message["message"]:
                    for attachment in message["message"]["attachments"]:
                        if attachment["type"] == 'template':
                            if "payload" in attachment:
                                if "buttons" in attachment["payload"]:
                                    for button in attachment["payload"]["buttons"]:
                                        if button["payload"] == "donate":
                                            val = True
                                            post_message(recipient_id, "Enter the number of people you think your food will serve")
                                            return  val

def check_quick_replies(recipient_id, body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                if "attachments" in message["message"]:
                    for attachment in message["message"]["attachments"]:
                        if attachment["type"] == 'template':
                            if "payload" in attachment:
                                if "elements" in attachment["payload"]:
                                    for element in attachment["payload"]["elements"]:

                                        if "buttons" in element:
                                            for button in element["buttons"]:
                                                if button["payload"] == "yes":
                                                    state = 6
                                                if button["payload"] == "no":
                                                    state = 3

                                                return state


def demo_display(recipient_id,body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                if "text" in message["message"]:
                    try:
                        number = int(message["message"]["text"])
                        state = 5
                    except:
                        number = 0
                        state = 4

                    return number, state

def quick_replies(recipient_id, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":message,
            "buttons":[
              {
                  "type": "postback",
                  "title": "Yes",
                  "payload": "yes"
              },{
                "type":"postback",
                "title":"No",
                "payload":"no"
              }
            ]
          }
        ]
      }
    }
  }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

def post_message(recipient_id,message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

