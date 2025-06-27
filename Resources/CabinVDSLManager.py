import Exscript
from Exscript.protocols import SSH2,Account
from robot.api import logger
from custom_exceptions import *
import re 
from Exscript.protocols.drivers import one_os

one_os.OneOSDriver.auto_authorize = lambda *a, **kw: None

Huawei_vendor_id_re = re.compile(r"\s+Vendor-ID\s+\:\s+(\w+)")
Huawei_CPE_card_location = re.compile(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")

Cabin_list ={
                "Huawei":{"ip":"10.60.120.147" ,"User":"tednoc","Pass":"tednoc#123"}
             }

def Connect_Cabin_SSH2(cabin_type):
    logger.console(f"✅ Connecting to {Cabin_list[cabin_type]["ip"]}")
    try:
        conn = SSH2()
        conn.connect(Cabin_list[cabin_type]["ip"])
        account = Account(Cabin_list[cabin_type]["User"],Cabin_list[cabin_type]["Pass"])
        conn.set_driver(one_os.OneOSDriver())
        conn.login(account)
        conn.set_prompt("[#]")
        conn.execute('enable')
        conn.execute('undo terminal monitor')
        print(conn.response)
        return conn,True
    except Exception as Error:
        logger.console(f"Failed connecting to {Cabin_list[cabin_type]["ip"]} with Error {Error}")
        return "",False
    
def cabin_conn_execute_cmd(conn,cmd):
    try:
        conn.execute(cmd)
        return conn.response , True
    except:
        return "", False

def cabin_get_vendor_id(cabin_type,ont_location):
    if cabin_type == "Huawei":
        cmd = f"display ont version {ont_location}"
        logger.console(f"cabin_check_vendor_ID {cmd}")
        conn,result = Connect_Cabin_SSH2(cabin_type)
        if result:
            resp,result = cabin_conn_execute_cmd(conn,cmd)
            if result:
                vendor_id = Huawei_vendor_id_re.findall(resp)[0]
                logger.console(f"✅ cabin_check_vendor_ID is {vendor_id}")
                return vendor_id
            else:
                return f"Failed cabin_check_vendor_ID function"

        return f"cabin_check_vendor_ID"
    else:
        return f"Failed location !!!!!!!!!!!"
    

def cabin_restart_cpe(cabin_type,ont_location):
    if cabin_type == "Huawei":
        logger.console(f"Reseting CPE from cabin type : {cabin_type} ONT_location : {ont_location}")
        conn,result = Connect_Cabin_SSH2(cabin_type)
        if result:
            logger.console(f"Reseting CPE from cabin apply : config")
            resp,result = cabin_conn_execute_cmd(conn,"config")
            if result:
                location_matrix = Huawei_CPE_card_location.findall(ont_location)[0]
                logger.console(f"Reseting CPE from cabin apply : interface gpon {location_matrix[0]}/{location_matrix[1]}")
                resp,result = cabin_conn_execute_cmd(conn,f"interface gpon {location_matrix[0]}/{location_matrix[1]}")
                logger.console(f"Reseting CPE from cabin apply : ont reset {location_matrix[2]} {location_matrix[3]}")
                resp,result = cabin_conn_execute_cmd(conn,f"ont reset {location_matrix[2]} {location_matrix[3]}")
                logger.console(f"Reseting CPE from cabin apply : quit")
                resp,result = cabin_conn_execute_cmd(conn,f"quit")
            else:
                return f"Failed cabin_check_vendor_ID function"

        return f"cabin_check_vendor_ID"
    else:
        return f"Failed location !!!!!!!!!!!"
    
if __name__ == "main":
    cabin_check_vendor_ID("Huawei","0 5 0 16")