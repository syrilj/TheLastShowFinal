import time
import hashlib
import requests
import os
import pytest
from functools import create_signature,create_query_string,sort_dictionary,upload_to_cloudinary,ask_gpt
import boto3
def test_sort_dict():
        timestamp = int(time.time)
        api_key = "1234"
        eager = " w_400,h_300,c_pad|w_260,h_200,c_crop"
        public_id = "sample_image"
        body = {
                "api_key":api_key,
                "timestamp":timestamp,
                "eager": eager,
                "public_id": public_id,
        }
        res = sort_dictionary(body,["api _key"])

        assert res.items() =={
                "public_id": public_id,
                "eager": eager,
                "timestamp":timestamp
        }.items()
qurey_string = create_qurey_string(res)
assert qurey_string = "eager=w400,h_300"

signature = create_signature(body,api_secret)
assert signature == "1234"
#use secure url for dynamo db table 


def test_uplaod():
    filename = "alan.png"
    res = upload_to_cloudinary(filename)
    print[res["eager"][0]["secure_url"]]
    assert res is not None

def test_gpt():
        prompt = "This is a test"
        res = ask_gpt(prompt)
        assert len(res)> 0 
def test_polly():
       text = "words to say"
       res = read_this(text)

       assert os.path.exists(res) 
       #do this becaue it needs to be publically avalibe to use 
       res = upload_to_cloudinary(res,resourse_type ="raw")  
       print(res["secure_url"])
       assert res(["secure_url"])>0
