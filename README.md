## Overview
California recently announced a digital Covid vaccine record.  I obtained mine, which was presented as a QR code on a web page.  I was curious what specifically was encoded in the QR code, so I set about trying to read it.

The QR code uses the SMART Health Card (https://smarthealth.cards/) format, which ends up using a signed JSON web token.

## Requirements
* 'zbar' (a non-Python tool) is required by the pyzbar library for decoding the QR codes.  On MacOS with Homebrew you can install it with 'brew install zbar'
* Only tested on Python 3.7 on MacOS

## Usage
0. Obtain your vaccine record from the California Department of Public Health: https://myvaccinerecord.cdph.ca.gov/.  Save the QR code image.
1. Setup Python environment:  virtualenv venv; source venv/bin/activate; pip install -r requirements.txt
2. Run script: ./ca-health-card-to-text.py <path to the saved QR code image>

Note: The Smart Health Card QR codes contain data and a signature to verify the data is correct.  This script just displays the data - it does not attempt to validate it.  So, if you wanted to actually validate a health card, this would be insufficient.

## So what *is* stored in the QR code after all? 
Slightly more information than the vaccine record page shows in text, but nothing super exciting:

- Name
- Birthdate
- Covid vaccine dates, lot numbers, and who gave you the vaccine (just CVS Pharmacy for mine, not the specific location or person).
- Interestingly, for me the actual name of the vaccine was not in the QR code - just a numeric vaccine code.  This CDC page shows what vaccine each of the codes refer to: https://www.cdc.gov/vaccines/programs/iis/COVID-19-related-codes.html
