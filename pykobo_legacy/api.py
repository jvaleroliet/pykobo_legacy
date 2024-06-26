import json 
import requests 
import pandas as pd
from io import StringIO
import inquirer
from copy import copy
import uuid
from itertools import combinations
from . import media
from .config import config_handler as config
from datetime import datetime
import os

# Get the current token
token = config.get_token()

# Get the current server URL
server_url = config.get_server_url()
# Get the current token
token = config.get_token()


#retrieve forms info
def forms_info(token=token, kc_server_url=server_url):
    '''Downloads all (active) forms available in the user account.'''
    token_hd="Token "+token
    x=kc_server_url+"api/v1/data"
    url = requests.get(x, headers={"Authorization" : token_hd})
    text = url.text
    data = json.loads(text)
    df=pd.json_normalize(data)
    return df


def json_to_csv(form_id, token=token, kc_server_url=server_url, values=False):
    '''Download a specific form and transform it in csv'''
    token_hd="Token "+token
    if values==True:
        x=kc_server_url+"api/v1/data/"+form_id+".csv?lang=Spanish (es)"
    else:
        x=kc_server_url+"api/v1/data/"+form_id+".csv"
    url = requests.get(x, headers={"Authorization" : token_hd})
    text = url.text
    data = pd.read_csv(StringIO(text))
    return data


def json_to_df(form_id, token=token, kc_server_url=server_url):
    token_hd="Token "+token
    x=kc_server_url+"api/v1/data/"+form_id
    url=requests.get(x, headers={"Authorization" : token_hd})
    text = url.text
    data = json.loads(text)
    df=pd.json_normalize(data)
    return df


def get_xls(form_id, token=token, kc_server_url=server_url, sheet=1):
    token_hd="Token "+token
    x=kc_server_url+"api/v1/forms/"+form_id+"/form.xls"
    url=requests.get(x, headers={"Authorization" : token_hd})
    if sheet==1:
        df = pd.read_excel(url.content, engine="xlrd")
    elif sheet==2:
        df = pd.read_excel(url.content, sheet_name="choices", engine="xlrd")
    else:
        df = pd.read_excel(url.content, sheet_name="settings", engine="xlrd")
    return df


def download_xls(form_id, download_path, token=token, kc_server_url=server_url ):
    token_hd="Token "+token
    x=kc_server_url+"api/v1/forms/"+form_id+"/form.xls"
    url=requests.get(x, headers={"Authorization" : token_hd})
    with open(download_path, 'wb') as f:
        f.write(url.content)
        f.close()

    

def change_validation_status( id, idform, new_validation, token=token, kc_server_url=server_url):
    token_hd="Token "+token
    x=kc_server_url+"api/v1/data/"+idform+"/"+id+"/validation_status"
    body={"validation_status.uid":new_validation}
    url=requests.patch(x, json=body, headers={"Authorization" : token_hd})
    print("Response code: "+str(url.status_code))

def update_data(uid, kpiform, data, token=token, kc_server_url=server_url):
    '''
    Must provide data in dict form. Ex: {"test_1":"a"}
    '''
    if not uid[0:6]=="_uuid:":
        uid="_uuid:"+uid
    token_hd="Token "+token
    x=kc_server_url+"api/v1/submissions"
    new_uid=str(uuid.uuid4())
    new_instance="uuid:"+new_uid
    meta={"instanceID":new_instance, "deprecatedID":uid}
    submission=data
    submission.update({"meta":meta})
    data={"id":kpiform, "submission":submission}
    url=requests.post(x, headers={"Authorization" : token_hd}, json=data)
    print("Response code: "+str(url.status_code))
    
    

def upload_data(kpiform, data, token=token, kc_server_url=server_url):
    '''
    Must provide data in dict form. Ex: {"test_1":"a"}
    '''
    token_hd="Token "+token
    x=kc_server_url+"api/v1/submissions"
    new_uid=str(uuid.uuid4())
    new_instance="uuid:"+new_uid
    meta={"instanceID":new_instance}
    submission=data
    submission.update({"meta":meta})
    data={"id":kpiform, "submission":submission}
    url=requests.post(x, headers={"Authorization" : token_hd}, json=data)
    print("Response code: "+str(url.status_code))
    

def search_select(search, token=token, kc_server_url=server_url, id=False):
    forms=forms_info(token, kc_server_url)
    forms_match=forms.loc[forms["title"].str.lower().str.contains(search.lower())]
    if forms_match.empty:
        print("Your search has no results. Try again.")
    else:
        questions = [
            inquirer.List('search',
                message="Select one form from the list: ",
                choices=forms_match["title"].to_list(),
                )
            ]
        answers = inquirer.prompt(questions)
        nombre=answers["search"]
        x=forms.loc[forms["title"]==nombre]["url"].values[0]
        token_hd="Token "+token
        
        if id==False:
            url=requests.get(x, headers={"Authorization" : token_hd})
            text = url.text
            data = json.loads(text)
            df=pd.json_normalize(data)
            return df
        else:
            return x




def get_id_string(id):
    ''' 
    Get id string from number id for a form.
    
    '''

    metadata=forms_info()
    metadata=metadata.loc[metadata["id"]==id]
    id_string=metadata["id_string"].tolist()[0]
    return id_string



def drop_groupnames(df):
    columns=copy(df.columns)
    final_columns=[]
    for count, ele in enumerate(columns):
        i=ele.split("/")[-1]
        final_columns.append(i)
    df.columns=final_columns
    return df

def list_combinations(sample_list):
    '''Dada una lista de items, nos crea una lista de tuplas con las combinaciones de esos items
    
    Argumentos:
    sample_list -- objeto tipo list
    '''
    list_combinations=[]
    for n in range(len(sample_list) + 1):
        list_combinations += list(combinations(sample_list, n))
    return list_combinations


def comb_to_str(touple, choices=False):
    '''Dada una tupla, nos crea un string con los elementos de la tupla separados por espacios " " o ";"
    
    Argumentos:
    touple -- tupla que queremos pasar a string
    choices -- True si queremos que la separación sea ";", False si queremos que la separación sea " " (espacio en blanco)
    '''
    if len(touple)==0:
        string=""
    else:
        string=touple[0]
        
        if len(touple)>1:
            for i in touple[1:]:
                if choices==False:
                    string+=" "+i
                else:
                    string+="; "+i

    return string


def list_comb_str(list_comb, choices=False):    
    '''Dada una lista de tuplas, nos genera una lista de strings cada uno con los elementos de la tupla separados por espacios " " o ";"

    Argumentos:
    list_comb -- lista de tuplas, con las combinaciones
    choices -- True si queremos que la separación sea ";", False si queremos que la separación sea " " (espacio en blanco)
    '''
    combinations_strings=[]
    for touple in list_comb:
        combinations_strings+=[comb_to_str(touple, choices)]
    return combinations_strings


def process_choices(sample_list, choices=False):
    '''Dada una lista de items, nos procesa todos los pasos anteriores

    Argumentos:
    sample_list -- lista de items
    choices -- valor para pasar a las otras funciones
    '''
    return list_comb_str(list_combinations(sample_list), choices)

def backup(folder_path):
    folder = os.path.join(folder_path, datetime.today().strftime("%Y%m%d"))
    if not os.path.exists(folder):
        os.mkdir(folder)
    forms = forms_info()
    forms.to_csv(os.path.join(folder, "forms_info.csv"))
    
    for form in forms.iterrows():
        id = str(form[1]["id"])
        form_folder = os.path.join(folder, f"{id}")
        if not os.path.exists(form_folder):
            os.mkdir(form_folder)
        data = json_to_df(id)
        data.to_csv(os.path.join(form_folder, "data.csv"))
        download_xls(id, f"{form_folder}/form.xls")



def create_dfs(form, language = None):
    """Esta función nos crea las dos hojas auxiliares para la validación de datos.

    Argumentos:
    form -- kobo.Form

    Output:
    aux -- pd.DataFrame
    choices_so_2 -- pd.DataFrame
    survey -- pd.DataFrame
    """
    #Separamos los atributos del formulario
    choices=form.choices
    survey=form.survey

    #Definimos la columna label:
    if language==None:
                label='label'
    else:
        label = 'label::'+language
        
    #Separamos los nombres de la lista y los tipos de pregunta
    survey[["type_nochoice","list_name"]]=survey["type"].str.split(" ",expand=True)

    #Procesamos los datos de selección única
    #Separamos los choices de selección única
    choices_so=copy(choices.loc[choices["list_name"].isin(survey.loc[survey["type_nochoice"]=="select_one"]["list_name"])])
    choices_so=copy(choices_so[["list_name", "name", label]])
    #Creamos la tabla auxiliar donde meteremos las coordenadas
    aux=pd.DataFrame(columns=["list_name", "coord_min", "coord_max"])
    #Esto nos sirve para inicializar las coordenadas
    coord_max=0
    #Como la tabla original de choices se va a desordenar, tenemos que crear también una que va a ser copia de esta donde meteremos los datos en el nuevo orden
    choices_so_2=pd.DataFrame(columns=["list_name", "name", label])
    #Hacemos el loop sobre cada una de las listas
    for lista in set(choices_so["list_name"]):
        #Nos quedamos con el sub dataframe asociado a esa lista
        df_lista=choices_so.loc[choices_so["list_name"]==lista]
        #Definimos las nuevsa coordenadas máxima y mínima
        len_lista=len(df_lista)
        coord_min=copy(coord_max+1)
        coord_max+=len_lista
        #Hacemos los appends a las dos hojas
        choices_so_2=pd.concat([choices_so_2, df_lista], ignore_index=True)
        df_aux_lista=pd.DataFrame({"list_name":[lista], "coord_min":[coord_min], "coord_max":[coord_max]})
        aux=pd.concat([aux, df_aux_lista], ignore_index=True)

    #Porcesamos ahora los datos de las listas de selección multiple. El único cambio es que tenemos que utilizar las funciones definidas al principio del script para crear las combinaciones
    choices_sm=copy(choices.loc[choices["list_name"].isin(survey.loc[survey["type_nochoice"]=="select_multiple"]["list_name"])])
    choices_sm=copy(choices_sm[["list_name", "name", label]])
    for lista in set(choices_sm["list_name"]):
        df_or_lista=copy(choices_sm.loc[choices_sm["list_name"]==lista])
        d={"name":process_choices(df_or_lista["name"].tolist()), label:process_choices(df_or_lista[label].tolist(), True)}
        df_lista=pd.DataFrame(data=d)
        df_lista["list_name"]=copy(lista)
        len_lista=len(df_lista)
        coord_min=copy(coord_max+1)
        coord_max+=len_lista
        choices_so_2=pd.concat([choices_so_2, df_lista], ignore_index=True)
        df_aux_lista=pd.DataFrame({"list_name":[lista], "coord_min":[coord_min], "coord_max":[coord_max]})
        aux=pd.concat([aux, df_aux_lista], ignore_index=True)

    return aux, choices_so_2, survey




class Form:
    def __init__(self, id, token=token, kc_server_url=server_url):
        self.id = id
        self.token=token
        self.kc_server_url=kc_server_url
        self.survey=get_xls(self.id, self.token, self.kc_server_url)
        self.choices=get_xls(self.id, self.token, self.kc_server_url, sheet=2)
        self.settings=get_xls(self.id, self.token, self.kc_server_url, sheet=3)
        self.data=json_to_df(self.id, self.token, self.kc_server_url)
        self.media=media.get_media_form(self.id, self.token, self.kc_server_url)

    def get_data_labels(self, choices=False, survey=False, language=None):
        
        if language==None:
                label='label'
        else:
            label = 'label::'+language


        if choices==True:
            

            survey_copy=copy(self.survey)
            survey_copy[["type_nochoice","list_name"]]=survey_copy["type"].str.split(" ",expand=True)
            survey_subset=copy(survey_copy[["name", "type_nochoice", "list_name"]])
            survey_subset=survey_subset.loc[survey_subset["type_nochoice"].isin(["select_one", "select_multiple"])]
            choices_copy=copy(self.choices)
            if not survey_subset.loc[survey_subset["type_nochoice"].isin(["select_multiple"])].empty:
                aux, choices_b, survey_b = create_dfs(self, language)
                choices_copy=copy(choices_b)

            

            keys=pd.merge(survey_subset[["list_name", "name"]], choices_copy, on="list_name", how="left", suffixes=("_survey", "_choices"))
            data_copy=copy(self.data)
            data_copy=drop_groupnames(data_copy)
            for col in list(set(survey_subset["name"])):
                try:
                    col_copy=copy(data_copy[col])
                    keys_subset=copy(keys.loc[keys["name_survey"]==col])
                    keys_subset=keys_subset[["name_survey", "name_choices", label]]
                    col_copy=pd.merge(col_copy, keys_subset, left_on=col, right_on="name_choices", how="left")
                    data_copy[col]=col_copy[label]

                except:
                    continue
            column_names=copy(self.data.columns.tolist())
            self.data=data_copy
            self.data.columns=column_names
            
        
        if survey==True:
            #Esto no funciona bien, hay que hacer algo con las columnas con labels repetidas
            column_names=pd.DataFrame(columns=["Colnames"], data=self.data.columns)
            column_names["Nogroup"]=column_names["Colnames"].apply(lambda x: x.split("/")[-1])
            column_names=pd.merge(column_names, self.survey[["name", label]], left_on="Nogroup", right_on="name", how="left")
            column_names["Final"]=column_names[["Colnames", label]].apply(lambda x: x[1] if pd.notna(x[1]) else x[0], axis=1)
            self.data.columns=column_names["Final"].tolist()
        
