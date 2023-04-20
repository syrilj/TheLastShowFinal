import time
import hashlib
import requests
import os
import pytest
import boto3
import importlib.util
spec = importlib.util.spec_from_file_location("create-obituary", "functions/create-obituary/main.py")
create_obituary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_obituary)

def test_polly_talk():
    # Test case 1: Provide valid text input
    text = "Hello, thIS IS BILLY BOB JUNIOR REPORTING FOR DUTY"
    result = create_obituary.polly_talk(text) 
    create_obituary.cloudinary_upload(result)
    assert result is not None


def test_upload_to_cloudinary():
    # Test case 1: Provide required arguments only
    filename = "functions/112648-yeager-eren-free-transparent-image-hd.jpeg"
    result = create_obituary.cloudinary_upload(filename)
    assert result is not None


    # Test case 2: Provide additional optional arguments
    extra_fields = {"tags": ["tag1", "tag2"], "context": "test"}
    result = create_obituary.cloudinary_upload(filename, resource_type="image", extra_fields=extra_fields)
    assert result is not None

