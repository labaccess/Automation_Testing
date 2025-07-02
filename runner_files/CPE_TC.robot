*** Settings ***
#Resource    ../CPE_Data/Zyxel_PX3321-T1.robot
Resource    ${MODEL_RESOURCE}
Resource    ../Resources/RouterBngManager.robot
Resource    ../Resources/CabinVDSLManager.robot

*** Variables ***
${vendor_id}
${CPE_VENDOR_ID_PAGE_INFO}

*** Test Cases ***
#
#Login And BNG REBOOT
#    [Documentation]    Logs into the router and reboot BNG
#    Open CPE Page
#    Login To Router
#    Test BNG Connection
#    Logout from Router
#    [Teardown]
#
#BNG REBOOT
#    [Documentation]    reboot BNG
#    Test BNG Connection
#    [Teardown]
#
#VENDOR ID
#    [Documentation]   TC12 - Check vendor ID of ONT \
#    Cabin Side Get Vendor ID
#    Open CPE Page
#    Login To Router
#    CPE Get Vendor ID
#    Logout from Router
#    Cabin Compare Vendor ID
#    [Teardown]

Testing SSID Change
    [Documentation]   TC14 - change SSID on CPE and check the reflection
    Open CPE Page
    Login To Router
    Change SSID "WIFI_TEST"
    Logout from Router
    [Teardown]


*** Keywords ***
Cabin Compare Vendor ID
    log  Cabin type is: ${CABIN_TYPE}
    log  Vendor ID from CPE side is: ${vendor_id}
    log  Vendor ID from Cabin side is: ${CPE_VENDOR_ID_PAGE_INFO}
    Should Be Equal    ${vendor_id}    ${CPE_VENDOR_ID_PAGE_INFO}
