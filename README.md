![XenXenXenSe Project banner](demonstration/banner.png)

# Project XenXenXenSe
A Modern RESTful API implemenation of XenAPI for Citrix Hypervisor® and XCP-ng.  
Try not to confuse with [ZenZenZenSe (前前前世)](https://en.wikipedia.org/wiki/Zenzenzense). 

## What is this?
Contrary to XenAPI which requires specific instruction of that calls command, get reference, request. Instead, it uses advantages of Object Oriented Asynchrounous Python and RESTful API to create "translation layer" for XenAPI.

## Where does Stella IT use this?
This is a "Core Component" of Stella IT's VM Management and control system.

## Guide
### How to Install
1. Clone this repository
2. Copy config.py.example to config.py
3. Enter your credentials
4. run `pipenv install`
5. activate virtualenv by `pipenv shell`
6. run server by `python3 main.py`

### API Docs
Working in progress.  
Please refer to automatic documentation page of FastAPI (available at /docs) for this time.  

## Developer
### Commit Conventions
We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit message.

## License
Distributed under GNU AGPLv3 *(GNU Affero General Public License Version 3)*.  
If you need commercial license, feel free to contact us at [contact@stella-it.com](mailto:contact@stella-it.com)  

### License FAQ
See [LICENSE_FAQ.md](LICENSE_FAQ.md).  

## Copyright
Copyright (c) Stella IT Co, Ltd.
