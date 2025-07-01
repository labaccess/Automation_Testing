*** Settings ***
Library    SeleniumLibrary
Resource   ../resources/sidebar_keywords.robot


*** Keywords ***
Change MTU Value
    Navigate To Sub Menu    network    Broadband
    Wait Until Element Is Visible    xpath=//table[@id="Network_Broadband_Broad_Table"]
    Click Element    xpath=(//span[@id="Network_Broadband_Broad_Edit1"])[1]
    Wait Until Element Is Visible    id=bb_mtuValue
    Clear Element Text    id=bb_mtuValue
    Input Text    id=bb_mtuValue    1492
    Click Button    id=WANInterface_btnsave
    Sleep    3s
