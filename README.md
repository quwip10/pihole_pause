Readme.md for pihole_pause.py
Program utilizes pihole API to make it easy to pause pihole as needed

Roadmap:
Create initial program with hardcoded values for my servers

Break out first_run() into its own module and import.

    This will reduce the imports needed every time since this is only needed once. 
Add argparse to pass values

Upadate get_webpasswd to use paramiko

Update get_pihole_ip to get secondary dns

    Also accept manual ip addresses via argparse


Very Future State:

Possibly make into browser extension
