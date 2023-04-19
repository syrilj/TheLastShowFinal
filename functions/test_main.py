import time
import hashlib
import requests
import os
import pytest
import boto3
import importlib.util
spec = importlib.util.spec_from_file_location("create-obituary", "/Users/syriljacob/Documents/the-last-show-hamza-and-syril/functions/create-obituary/main.py")
create_obituary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_obituary)

def test_read_this():
    # Test case 1: Provide valid text input
    text = "Hello, thIS IS BILLY BOB JUNIOR REPORTING FOR DUTY"
    filename = create_obituary.read_this(text)
    assert os.path.exists(filename)
    assert filename.endswith(".mp3")


def test_upload_to_cloudinary():
    # Test case 1: Provide required arguments only
    filename = "functions/112648-yeager-eren-free-transparent-image-hd.jpeg"
    result = create_obituary.upload_to_cloudinary(filename)
    assert result is not None


    # Test case 2: Provide additional optional arguments
    extra_fields = {"tags": ["tag1", "tag2"], "context": "test"}
    result = create_obituary.upload_to_cloudinary(filename, resource_type="image", extra_fields=extra_fields)
    assert result is not None

    # Test case 3: Provide invalid filename
#     filename = "nonexistent_file.jpeg"
#     with pytest.raises(Exception) as e:
#         result = create_obituary.upload_to_cloudinary(filename)
#     assert str(e.value) == "File not found"


# def test_sort_dict():
#         timestamp = int(time.time)
#         api_key = "1234"
#         eager = " w_400,h_300,c_pad|w_260,h_200,c_crop"
#         public_id = "sample_image"
#         body = {
#                 "api_key":api_key,
#                 "timestamp":timestamp,
#                 "eager": eager,
#                 "public_id": public_id,
#         }
#         res = sort_dictionary(body,["api _key"])

#         assert res.items() =={
#                 "public_id": public_id,
#                 "eager": eager,
#                 "timestamp":timestamp
#         }.items()
#         api_secret = ""
#         qurey_string = create_query_string(res)
#         assert qurey_string == "eager=w400,h_300"

#         signature = create_signature(body,api_secret)
#         assert signature == "1234"
# #use secure url for dynamo db table 

#     with mock_ssm():
#         # Create a boto3 SSM client
#         client = boto3.client('ssm')
        
#         # Add a parameter to the SSM parameter store
#         client.put_parameter(
#             Name='/the-last-show/secret-key-cloudinary',
#             Value='my-secret-key',
#             Type='SecureString',
#             KeyId='alias/aws/ssm',
#         )
        
#         # Call the get_key() function to retrieve the parameter
#         key_path = '/the-last-show/secret-key-cloudinary'
#         result = get_key(key_path)
        
#         # Assert that the result matches the expected value
#         assert result == 'my-secret-key'

# def test_gpt():
#         prompt = "This is a test"
#         res = ask_gpt(prompt)
#         assert len(res)> 0 
# def test_polly():
#        text = "words to say"
#        res = read_this(text)

#        assert os.path.exists(res) 
#        #do this becaue it needs to be publically avalibe to use 
#        res = upload_to_cloudinary(res,resourse_type ="raw")  
#        print(res["secure_url"])
#        assert res(["secure_url"])>0
