import requests, os
from os import listdir, mkdir, path
from subprocess import run, DEVNULL
from json import load

if not path.isdir("./hashes"):
    try:
        os.rename("./hashes", "./hashes.old")
        print('Renamed your hashes file to "hashes.old"!')
    except:
        pass
    try:
        mkdir("./hashes")
    except:
        print(
            'Failed to make hashes directory! Make a directory called "hashes" and restart the program.'
        )
        exit()

if not path.isdir("./handshakes"):
    print(
        'Failed to find handshakes! Create a directory called "handshakes", place your handshakes inside and restart the program.'
    )
    exit()

with open("config.json", "r") as f:
    config = load(f)
    f.close()

new_config = {"whitelist": []}

for whitelisted_ssid in config["whitelist"]:
    new_config.append(whitelisted_ssid.lower())

config = new_config
new_config = None

handshakes = listdir("./handshakes/")
hashes = listdir("./hashes/")
size = len(handshakes)
flag = False
msg = ""
uploaded = 0

i = 0

for handshake in handshakes:
    ssid = handshake.lower().split("_")[0]
    if ssid in config["whitelist"]:
        msg = "\033[93mHandshake is in the whitelist!\033[0m"
    elif handshake.endswith(".pcap"):
        run(
            [
                "hcxpcapngtool",
                f"./handshakes/{handshake}",
                "-o",
                f"./hashes/{ssid}.hc22000",
            ],
            capture_output=False,
            stderr=DEVNULL,
            stdout=DEVNULL,
        )

        if path.exists(f"./hashes/{ssid}.hc22000"):
            f = open(f"./hashes/{ssid}.hc22000", "r")
            hash = f.read()
            f.close()

            old = open("./old.txt", "r")
            old_hashes = old.read().split("\n")
            old.close()

            c = False
            """ old funny code
            for e in hash.split("\n"):
                if len(e) > 0 and e in old_hashes:
                    c += 1
            """
            for currenthash in hash.split("\n"):
                if (len(currenthash) != 0) and (currenthash in old_hashes):
                    c = True

            if c == False:
                old = open("./old.txt", "a")
                old.write(hash)
                old.close()

                handshake = open(f"./handshakes/{handshake}", "rb")
                payload = {"file": handshake}
                headers = {"user-agent": "LockBlock-Dev/wpa-sec-upload (1.0.0)"}
                cookies = {"key": config["api_key"]}
                r = requests.post(
                    f'{config["api_url"]}?submit',
                    headers=headers,
                    cookies=cookies,
                    files=payload,
                )
                handshake.close()

                if r.text == "Not a valid capture file. We support pcap and pcapng.":
                    msg = "\033[91mInvalid capture file!\033[0m"
                elif r.text == "No valid handshakes/PMKIDs found in submitted file.":
                    msg = "\033[91mNo valid handshakes/PMKIDs found!\033[0m"
                else:
                    print(r.text)
                    msg = "\033[92mHandshake uploaded!\033[0m"
                    uploaded += 1
            else:
                msg = "\033[93mHandshake already uploaded!\033[0m"
        else:
            msg = "\033[91mInvalid capture file!\033[0m"
    else:
        msg = "\033[91mNot a handshake file!\033[0m"

    flag = False
    i = i + 1
    print(f"Handshake {i}/{size}: {handshake} => {msg}")
print(f"\nUploaded {uploaded} handshakes of {size} handshakes!")

run(["rm", "-r", "./hashes"])
