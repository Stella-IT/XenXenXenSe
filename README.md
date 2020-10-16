![XenXenXenSe Project banner](demonstration/banner.png)

# Project XenXenXenSe
A Modern RESTful API implemenation of XenAPI for Citrix Hypervisor® and XCP-ng.  
Try not to confuse with [ZenZenZenSe (前前前世)](https://en.wikipedia.org/wiki/Zenzenzense). 

## Notice
**BREAKING CHANGES:**  
Since, [*"master"* term in technological industries](https://en.wikipedia.org/wiki/Master/slave_(technology)) triggers and offends some , maintainer (@MisakaMikoto0502) has been decided this breaking changes to this repository.  
Since this change can affect all of the forked repositories, Please make sure you have your default branch is using name *"main"* if else, please change it to *"main"*. Thank you.  
  
**SLOW UPDATE NOTICE:**  
XenXenXenSe is currently in rewrite session to create a modular structure and in process of seperating between [XenGarden which is a Python wrapper for XenAPI](https://github.com/Stella-IT/XenGarden).  
Due to this, XenXenXenSe Project is currently on going maintenance work, therefore, having a slow update speed.  
Thank you for your understanding.  
  
## Build Status
![Unit Test](https://github.com/Stella-IT/XenXenXenSe/workflows/Unit%20Test/badge.svg)
![Build Debian Package](https://github.com/Stella-IT/XenXenXenSe/workflows/Build%20Debian%20Package/badge.svg)
![Python Script Linting](https://github.com/Stella-IT/XenXenXenSe/workflows/Python%20Script%20Linting/badge.svg)

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
5. run server via `pipenv run start`

### API Docs
Working in progress.  
Please refer to automatic documentation page of FastAPI (available at /docs) for this time.  

## Contributors' Guidelines
### Commit Conventions
We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit message.

### Black Formatter
We use [Black Formatter](https://github.com/psf/black) to format the code

### pre commit hooks
We are using pre-commit for checking linters and commit conventions before the commits.  
Please install it via `pipenv run pre-commit-setup` after you clone it.

## License
Distributed under MIT License.
If you need commercial license, feel free to contact us at [contact@stella-it.com](mailto:contact@stella-it.com)  

### License FAQ
See [LICENSE_FAQ.md](LICENSE_FAQ.md).  

## Copyright
Copyright (c) Stella IT Co, Ltd.
