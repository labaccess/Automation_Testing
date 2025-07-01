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

*** Keywords ***
Verify MTU Value
    Navigate To Sub Menu    network    Broadband
    Wait Until Element Is Visible    xpath=//table[@id="Network_Broadband_Broad_Table"]
    Click Element    xpath=(//span[@id="Network_Broadband_Broad_Edit1"])[1]
    Wait Until Element Is Visible    id=bb_mtuValue
    ${current_value}=    Get Value    id=bb_mtuValue
    ${adjusted_value}=    Evaluate    int(${current_value}) - 8
    Should Be Equal As Strings    ${adjusted_value}    1492
    Log To Console    MTU value is correctly set to: ${current_value}
    Log To Console    MTU value is Adjusted set to: ${adjusted_value}


