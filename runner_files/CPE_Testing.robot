*** Settings ***
Library           SeleniumLibrary    run_on_failure=Nothing
Library           OperatingSystem
Library           Resources/excel_keywords.py


*** Variables ***
${ROUTER_URL}         https://192.168.1.1
${USERNAME}           admin
${PASSWORD}           00000044
${EXCEL_PATH}         ${OUTPUT DIR}/serial_info.xlsx
${CSV_PATH}           ${OUTPUT DIR}/serial_info.csv
${IFRAME_XPATH}       //*[@id="divTabledeviceInfoForm"]


*** Test Cases ***
Login And Save Device Info
    [Documentation]    Logs into the router, extracts all info table fields, and saves to Excel
    Setup Browser
    Login To Router
    # Navigate To Device Info
    # Extract Table To Excel
    Logout from Router
    [Teardown]    Close Browser

*** Keywords ***
Setup Browser
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --ignore-certificate-errors
    Call Method    ${options}    add_argument    --allow-insecure-localhost
    Open Browser    ${ROUTER_URL}    chrome    options=${options}
    Maximize Browser Window
    
Login To Router
    Wait Until Element Is Visible    id=username    10s
    Input Text    id=username    ${USERNAME}
    Input Text    id=userpassword    ${PASSWORD}
    Click Button    id=loginBtn

    Sleep    5s    # Optional: wait for UI update
    Capture Page Screenshot    Login To Router page verification.png

    #Execute JavaScript    arguments[0].scrollIntoView(true);    xpath=//h3[text()='WiFi Settings']
    Scroll Element Into View    xpath=//h3[normalize-space(text())='WiFi Settings']
    Capture Page Screenshot    Login To Router page wifi setting.png


    ${total_height}=    Execute JavaScript    return document.body.scrollHeight
    ${viewport_height}=    Execute JavaScript    return window.innerHeight
    ${scrolls}=    Evaluate    int(${total_height} / ${viewport_height})

    FOR    ${i}    IN RANGE    ${scrolls}
        Execute JavaScript    window.scrollBy(0, ${viewport_height})
        Sleep    1s
        Capture Page Screenshot    part_${i}.png
    END
    #Log    <img src="Login To Router page verification.png">    html=true

    # Wait Until Page Contains Element    id=name_Systeminfo    10s
    # Click Element    id=name_Systeminfo

Navigate To Device Info

    Wait Until Page Contains Element    id=name_deviceinfo    10s
    Click Element    id=name_deviceinfo

    # Step 1: Click the DSL menu item
    Click Element    id=deviceinfo

    # Step 2: Wait for the iframe to load the correct src
    Wait Until Keyword Succeeds    10x    1s    Frame Should Contain    id=menuIframe    Device

    # Step 3: Switch to the iframe
    Select Frame    id=menuIframe
    Sleep    1s    # Optional: wait for UI update
    Capture Page Screenshot    device_info.png
    

Extract Table To Excel

    # Step 4: Now extract the DSL info
    Wait Until Page Contains Element    xpath=//table
    ${rows}=    Get WebElements    xpath=//table//tr
    ${data}=    Create List

    FOR    ${row}    IN    @{rows}
        ${Data_text}=    Get Text    ${row}
        ${cells}=    Data Reformating Device Info    ${Data_text}
    END

    Write Full Table To Csv    ${CSV_PATH}   

    # Step 5: Switch back to main page if needed
    Unselect Frame

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
    Click Element    xpath=//button[.//span[normalize-space(text())='OK']]