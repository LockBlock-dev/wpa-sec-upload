import requests
from os import listdir, mkdir, path
from subprocess import run, DEVNULL
from json import load

try:
    mkdir("./hashes")
except:
    pass

with open("config.json", "r") as f:
    config = load(f)
    f.close()

for i in range(len(config["whitelist"])):
    config["whitelist"][i] = config["whitelist"][i].lower()

handshakes = listdir("./handshakes/")
hashes = listdir("./hashes/")
size = len(handshakes)
flag = False
msg = ""
uploaded = 0

for i in range(size):
    ssid = handshakes[i].lower().split("_")[0]
    if ssid in config["whitelist"]:
        msg = "Handshake is in the whitelist"
    elif handshakes[i].endswith(".pcap"):
        run(
            [
                "hcxpcapngtool",
                f"./handshakes/{handshakes[i]}",
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

            c = 0

            for e in hash.split("\n"):
                if len(e) > 0 and e in old_hashes:
                    c += 1

            if c == 0:
                old = open("./old.txt", "a")
                old.write(hash)
                old.close()

                handshake = open(f"./handshakes/{handshakes[i]}", "rb")
                payload = {"file": handshake}
                headers = {"user-agent": "test"}
                cookies = {"key": config["api_key"]}
                r = requests.post(
                    f'{config["api_url"]}?submit',
                    headers=headers,
                    cookies=cookies,
                    files=payload,
                )
                handshake.close()

                if r.text == "Not a valid capture file. We support pcap and pcapng.":
                    msg = "Not a valid capture file"
                elif r.text == "No valid handshakes/PMKIDs found in submitted file.":
                    msg = "No valid handshakes/PMKIDs found"
                else:
                    print(r.text)
                    msg = "Handshake uploaded"
                    uploaded += 1
            else:
                msg = "Handshake already uploaded"
        else:
            msg = "Not a valid capture file"
    else:
        msg = "Not a handshake file"

    flag = False

    print(f"Handshake {i+1}/{size}: {handshakes[i]} => {msg}")
print(f"\nUploaded {uploaded} handshakes on {size} handshakes")

run(["rm", "-r", "./hashes"])
