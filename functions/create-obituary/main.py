# add your create-obituary function here
#setup fucntion for cloudinary  
import os 
import time
import requests
import hashlib

import boto3
#cloudinary stuff 
def upload_to_clodinary(filename,resource_type="image" ):
        api_key = ""
        cloudname = ""
        #you get this from parameters 
        api_secret = os.getenv("C_API_SECRET")
      
        body ={
                "api_key":api_key,
        }

        files = {
                "file":open(filename,"rb")
        }
        timestamp = int(time.time())
        body["timestamp"] = timestamp
        body.update(timestamp)
        body["signature"] = create_signature(body,api_secret)

        url = "https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload".format(cloudname)
        res = requests.post(url,files =files, data=body )
        return res.json()

def create_signature(body,api_secret):
        exclude = ["api_key","resource_type","cloud_name"]
        timestamp = int(time.time())
        body[ "timestamp"] = timestamp
        sorted_body = sort_dictionary(body,exclude)
        qurey_string = create_query_string(body)
        qurey_string_append = f"{qurey_string}{api_secret}"
        hased = hashlib.sha1(qurey_string_append.encode())
        singature = hashlib.hexadigest
        return singature

def sort_dictionary(dictionary):
        return{k: v for k,v in sorted(dictionary.items(),key = lambda item: item[0]) if key not in exclude}

def create_query_string(body):
        qurey_string =""
        for idx,(k,v) in enumerate(body.items()):
                qurey_string = f"{k} = {v}" if idx == 0 else f"{qurey_string}&{k}={v}"
        return qurey_string


def ask_gpt(prompt):
        url = "https://api.openai.com/v1/completions"
        headers = {
                #need tp read api key from parameters store 
                "Content-Type": "application/json",
                "Authorizaton": f"Bearer {os.getenv('CH_API_Key')}"
        }
        body = {
                "model": "text-davinvi-003",
                "prompt": prompt,
                "max_tokens": 400,
                "temperature": 0.2,
        }
        res = requests.post(url,headers=headers,json=body)
        return res.json()["choices"][0]["secure_url"]

#chat gpt use completions api for chatgpt one its chaeper and whats used in th edemo 
#use this module pip install requests-toolbelt need to include in lambda fucntion 


#amazon_polly do standard you can use any voice  there are 2 types of input text theres ssml and plain text ssml is just more verersatile to add like pauses and stuff to it 
#got ot use aws-valut -exec command to run this 
def read_this(text):
        client  = boto3.client("polly")
        res = client.synthesize_speech(
                Engine = 'standard',
                LanguageCode = 'en-US',
                Text=text,
                OutputFormat="mp3",
                textType = 'text',
                VoiceId="Joanna"
        )
        filename = "polly.mp3"
        with open(filename,"wb") as f:
                f.write(res["AudioStream"].read())
        return filename



#dynamodb Structure
#uuid - string
#fullname - string
#born - string
#died - string
#image - file
#obituary - string
