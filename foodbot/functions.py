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
        "text":"Thanks for taking the step to donate food to the needy !! Your pretty great!",
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
            if "postback" in message:
                if "payload" in message["postback"]:

                    if message["postback"]["payload"] == "donate":
                        val = True
                        return  val

def check_quick_replies(recipient_id, body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "postback" in message:
                if "payload" in message["postback"]:

                    if message["postback"]["payload"] == "yes":
                        state = 6
                    else:
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

def get_location_status(lat, long):
    get_message_url = 'https://script.google.com/macros/s/AKfycbwro50BxXC-8_Z_bEYJdFCfeQU8euwClIqaoOZs3mbCc-4wLtU/exec?lat={0}&lng={1}'.format(str(lat), str(long))
    # status = requests.get(get_message_url, headers={"Content-Type": "application/json"}).content
    status = True
    return status

def order_placed(lat, long, recipient_id, counter):
    post_message_url = \
        'https://script.google.com/macros/s/AKfycbwmjwSHMW8905HlvwlsaftLauWeVbPZlrQkrQZnjhC94VV6xcxR/exec?lat={0}&long={1}&customer_id={2}&order_id={3}'\
            .format(lat, long, recipient_id, counter)
    status = requests.post(post_message_url)
    return status


def template(recipient_id,name):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id":recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Congratulations on your donation!! Food donated to CoWoks Meal Center!",
                            "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Wok_cooking.jpg",
                            "subtitle": "Your food has reached {0}, We look forward to having you help us again.".format(name)


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

