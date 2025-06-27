*** Settings ***
Library    RouterBngManager.py

*** Variables ***
${IP}      192.168.1.1
${REBOOTMSG}  "check old Router"

*** Keywords ***
Test BNG Connection
    ${response}=    RouterBngManager.Bng Connect   ${IP}
    #Log    ${response}
    ${status}=    RouterBngManager.Bng Reboot   ${REBOOTMSG}
    #Log    ${status} 