'''
@File    :   media.py
@Time    :   2023/01/17 12:32:19
@Author  :   Juan Valero Oliet 
@Email   :   jvalero@accioncontraelhambre.org
@Desc    :   Este módulo permite subir, actualizar, y borrar media a través de la api.
'''

import json
import requests 
import pandas as pd
from copy import copy
from kobo.settings import TOKEN, SERVER_URL, USER
import os
import time
import kobo.api as api



def extract_media(column, i):
    if i<len(column):
        result=column[len(column)-1-i]
    else:
        result = ""
    return result




def upload_media(
    idform : str, 
    folder_path : str,
    file_name : str,
    rewrite : bool = False,
    token : str = TOKEN, 
    kc_server_url : str = SERVER_URL):
    '''
    This provides method to upload media via api. 
    Only csv or images are allowed.

    KeyArgs:
    idform -- form id
    file_path -- path to the file to be uploaded
    token -- autorithation token
    kc_server_url -- url to the server
    '''


    file_extension = os.path.splitext(file_name)[1]

    valid_media = [".jpeg",".jpg", ".png", ".csv"]
    img_extension=[".jpeg",".jpg", ".png"]
    

    if folder_path[-1] not in ["/", "\\"]:
        folder_path+="/"

    if file_extension not in valid_media:
        raise ValueError("upload_media: semestre must be one of %r." % valid_media)

    if file_extension in img_extension:
        mime = "image/{}".format(file_extension[1:])
    else:
        mime = "text/{}".format(file_extension[1:])
    print(mime)
    
    token_hd="Token {}".format(token)
    x="{}api/v1".format(kc_server_url)

    data = {
        'data_value': file_name,
        'xform': idform,
        'data_type': 'media',
        'data_file_type': mime,
    }
    headers={"Authorization" : token_hd}
    files = {'data_file': (file_name, open(fr'{folder_path}\{file_name}', 'rb').read(), mime)}

    response = requests.get("{}/metadata.json".format(x), headers=headers)

    dict_response = json.loads(response.text)

    # Delete appropriate entry in the metadata.json (delete old file)
    for each in dict_response:
        if each['xform'] == int(idform) and each['data_value'] == file_name:
            print(each)
            if rewrite == True:
                del_id = each['id']
                print("{}/metadata/{}".format(x, del_id))
                response.status_code = 403
                while response.status_code!=204:
                    response = requests.delete("{}/metadata/{}".format(x, del_id), headers=headers)
                    print(response.status_code)
                    time.sleep(1)
                break
            else:
                raise ValueError("There is already a file with the same name! Select new name or set rewrite = True")

    response = requests.post("{}/metadata.json".format(x), data=data, files=files, headers=headers)
    if response.status_code == 201:
        print("Successfully uploaded {} to {} form.".format(file_name, idform))
    else:
        print("Unsuccessful. Response code: {}".format(str(response.status_code)))

def upload_media_direct(
    idform : str, 
    file : str,
    file_name : str,
    file_name_new : str,
    rewrite : bool = False,
    token : str = TOKEN, 
    kc_server_url : str = SERVER_URL):
    '''
    This provides method to upload media via api, but media downloaded in situ. 
    Only csv or images are allowed.

    KeyArgs:
    idform -- form id
    file_path -- path to the file to be uploaded
    token -- autorithation token
    kc_server_url -- url to the server
    '''


    file_extension = os.path.splitext(file_name)[1]

    valid_media = [".jpeg",".jpg", ".png", ".csv", ".JPGE", ".JPG", ".PNG"]
    img_extension=[".jpeg",".jpg", ".png", ".JPGE", ".JPG", ".PNG"]
    

    
    if file_extension not in valid_media:
        raise ValueError("upload_media: semestre must be one of %r." % valid_media)

    if file_extension in img_extension:
        mime = "image/{}".format(file_extension[1:])
    else:
        mime = "text/{}".format(file_extension[1:])
    # print(mime)
    
    token_hd="Token {}".format(token)
    x="{}api/v1".format(kc_server_url)

    data = {
        'data_value': file_name,
        'xform': idform,
        'data_type': 'media',
        'data_file_type': mime,
    }
    headers={"Authorization" : token_hd}
    files = {'data_file': (file_name_new, file, mime)}

    response = requests.get("{}/metadata.json".format(x), headers=headers)

    dict_response = json.loads(response.text)

    # Delete appropriate entry in the metadata.json (delete old file)
    for each in dict_response:
        if each['xform'] == int(idform) and each['data_value'] == file_name_new:
            if rewrite == True:
                del_id = each['id']
                # print("{}/metadata/{}".format(x, del_id))
                response.status_code = 403
                while response.status_code!=204:
                    response = requests.delete("{}/metadata/{}".format(x, del_id), headers=headers)
                    print(response.status_code)
                    
                break
            else:
                raise ValueError("There is already a file with the same name! Select new name or set rewrite = True")

    nmax=0
    response.status_code!=500
    while response.status_code!=201 and nmax<20:
        response = requests.post("{}/metadata.json".format(x), data=data, files=files, headers=headers)
        if response.status_code == 201:
            break
        else:
            time.sleep(1)
            nmax+=1

    if response.status_code == 201:
            print("Successfully uploaded {} to {} form.".format(file_name, idform))
    else:
        print("Unsuccessful. Response code: {}".format(str(response.status_code)))


def acchatments_to_column(
    data : pd.DataFrame,
    media_columns : list):
    '''
    This function returns attached media in new columns, 
    one for each question with media, given df.
    
    '''

    i=0
    for column in media_columns:
        media=data["_attachments"].apply(lambda x: extract_media(x, i))
        media=pd.json_normalize(media)
        data["media_"+column]=media["download_url"]
        i+=1


    return data
    

def df_with_ttachments_column(
    idform : str,
    media_columns : list,
    token : str = TOKEN, 
    kc_server_url : str = SERVER_URL):
    '''
    This function returns attached media in new columns, 
    one for each question with media, given id form.
    
    '''

    data = api.json_to_df(
        idform,
        token,
        kc_server_url)

    i=0
    for column in media_columns:
        media=data["_attachments"].apply(lambda x: extract_media(x, i))
        media=pd.json_normalize(media)
        data["media_"+column]=media["download_url"]
        i+=1


    return data
    

def get_media_form(form_id, token=TOKEN, kc_server_url=SERVER_URL):
    '''
    This function gets all media from a form.

    '''

    token_hd="Token {}".format(token)
    x="{}api/v1".format(kc_server_url)
    headers={"Authorization" : token_hd}
    response = requests.get("{}/metadata.json".format(x), headers=headers)
    dict_response = json.loads(response.text)
    df=pd.DataFrame(dict_response)
    df=df.loc[df["xform"]==form_id]

    return df



def download_media(
    idform : str,
    id_media : str,
    token : str = TOKEN, 
    kc_server_url : str = SERVER_URL,
    user : str = USER):
    '''
    This function downloads data (image or csv) from a form media.
    
    '''

    form_id_string=api.get_id_string(idform)
    link="{}/{}/forms/{}/formid-media/{}".format(
        kc_server_url, 
        user, 
        form_id_string, 
        id_media)

    token_hd="Token {}".format(token)
    headers={"Authorization" : token_hd}
    media=requests.get(link, headers=headers).content

    return media

