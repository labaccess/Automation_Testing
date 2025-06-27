import Exscript
from robot.api import logger
from custom_exceptions import *

global BNG_MODEL
BNG_MODEL = "Cisco"

def bng_connect(ip):
    logger.console(f"\n")
    logger.console(f"Connecting to {BNG_MODEL} at {ip}")
    #raise StepFailedError("Configure Ip Error", "Configuration step failed")
    return f"Connecting to {BNG_MODEL} at {ip}"

def bng_reboot(msg):
    logger.console(f"{BNG_MODEL} rebooted with MSG : {msg}")
    return f"{BNG_MODEL} rebooted with MSG : {msg}"