import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC0a69daf1e8412c4d4bb91712beaf89ae'
auth_token = 'e939a41b20a3618db83484a543728d78'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='There is one apple in fridge',
         from_='+14436489378',
         to='+918523861880'
     )

print("message sent")