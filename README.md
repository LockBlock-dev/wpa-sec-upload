# wpa-sec upload

[![GitHub stars](https://img.shields.io/github/stars/LockBlock-dev/wpa-sec-upload.svg)](https://github.com/LockBlock-dev/wpa-sec-upload/stargazers)

Upload capture files to wpa-sec.

## Installation

-   Install [Python3](https://www.python.org/downloads/).
-   Get `hcxpcapngtool` from [hcxtools](https://github.com/ZerBea/hcxtools)
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

[Czechball for his upload script](https://github.com/Czechball/wpa-sec-api)

## Copyright

See the [license](/LICENSE)
