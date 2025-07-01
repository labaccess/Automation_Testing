*** Settings ***
Library    SeleniumLibrary
Library    DateTime
Library    OperatingSystem

*** Keywords ***
Open Router With Security Bypass
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${options}    add_argument    --ignore-certificate-errors
    Create WebDriver    Chrome    options=${options}
    Go To    ${ROUTER_URL}

Login To Router
    Maximize Browser Window
    Wait Until Element Is Visible    id=username    timeout=10s
    Input Text    id=username        ${USERNAME}
    Input Text    id=userpassword    ${PASSWORD}
    Click Button  id=loginBtn
    Run Keyword And Continue On Failure    Wait Until Element Is Visible    id=card_sys    timeout=15s
    Sleep    3s
    Capture Page Screenshot    ${SCREENSHOT_DIR}/login.png

Logout From Router
    Wait Until Element Is Visible    id=h_menu_list    timeout=5s
    Click Element    id=h_menu_list
    Wait Until Element Is Visible    id=navbar_logout    timeout=5s
    Click Element    id=navbar_logout
    #Wait Until Page Contains Element    xpath=//button[span[text()='OK']]    timeout=10s #ONT ZYXEL
    #Sleep    1s
    #Click Element    xpath=//button[span[text()='OK']]  #ONT ZYXEL

    Wait Until Page Contains Element    xpath=//button[span[text()='Ok']]    timeout=10s
    Sleep    1s
    Click Element    xpath=//button[span[text()='Ok']]
    Wait Until Element Is Visible    id=username    timeout=15s



    Wait Until Element Is Visible    id=username    timeout=15s
    ${timestamp}=    Get Time    result_format=%Y%m%d_%H%M%S
    Sleep    1s
    Capture Page Screenshot     ${SCREENSHOT_DIR}/logout.png

