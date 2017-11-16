# AWS EC2 IP reputation check
Lambda function triggers to check public IP reputation of any new ec2 instances

Full write-up soon!

## Concept

* Monitor your AWS account for new EC2 instances
* Grab any associated Public IP address
* Send the IP to an SNS topic
* A Lambda function receives the IP and checks a public reputation service
* SMS is sent to a user if the IP has previously been associated with something dubious

![architecture](https://github.com/raoul361/AWS-ec2IPreputation/blob/master/Web%20App%20Reference%20Architecture.png)

Note I've included various files needed to show the roles, policies and configuration of the stack.

## Getting EC2 Instance Data

This is fairly simple; grab the IP from an Instance number (via the full ARN in the CloudWatch message)

```
for res in ec2instance['Reservations']:
    for inst in res['Instances']:
        public_ip = inst['PublicIpAddress']
```

## ThreatCrowd

I use this simply as an example; plus it's free! ThreatCrowd provides a [-1,0,1] scoring for domains based on crowd sourced voting.

```
result =  requests.get("https://www.threatcrowd.org/searchApi/v2/ip/report/?ip=" + message)
report = json.loads(result.text)
vote = report['votes']
```

## Why not AWS Config

This gives a more nuanced view and can be adapted to use services that provide more detailed scoring. ASC Config seems to be a pass/fail; in this case, we just want people to be aware of what is going on.

The idea is not to shut anything down, but provide info for an informed decision.


## Further Adaptions

* Could easily add more Lambda functions to handle ELB, NAT and other IP address sources.
* Subscriptions for whitelisting services in SIEM
* General notification service
