# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests


class MainView(generic.View):
	def get(self, request, *args, **kwargs):
		if request.GET['hub.verify_token'] == '5602':
			return HttpResponse(request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')
	
	@csrf_exempt
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		

		print "Incoming"
		incoming_message = json.loads(request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print message
		
					prepare_reply(message['sender']['id'], message['message']['text'])
					#post_button(message['sender']['id'], message['message']['text'])
		return HttpResponse()

def prepare_reply(fbid, received_message):
	reponses = {
		'Hey': ['message', 'Hey yourself!'],
		'links': ['button', ['www.google.com','Back']]
		}
	print responses[received_message]
	

def post_message(fbid, received_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAALsttL5IYsBADNn88xVFKzm4QZBPg8u9NxZANNXEQLKA7gZBzA6F2ZCdTzVdRrD3tgtO6ORmLwRaD8UySZCN8xwVE7QuadxyiZC2Jx0Eg1UztvNNygMPb5n7kRO3jDQEMEnbcATdYvkpSIxNiZBNjQD7akwr0vSNQLZBdf6EaWcVQZDZD'
	response_msg = json.dumps(
		{"recipient":{"id":fbid},
		 "message":
		 	{"text":received_message}})

	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def post_button(fbid, received_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAALsttL5IYsBADNn88xVFKzm4QZBPg8u9NxZANNXEQLKA7gZBzA6F2ZCdTzVdRrD3tgtO6ORmLwRaD8UySZCN8xwVE7QuadxyiZC2Jx0Eg1UztvNNygMPb5n7kRO3jDQEMEnbcATdYvkpSIxNiZBNjQD7akwr0vSNQLZBdf6EaWcVQZDZD'
	response_msg = json.dumps(
		{"recipient":{"id":fbid},
		 "message":
		 	{"attachment":{
		 		"type":"template",
		 		"payload":{
		 			"template_type":"button",
		 			"text":received_message,
		 			"buttons":[
		 			{
		 				"type":"web_url",
		 				"url":"www.google.com",
		 				"title":"Google"

		 			},
					{
		 				"type":"web_url",
		 				"url":"www.facebook.com",
		 				"title":"Facebook"
		 			},
					{
		 				"type":"web_url",
		 				"url":"www.instagram.com",
		 				"title":"instagram"
		 			},
		 			]
		 		}
		 	}
		 	}})

	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()