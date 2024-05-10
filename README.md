# pykobo_legacy
## Introduction
This is an old repository to fetch data from KoboToolBox that uses the api v1. Is shared for reference and to use by entities that have an old KoboToolBox version installed on their systems.

### Note
This repository is not maintained anymore. Please use the new version of pykobo [https://github.com/pvernier/pykobo](https://github.com/pvernier/pykobo) or my fork with new features [https://github.com/jvalero/pykobo](https://github.com/jvalero/pykobo).
This was one of my first projects in Python, so please don't expect it to be perfect.

## 1. Installation

## 2. Configuration File
The configuration settings are stored in a JSON file named config.json, located within the pykobo_legacy/config subfolder. If the file does not exist, it will be created with default settings when you first use the package.

The configuration settings you need to set are:
- token: Authentication token for the KoBoToolbox server.
- server_url: URL for the KoBoToolbox server.

You can access and modify the configuration settings using the provided functions:

### Set configuration settings
You must do this at least once before using the package.

```python
import pykobo_legacy.config as config

# Set a new token
config.set_token("new_token")

# Set a new server URL
config.set_server_url("https://example.com")

# Set a new user
config.set_user("new_user")
```

### Get configuration settings
The package access the configuration settings using the following functions, that you can use to get the current values of the settings:

```python
import pykobo_legacy.config as config

# Get the current token
token = config.get_token()

# Get the current server URL
server_url = config.get_server_url()

# Get the current user
server_url = config.get_user()

