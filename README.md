<p align="center">
  <img src="https://image.genie.co.kr/imageg/web/common/logo_genie.png">
</p>  

## Overview
**GeniePy** is a tool for downloading streamable tracks from Genie.co.kr

Tested on **[Python 3.8.0](https://www.python.org/downloads/release/python-380/)**


## Installation & Setup

```
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
Username | Genie Username | `Slyyxp`
Password | Genie Password | `ReallyBadPassword123`

**directories:**

Config  | Description  | Example
------------- | ------------- | -------------
download_directory | Directory to download files to | `Z:/GeniePy/downloads`
log_directory | Directory to save log files to  | `Z:/GeniePy/logs`
default_format | Default download format (1: MP3, 2: 16-bit FLAC, 3: 24-bit FLAC) | `3`
artist_folders | Whether or not to nest downloads into artist folders | `True/False`

# To Do
- [ ] Refactor & Cleanup rip()
- [ ] Playlist support
- [ ] Artist support

## Disclaimer
- The usage of this script **may be** illegal in your country. It's your own responsibility to inform yourself of Copyright Law.