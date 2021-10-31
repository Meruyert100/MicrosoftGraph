import requests
import json
import logging
import azure.functions as func
from azure.storage.blob import ContainerClient

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):

  user = requests.get(
    '{0}/me'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token)
    },
    params={
      '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
    })

  return user.json()

def get_images():
  container_sas_url = "https://mersecuredphotos.blob.core.windows.net/securedphotos?sp=rl&st=2021-10-31T08:51:10Z&se=2021-10-31T16:51:10Z&spr=https&sv=2020-08-04&sr=c&sig=8n4T8Ex70MSF1dht4y8w0l20vppAFUkPpJJMK9yJOtQ%3D"
  container = ContainerClient.from_container_url(container_sas_url)
  blob_list = container.list_blobs()
  images = []
  for blob in blob_list:
    blob = container.get_blob_client(blob)
    images.append(blob.url)
  return images