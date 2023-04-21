import os
import time
import requests
from requests_toolbelt.multipart import decoder
import hashlib
import boto3
import base64
import json

client = boto3.client('ssm')     
response = client.get_parameters_by_path(
    Path = '/the-last-show/',
    Recursive=True,
    WithDecryption=True
)

dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
table = dynamodb.Table('lastshow-30144227')

keys = {item['Name']: item['Value'] for item in response['Parameters']}

def get_parameters(key_path):
   return keys.get(key_path, None)

def lambda_handler(event, context):
    body = event["body"] 

    if event["isBase64Encoded"]:
        body = base64.b64decode(body)

    content_type = event["headers"]["content-type"]
    data = decoder.MultipartDecoder(body, content_type)

    binary_data = [part.content for part in data.parts]
    name = binary_data[1].decode()
    birth = binary_data[2].decode()
    death = binary_data[3].decode()

    uuid = event["headers"]["uuid"]

    key = "obituary.png"
    filename = os.path.join("/tmp", key)
    with open (filename, "wb") as f:
        f.write(binary_data[0])

    result = cloudinary_upload(filename, resource_type="image")


    cloudinary_url = result['url']
    text_chatgpt = gpt_prompt(name, birth, death)
    text_from_polly = polly_talk(text_chatgpt)
    mp3 = cloudinary_upload(text_from_polly, resource_type="raw")

    try:
        table.put_item(
        Item={
            'name': name,
            'birth': birth,
            'death': death,
            'uuid': uuid,
            "cloudinary_url": cloudinary_url,
            "description": text_chatgpt,
            "polly_url": mp3["secure_url"]
        }
   ) 
        return {
        "statusCode": 200,
        "body": json.dumps({
                "name": name,
                "birth": birth,
                "death": death,
                "cloudinary_url": cloudinary_url,
                "description": text_chatgpt,
                "polly_url": mp3["secure_url"]
        })
        }
    except Exception as e:
        return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Error adding item to database"
        })
        }
def cloudinary_upload(filename, resource_type = "", extra_fields=()):
   api_secret = get_parameters("/the-last-show/secret-key-cloudinary")
   api_key = get_parameters("/the-last-show/key-cloudinary")
   cloud_name = "dhavjvbib"
   body = {
       "api_key" : api_key
   }

   files = {
       "file": open(filename, "rb")
   }

   timestamp = int(time.time())
   body["timestamp"] = timestamp
   body.update(extra_fields)
   body["signature"] = signature_creation(body, api_secret)

   url = f"http://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload".format(cloud_name)
   result = requests.post(url, files = files, data = body)
   return result.json()


def signature_creation(body, api_secret):
   exclude = ["api_key", "resource_type", "cloud_name"]
   sorted_body = give_sorted_dictionary(body)
   query_string = query_string_creation(sorted_body)
   query_string_appended = f"{query_string}{api_secret}"
   hashed = hashlib.sha1(query_string_appended.encode())
   signature = hashed.hexdigest()
   return signature
  
def give_sorted_dictionary(dictionary):
   exclude = ["api_key", "resource_type", "cloud_name"]
   return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[0]) if k not in exclude}

  
def query_string_creation(body):
   query_string = ""
   for idx, (k,v) in enumerate(body.items()):
       query_string = f"{k}={v}" if idx == 0 else f"{query_string}&{k}={v}"
   return query_string

def gpt_prompt(name, birth, death):
   api_secret = get_parameters("/the-last-show/api-key")
   url = "https://api.openai.com/v1/completions"
   headers = {
       "Content-Type" : "application/json",
       "Authorization" : f"Bearer {api_secret}"
   }
   prompt = f"write an obituary about {name}, a fictional character born on {birth} and died on {death}, who leaves a heroic legacy of unwavering determination, selflessness, and inspiration"


   body = {
       "model": "text-curie-001",
       "prompt": prompt,
       "max_tokens": 600,
       "temperature": 0.4
   }


   result = requests.post(url, headers=headers, json=body)
   return result.json()["choices"][0]["text"]


def polly_talk(prompt):
   client = boto3.client('polly')
   response = client.synthesize_speech(
   Engine ='standard',
   LanguageCode ='en-US',
   OutputFormat = 'mp3',
   Text = prompt,
   TextType = 'text',
   VoiceId = 'Joanna'
)

   filename = "/tmp/polly.mp3"
   with open(filename, "wb") as f:
       f.write(response["AudioStream"].read())

   return filename
