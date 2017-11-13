import boto3
import os

def lambda_handler(event, context):
    ec2client = boto3.client('ec2')
    snsclient = boto3.client("sns")
    
    for instance in event['resources']:
        print(instance)
        
        ec2instance = ec2client.describe_instances(InstanceIds=[instance.partition('/')[2]])
        print ec2instance
        
        for res in ec2instance['Reservations']:
            for inst in res['Instances']:
                public_ip = inst['PublicIpAddress']
                print( public_ip)
                    
                snsclient.publish(Message = public_ip, TopicArn=os.environ.get("TOPIC_ARN"))
                
                
    return 'Hello from Lambda'