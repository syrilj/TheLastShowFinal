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
keys = {item['Name']: item['Value'] for item in response['Parameters']}

def get_key(key_path):
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


    key = "obituary.png"
    file_name = os.path.join("/tmp", key)
    with open (file_name, "wb") as f:
        f.write(binary_data[0])

    res = upload_to_cloudinary(file_name)



    cloudinary_url = res['url']
    #got to fix this function might not need could be done with create ob but well see 

    #probalby not done right this whole handler 
    return {
       "statusCode": 200,
       "body": json.dumps({
            "name": name,
            "birth": birth,
            "death": death,
            "cloudinary_url": cloudinary_url,
            #need to add gpt and pollu
       })
    }

def upload_to_cloudinary(filename, resource_type = "image", extra_fields=()):
   #modified from profs code done in lecture
   api_secret = get_key("/the-last-show/secret-key-cloudinary")
   api_key = get_key("/the-last-show/key-cloudinary")
   cloud_name = "dhshz69p3"

   body = {
       "api_key" : api_key
   }

   files = {
       "file": open(filename, "rb")
   }

   timestamp = int(time.time())
   body["timestamp"] = timestamp
   body.update(extra_fields)
   body["signature"] = create_signature(body, api_secret)

   url = f"http://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload".format(cloud_name)
   res = requests.post(url, files = files, data = body)
   return res.json()


def create_signature(body, api_secret):
   exclude = ["api_key", "resource_type", "cloud_name"]
   sorted_body = sort_dictionary(body)
   query_string = create_query_string(sorted_body)
   query_string_appended = f"{query_string}{api_secret}"
   hashed = hashlib.sha1(query_string_appended.encode())
   signature = hashed.hexdigest()
   return signature

def sort_dictionary(dictionary):
   exclude = ["api_key", "resource_type", "cloud_name"]
   return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[0]) if k not in exclude}
  
def create_query_string(body):
   query_string = ""
   for idx, (k,v) in enumerate(body.items()):
       query_string = f"{k}={v}" if idx == 0 else f"{query_string}&{k}={v}"
   return query_string

# def ask_gpt(name, bisth, death):
#    api_secret = get_key("/the-last-show/secret-key-gpt")
#    url = "https://api.openai.com/v1/completions"
#    headers = {
#        "Content-Type" : "applications/json",
#        "Authorization" : f"Bearer {api_secret}"
#    }


#    prompt = f"write an obituary about a fictional character named {name} who was born on {birth} and died on {death}"

#    body = {
#        "model": "text-davinci-003",
#        "prompt": prompt,
#        "max_tokens": 400,
#        "temperature": 0.5
#    }


#    res = requests.post(url, headers=headers, json=body)
#    return res.json()["choices"][0]["text"]

def read_this(text):
   client = boto3.client('polly')
   response = client.synthesize_speech(
   Engine ='standard',
   LanguageCode ='en-US',
   OutputFormat = 'mp3',
   Text = text,
   TextType = 'text',
   VoiceId = 'Joanna'
)

   filename = "polly.mp3"
   with open(filename, "wb") as f:
       f.write(response["AudioStream"].read())


   return filename

def get_cloudinary_url(filename):
    return upload_to_cloudinary(filename)['url']

def get_gpt_text(name, birth, death):
    return ask_gpt(name, birth, death)

def get_polly_url(text):
    filename = read_this(text)
    return upload_to_cloudinary(filename, resource_type='video')['url']

# Create obituary function
def create_obituary(uuid, fullname, born, died, image_filename, obituary):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('obituaries') # Update the table name to your DynamoDB table name
    
    # Upload image to Cloudinary
    image_url = upload_to_cloudinary(image_filename)
    
    # Generate obituary text with GPT-3
    prompt = f"Create obituary for {fullname}. Born on {born}, died on {died}. {obituary}"
    obituary_text = ask_gpt(prompt)
    
    # Generate audio file with Amazon Polly
    audio_filename = read_this(obituary_text)
    
    # Create item in DynamoDB
    item = {
        'uuid': uuid,
        'fullname': fullname,
        'born': born,
        'died': died,
        'image': image_url,
        'obituary': obituary_text
    }
    table.put_item(Item=item)
    
    # Return obituary text and audio file name
    return obituary_text, audio_filename

















# import os 
# import time
# import requests
# import hashlib
# from requests_toolbelt.multipart import decoder
# import boto3
# #cloudinary stuff 
# def upload_to_clodinary(filename,resource_type="image" ):
#         api_key = ""
#         cloudname = ""
#         #you get this from parameters 
#         api_secret = os.getenv("C_API_SECRET")
      
#         body ={
#                 "api_key":api_key,
#         }

#         files = {
#                 "file":open(filename,"rb")
#         }
#         timestamp = int(time.time())
#         body["timestamp"] = timestamp
#         body.update(timestamp)
#         body["signature"] = create_signature(body,api_secret)

#         url = "https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload".format(cloudname)
#         res = requests.post(url,files =files, data=body )
#         return res.json()

# def create_signature(body,api_secret):
#         exclude = ["api_key","resource_type","cloud_name"]
#         timestamp = int(time.time())
#         body[ "timestamp"] = timestamp
#         sorted_body = sort_dictionary(body,exclude)
#         qurey_string = create_query_string(body)
#         qurey_string_append = f"{qurey_string}{api_secret}"
#         hased = hashlib.sha1(qurey_string_append.encode())
#         singature = hashlib.hexadigest
#         return singature

# def sort_dictionary(dictionary):
#         return{k: v for k,v in sorted(dictionary.items(),key = lambda item: item[0]) if key not in exclude}

# def create_query_string(body):
#         qurey_string =""
#         for idx,(k,v) in enumerate(body.items()):
#                 qurey_string = f"{k} = {v}" if idx == 0 else f"{qurey_string}&{k}={v}"
#         return qurey_string


# def ask_gpt(prompt):
#         url = "https://api.openai.com/v1/completions"
#         headers = {
#                 #need tp read api key from parameters store 
#                 "Content-Type": "application/json",
#                 "Authorizaton": f"Bearer {os.getenv('CH_API_Key')}"
#         }
#         body = {
#                 "model": "text-davinvi-003",
#                 "prompt": prompt,
#                 "max_tokens": 400,
#                 "temperature": 0.2,
#         }
#         res = requests.post(url,headers=headers,json=body)
#         return res.json()["choices"][0]["secure_url"]

# #chat gpt use completions api for chatgpt one its chaeper and whats used in th edemo 
# #use this module pip install requests-toolbelt need to include in lambda fucntion 


# #amazon_polly do standard you can use any voice  there are 2 types of input text theres ssml and plain text ssml is just more verersatile to add like pauses and stuff to it 
# #got ot use aws-valut -exec command to run this 
# def read_this(text):
#         client  = boto3.client("polly")
#         res = client.synthesize_speech(
#                 Engine = 'standard',
#                 LanguageCode = 'en-US',
#                 Text=text,
#                 OutputFormat="mp3",
#                 textType = 'text',
#                 VoiceId="Joanna"
#         )
#         filename = "polly.mp3"
#         with open(filename,"wb") as f:
#                 f.write(res["AudioStream"].read())
#         return filename



#dynamodb Structure
#uuid - string
#fullname - string
#born - string
#died - string
#image - file
#obituary - string
