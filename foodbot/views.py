# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
# Create your views here.
from models import UserInfo
from functions import get_recipient_id, get_started, get_location, post_message, generic_template, demo_display, check_template, quick_replies, check_quick_replies

def verify_token(request):
    if (request.GET['hub.verify_token'] == 'hunger'):
        return HttpResponse(request.GET['hub.challenge'],status=200)
    else:
        return HttpResponse("Wrong verification token",status=200)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        body=json.loads(request.body.decode('utf-8'))
        recipient_id = get_recipient_id(body)
        print recipient_id
        for entry in body['entry']:
            for message in entry['messaging']:
                if "postback" in message:
                    if message["postback"]["payload"] == "start":
                        if not(UserInfo.objects.filter(name= recipient_id).exists()):
                            post_message(recipient_id,'Welcome to HungerHero, you can donate your excess food to people who need it. Dont throw out food in haste. We make sure theres no waste. Cheers!   ')

                            s = UserInfo()
                            s.name = recipient_id
                            s.lat = 0
                            s.long = 0
                            s.counter = 0
                            s.state = 0
                            s.served = 0
                            s.save()
                            post_message(recipient_id, 'Please enter your location via attachment button')
                            return HttpResponse(status=200)
                        if UserInfo.objects.filter(name = recipient_id).exists():
                            post_message(recipient_id, 'Welcome back to HungerHero!')
                            s = UserInfo.objects.get(name=recipient_id)
                            s.state = 1
                            s.save()

        k = UserInfo.objects.get(name=recipient_id)

        if k.state == 0:
            try:
                lat, long = get_location(recipient_id, body)
                k.lat = lat
                k.served = 0
                k.long = long
                k.state = 1
                k.save()

            except:
                post_message(recipient_id,'Please use the + sign and the location option to give us your location for the pickup')

        if k.state == 1:
            # location detect webhook
            generic_template(recipient_id)
            k.state = 2
            k.save()


        if k.state == 2:

            if check_template(recipient_id, body):
                k.state = 3
                k.save()
            else:
                k.state = 1
                k.save()

        if k.state == 3:
            post_message(recipient_id, 'Please tell us how many people do you think your excess food would serve. Dont fret, just give us an estimate. ')
            k.state = 4
            k.save()

        if k.state == 4:
            try:
                number, state = demo_display(recipient_id, body)
                k.state = state
                k.served = number + k.served
                k.save()
                if state == 5:
                    quick_replies(recipient_id, 'Let me confirm, thats food for '+str(number)+ ' people?')
                if state == 4:
                    post_message(recipient_id, 'We didnt catch that, please re-enter your number')

            except:
                k.state = 3
                k.save()

        if k.state == 5:
            state = check_quick_replies(recipient_id, body)
            k.state = state
            k.save()

        if k.state == 6:
            post_message(recipient_id, 'Thank you for your contibution, our delivery executive will be here to pick your food up in about 30 minutes')
            # Ping backend with order created and people served
            k.save()

        if k.state == 7:
            # Contribution received POST req
            post_message(recipient_id, 'Your contribution has reached ')



        return HttpResponse(status=200)

    if request.method == 'GET':
        return verify_token(request)

#
# def food_center_webhook(request):
#     if request.method == 'POST':

