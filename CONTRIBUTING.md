# Contributing Guidelines
Thank you for your interest in Project XenXenXenSe. This document will help you kick start how to contribute into XenXenXenSe Project.

While contributions are always welcome, But please if your change you wish to make is breaking changes in any form, please first discuss the change you wish to make via issue.  
Please note this project follows [Stella IT Opensource Project Code of Conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.  

## Contributors' Guidelines
Please following the rules below in order to be accepted at PR.

### Commit Conventions
We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit message.  
This is for enhancing readability and for future automatic parsing 

### Black Formatter
We use Black Formatter to format the code. The properly formatted code is necessary before your code being merged.  
This can be triggered via `./scripts/format.sh` and `./scripts/format-imports.sh`

### Target Python Version
Currently, XenXenXenSe targets Python 3.9, and supports Python 3.7 or up.  
Supported interpreters are:  
 * Official Python Interpreter
 * PyPy

## I want to add a feature!
Please note that we use [XenGarden](https://github.com/Stella-IT/XenGarden) as our XenAPI gateway. If you want to implement a feature, Please check the feature you want to implement is implemented on [XenGarden](https://github.com/Stella-IT/XenGarden) first. If not, Please implement in [XenGarden](https://github.com/Stella-IT/XenGarden), *(Your PRs are welcomed at XenGarden too!)* before implementing it on XenXenXenSe.
