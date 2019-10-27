# pihole DNS pause
# atlasalex
import sys
import argparse
import re
import os
import paramiko

pattern = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
resolv_file = "/etc/resolv.conf"


def first_run():
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
    with os.popen(f'ssh -t {username}@{pihole_ip} "sudo cat /etc/pihole/setupVars.conf | grep PASSWORD"') as p_word_file:
        passwordd = p_word_file
        for entry in p_word_file:
            print(entry)
        # return(passwordd[0])


def get_pihole_status(pihole_ip):
    pass


if __name__ == "__main__":

    print("poop", get_pihole_ip())

    print("passssss", get_webpassword(get_pihole_ip(), "atlasalex"))
