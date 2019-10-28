# paramiko test
from pexpect import pxssh
import getpass

grab = ""

hostname = input("hostname: ")
username = input("enter username for ssh: ")
ssh_pass = getpass.getpass("ssh password: ")

ssh_sess = pxssh.pxssh(options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})

if not ssh_sess.login(hostname, username, ssh_pass):
    print("ERRORRRRRR")  # FIXME add logging here
else:
    # ssh_sess.sendline('uptime')
    ssh_sess.sendline("sudo cat /etc/pihole/setupVars.conf | grep PASSWORD")
    print("Retrieving Web Password")
    print("Please wait")
    ssh_sess.prompt()
    ssh_sess.sendline(ssh_pass)
    ssh_sess.prompt()
    grab = str(ssh_sess.before.decode("utf-8").strip())
    ssh_sess.logout()

print("contents of grab: ", grab)
print()

print(grab[grab.find("=")+1:-1])  # This will be a return in the python module
