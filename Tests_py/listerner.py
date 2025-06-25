from robot import result, running
from robot.api.interfaces import ListenerV3


class Example(ListenerV3):
    def __init__(self):
        print(f"Suite Suite !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def start_suite(self, data: running.TestSuite, result: result.TestSuite):
        print(f"Suite Suite !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Suite '{data.name}' starting.")

    def end_test(self, data: running.TestCase, result: result.TestCase):
        print(f"Test '{result.name}' ended with status {result.status}.")