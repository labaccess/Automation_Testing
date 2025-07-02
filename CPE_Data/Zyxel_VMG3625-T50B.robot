*** Settings ***
Library           SeleniumLibrary    run_on_failure=Nothing
Library           OperatingSystem

*** Variables ***
${ROUTER_URL}         https://192.168.1.1
${USERNAME}           admin
${PASSWORD}           Love@younis95
${USER_NAME_LOGIN_ID_VISIBLE}   username
${PASSWORD_LOGIN_ID_VISIBLE}    userpassword
${BTN_LOGIN_ID_VISIBLE}    loginBtn
${CABIN_TYPE}      Huawei
${DUT_LOCATION}  0 5 0 16
${SSID_FIELD}        id=wifi_ssid_000_11general11_000
${SSID_SAVE_BUTTON}  id=applyWifiBtn
${VENDOR}

*** Keywords ***
Open CPE Page
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --ignore-certificate-errors
    Call Method    ${options}    add_argument    --allow-insecure-localhost
    Open Browser    ${ROUTER_URL}    chrome    options=${options}
    Maximize Browser Window

Login To Router
    Wait Until Element Is Visible    id=${USER_NAME_LOGIN_ID_VISIBLE}    10s
    Input Text    id=${USER_NAME_LOGIN_ID_VISIBLE}    ${USERNAME}
    Input Text    id=${PASSWORD_LOGIN_ID_VISIBLE}    ${PASSWORD}
    Click Button    id=${BTN_LOGIN_ID_VISIBLE}

    Sleep    5s    # Optional: wait for UI update
    Capture Page Screenshot    welcome_page.png

CPE Get Vendor ID
    Sleep    1s
    Click Element    xpath=//div[@id='card_sys']/div
    Sleep    1s
    Click Element    xpath=//div[@id='card_sysinfo']/span
    Sleep    1s
    Capture Page Screenshot    device_Vendor_ID.png
    ${CPE_VENDOR_ID_PAGE_INFO} =    Get Text    xpath=//li[normalize-space(.)='Manufacturer']/following-sibling::li[1]
    Set Suite Variable    ${CPE_VENDOR_ID_PAGE_INFO}
    Log    Manufacturer is: ${CPE_VENDOR_ID_PAGE_INFO}

Logout from router
    Sleep    3s    # Optional: wait for UI update
    # Step 1: Click the DSL menu item
    Click Element   id=h_menu_list

    Sleep    3s    # Optional: wait for UI update
    # Step 1: Click the logout bottum
    Click Element    id=navbar_logout

    # Step 2: Wait for the iframe to load the correct src
    Wait Until Page Contains    Are you sure you want to logout?    timeout=10s

    Sleep    3s    # Optional: wait for UI update
    # Step 3: click OK
    Click Element    xpath=//button[.//span[normalize-space(text())='Ok']]

    Close Browser

Change SSID
    [Arguments]    ${NEW_SSID}
    Navigate To Sub Menu    network    Wireless
    Wait Until Element Is Visible    ${SSID_FIELD}    timeout=10s
    Clear Element Text    ${SSID_FIELD}
    Input Text    ${SSID_FIELD}    ${NEW_SSID}
    Click Button    ${SSID_SAVE_BUTTON}
    Sleep    2s
    Capture Page Screenshot    ${SCREENSHOT_DIR}/ssid_change.png


Open Sidebar
    Wait Until Element Is Visible    ${SIDEBAR_BUTTON}    timeout=5s
    Click Element    ${SIDEBAR_BUTTON}
    Sleep    1s

Navigate To Main Menu
    [Arguments]    ${menu_id}
    Open Sidebar
    Click Element    xpath=//a[@href="#${menu_id}"]
    Sleep    2s

Navigate To Sub Menu
    [Arguments]    ${main_menu_id}    ${sub_href}
    Navigate To Main Menu    ${main_menu_id}
    Click Element    xpath=//a[contains(@href, "${sub_href}")]
    Sleep    2s
