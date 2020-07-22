<p align="center">
  <img src="https://image.genie.co.kr/imageg/web/common/logo_genie.png">
</p>  
<p align="center">
  <img src="https://img.shields.io/github/issues/Slyyxp/GeniePy?style=for-the-badge">  
  <img src="https://img.shields.io/github/languages/code-size/slyyxp/GeniePy?style=for-the-badge">  
  <img src="https://img.shields.io/maintenance/yes/2020?style=for-the-badge">  
</p>  

## Overview
**GeniePy** is a tool for downloading streamable tracks from **[Genie.co.kr](https://www.genie.co.kr/)**

Tested on **[Python 3.8.0](https://www.python.org/downloads/release/python-380/)**

## Prerequisites

- Python 3.6+
- Genie.co.kr subscription.  
  
## Installation & Setup

```bash
git clone https://github.com/Slyyxp/GeniePy.git
cd GeniePy
pip install -r requirements.txt
```

- Insert username and password into config.py.example  

- Rename config.py.example to config.py

## Command Usage
```
python genie.py -u {album_url} -f 3
```
Command  | Description  | Example
------------- | ------------- | -------------
-u | Genie album url (Required) | `https://www.genie.co.kr/detail/albumInfo?axnm=81510805`
-f | Format. 1: MP3, 2: 16-bit FLAC, 3: 24-bit FLAC (Optional) | `2`

## config.py

**credentials:**

Config  | Description  | Example
------------- | ------------- | -------------
username | Genie Username | `Slyyxp`
password | Genie Password | `ReallyBadPassword123`
device_id | Android Device ID | `eb9d53a3c424f961`
user_agent | User Agent | `genie/ANDROID/5.1.1/WIFI/SM-G930L/dreamqltecaneb9d53a3c424f961/500200714/40807`

**directories:**

Config  | Description  | Example
------------- | ------------- | -------------
download_directory | Directory to download files to | `Z:/GeniePy/downloads`
log_directory | Directory to save log files to  | `Z:/GeniePy/logs`
default_format | Default download format (1: MP3, 2: 16-bit FLAC, 3: 24-bit FLAC) | `3`
artist_folders | Whether or not to nest downloads into artist folders | `True/False`

# To Do
- [x] Figure out hardware identifiers  
- [ ] Refactor & Cleanup rip()
- [ ] Playlist support
- [ ] Artist support

## Disclaimer
- The usage of this script **may be** illegal in your country. It's your own responsibility to inform yourself of Copyright Law.