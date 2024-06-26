<p align="center">
  <picture>
    <img alt="pykobo" src="https://jvaleroliet.github.io/images/pykobo.png" style="max-width: 100%;">
  </picture>
</p>

## Introduction
This is an old repository to fetch data from KoboToolBox that uses the api v1. Is shared for reference and to use by entities that have an old KoboToolBox version installed on their systems.
It offers the possibility to make a backup of the data stored in the KoBoToolBox server (see [Backup](#backup) section).


### Note
This repository is not maintained anymore. Please use the new version of pykobo [https://github.com/pvernier/pykobo](https://github.com/pvernier/pykobo) or my fork with new features [https://github.com/jvalero/pykobo](https://github.com/jvalero/pykobo).
This was one of my first projects in Python, so please don't expect it to be perfect.

## 1. Installation
To install, run the following command in your terminal:

`pip install git+https://github.com/jvaleroliet/pykobo_legacy.git@main`


## 2. Configuration File
The configuration settings are stored in a JSON file named config.json, located within the pykobo_legacy/config subfolder. If the file does not exist, it will be created with default settings when you first use the package.

The configuration settings you need to set are:
- token: Authentication token for the KoBoToolbox server.
- server_url: URL for the KoBoToolbox server.

You can access and modify the configuration settings using the provided functions:

### Set configuration settings
You must do this at least once before using the package.

```python
import pykobo_legacy.config.config_handler as config

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
```
    
## 3. Basic Usage
Once the configuration settings are set, you can use the package to interact with the KoBoToolbox server.

### Forms info
To get all the forms and the information about them, you can use the following function, which returns a pandas DataFrame:

```python
import pykobo_legacy as kb

# Fetch all the forms information
forms_info = kb.api.forms_info()

# Print the forms information
print(forms_info)
```

### Form Class
Once you have selected the form you want to fetch data from, you can get its id from the forms_info dataframe and use the Form class to interact with it. 


```python

# Fetch data from a form
form_id = "form_id"
data = kb.Form(form_id)

```

The Form class has the following atributes:

- survey: The survey sheet from the xlsform.
- choices: The choices sheet from the xlsform.
- settings: The settings sheet from the xlsform.
- data: The submission data from the form.
- media: The media files from the form.

The Form class has the following methods:

- get_data_labels: To get the labels of the data columns or the data values in a specific language.


### The media module
The media module allows you to interact with the media from the form, either from the submissions or from the form. Let's see a couple of examples:

#### Upload media
To upload an image or a csv file to a form, you can use the following function:

```python
import pykobo_legacy as kb

# Upload an image to a form
form_id = "form_id"
image_path = "path/to/image.jpg"
image_name = "new_name.jpg"
kb.media.upload_media(form_id, image_path, image_name, rewrite=False)

# Upload a csv file to a form
form_id = "form_id"
csv_path = "path/to/csv.csv"
csv_name = "new_name.csv"
kb.media.upload_media(form_id, csv_path, csv_name, rewrite=True)

```

As you can see, when uploading the image we don't want to rewrite a file that is on the server with the same name. However, when uploading the csv file we want to rewrite the file that is on the server with the same name. That's why we choose the rewrite parameter.


#### Download media
To download the media from the form, you can use the following function:

```python
import pykobo_legacy as kb

# Download an image from a form
form_id = "form_id"
media_id = "media_id"
kb.media.download_media(form_id, media_id)
```

### Backup
The package offers a function to backup all the projects from the user account. It will save the data and the xls in two separate files, in one folder for each form, as well as the form info in a file called form_info.

```python
import pykobo_legacy as kb

# Backup all the projects from the user account
kb.api.backup("output/folder/path/for/backup")

```




