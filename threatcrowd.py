from __future__ import print_function

import json
import requests
import boto3
import os
import socket

def lambda_function(event, context):
    client = boto3.client("sns")
    message = event['Records'][0]['Sns']['Message']
    
    try:
		socket.inet_aton(message)
    except socket.error:
		print("Received invalid address")
		return message
		
    result =  requests.get("https://www.threatcrowd.org/searchApi/v2/ip/report/?ip=" + message)

    report = json.loads(result.text)
    try:
        vote = report['votes']
    
        if( vote < 0 ):
            outcome = "Reputation for: " + message + " is malicious"
            client.publish(Message = outcome, TopicArn=os.environ.get("TOPIC_ARN"))
        else:
            outcome = "Reputation for: " + message + " is probably harmless"
            client.publish(Message = outcome, TopicArn=os.environ.get("TOPIC_ARN"))
    except:
        print("No information")
        outcome = "Reputation for: " + message + " is unknown"
        client.publish(Message = outcome, TopicArn=os.environ.get("TOPIC_ARN"))
        
    return message