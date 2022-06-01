# wpa-sec upload

[![GitHub Stars](https://img.shields.io/github/stars/LockBlock-dev/wpa-sec-upload.svg)](https://github.com/LockBlock-dev/wpa-sec-upload/stargazers)
[![GitHub Watchers](https://img.shields.io/github/watchers/LockBlock-dev/wpa-sec-upload.svg)](#)
[![GitHub Forks](https://img.shields.io/github/forks/LockBlock-dev/wpa-sec-upload.svg)](https://github.com/Lockblock-dev/wpa-sec-upload/network/members)
[![GitHub Contributors](https://img.shields.io/github/contributors/LockBlock-dev/wpa-sec-upload.svg)](#)

Upload capture files to wpa-sec.

## Installation

-   Install [Python3](https://www.python.org/downloads/).
-   Get `hcxpcapngtool` from [hcxtools](https://github.com/ZerBea/hcxtools).
-   Download or clone the project.
-   Edit the [config.json](./config.json):

```json
{
    "api_url": "https://wpa-sec.stanev.org/",
    "api_key": "",
    "whitelist": []
}
```

Put your own WIFIs SSID in the whitelist like `["AndroidAP1234"]`.

-   Run `python3 upload.py`.

## Credits

-   [Czechball's upload script.](https://github.com/Czechball/wpa-sec-api)

## Copyright

See the [license](/LICENSE).
