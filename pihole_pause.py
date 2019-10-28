# pihole DNS pause
# atlasalex
import sys
import argparse
import os
import requests
import re
import getpass
from pexpect import pxssh

pattern = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"


def first_run(pihole_ip=None, username=None):
    with open("./pihole_pause.conf", "w") as conf:
        pihole_ip = get_pihole_ip()
        passwd = get_webpassword(pihole_ip, username)

        conf.writelines(f"pihole_ip,{pihole_ip}\n")
        conf.writelines(f"pihole_webpass,{passwd}\n")


def load_conf():
    # FIXME load conf from pihole_pause.conf
    pass


def get_pihole_ip():
    user_os = sys.platform
    if user_os == "darwin":
        with os.popen("scutil --dns") as dns:
            for entry in dns:
                if re.search(pattern, entry):
                    return re.search(pattern, entry)[0]

    elif user_os == "win32":
        pass

    elif sys.platform.startswith("linux"):
        if os.path.exists("/etc/resolv.conf"):
            with open("/etc/resolv.conf", "r") as filer:
                resolv = filer.read()

                return((re.search(pattern, resolv)[0]))


def get_webpassword(pihole_ip, username):
    # FIXME add argparse variables and input checking
    # FIXME add logging
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
        ssh_sess.sendline(
                "sudo cat /etc/pihole/setupVars.conf | grep PASSWORD"
                          )
        print("Retrieving Web Password")
        print("Please wait")
        ssh_sess.prompt()
        ssh_sess.sendline(ssh_pass)
        ssh_sess.prompt()
        grab = str(ssh_sess.before.decode("utf-8").strip())
        ssh_sess.logout()

    return grab[grab.find("=")+1:-1]


def get_pihole_status(pihole_ip):
    r = requests.get(f"http://{pihole_ip}/admin/api.php?status")
    if r.status_code == 200:
        return r.json()['status']


if __name__ == "__main__":

    if not os.path.exists("./pihole_pause.conf"):
        first_run()
    else:
        print("not first run.\nLoading configuration")
        load_conf()
