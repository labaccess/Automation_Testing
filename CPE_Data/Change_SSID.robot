*** Settings ***
Library    SeleniumLibrary
Resource   ../resources/sidebar_keywords.robot

*** Variables ***
${SSID_FIELD}        id=wifi_ssid_000_11general11_000
${SSID_SAVE_BUTTON}  id=applyWifiBtn

*** Keywords ***

Change SSID
    [Arguments]    ${NEW_SSID}    
    Navigate To Sub Menu    network    Wireless
    Wait Until Element Is Visible    ${SSID_FIELD}    timeout=10s
    Clear Element Text    ${SSID_FIELD}
    Input Text    ${SSID_FIELD}    ${NEW_SSID}
    Click Button    ${SSID_SAVE_BUTTON}
    Sleep    2s
    Capture Page Screenshot    ${SCREENSHOT_DIR}/ssid_change.png
