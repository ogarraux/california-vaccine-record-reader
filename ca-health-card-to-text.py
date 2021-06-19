#!/usr/bin/env python

import argparse
import base64
import json
import zlib

from pyzbar.pyzbar import decode
from PIL import Image

def qrcode_to_shc_text(image_path):
    result = decode(Image.open(image_path))
    return result[0].data.decode("utf-8") 

def shc_text_to_jws(shc_string):
    # in theory there could be multiple chunks, but mine didn't have that
    shc_string = shc_string.replace('shc:/', '')
    
    decoded_shc_string = ""

    for i in range(0, len(shc_string), 2):
        # https://github.com/smart-on-fhir/health-cards/blob/main/docs/index.md
        # take each group of 2 digits from QR code.  Subtract 45 and convert them to a character
        decoded_shc_string += chr(int(shc_string[i:i+2]) + 45)
    
    return decoded_shc_string

def jws_to_json(jws_string):
    # the pyjwt library seems like it should be able to decode this
    # but it failed for me.  maybe related to the compression? idk

    # contains header, data, and signature separated by '.'
    jws_list = jws_string.split(".")
    decoded_data = base64.urlsafe_b64decode(jws_list[1] + "=")
    
    # wbits -15 tells zlib that this is a "raw" deflate compression (which has no headers)
    decompressed_data = zlib.decompress(decoded_data, wbits=-15)
    return decompressed_data

def pretty_json(data):
    return json.dumps(json.loads(data.decode("utf-8")), indent=4, sort_keys=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    args = ap.parse_args()

    print(pretty_json(jws_to_json(shc_text_to_jws(qrcode_to_shc_text(args.file)))))