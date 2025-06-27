*** Settings ***
Library    ./CabinVDSLManager.py

*** Keywords ***
Cabin Side Get Vendor ID
    ${vendor_id}=    Cabin Get Vendor ID    ${CABIN_TYPE}    ${DUT_LOCATION}
    Set Suite Variable    ${vendor_id}
    Log    Vendor ID is: ${vendor_id}

