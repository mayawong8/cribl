import os
import pytest
import time

# start with a wait to verify workflow of other applications is complete
# may need to be longer depending on size of input of agent
@pytest.fixture(scope="session", autouse=True)
def wait():
    time.sleep(5)

def read_log(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()
    
def test_target1_log():
    content = read_log("output/target1/events.log")
    assert "This is event number" in content, "Target1 log missing expected events"

def test_target2_log():
    content = read_log("output/target2/events2.log")
    assert "This is event number" in content, "Target2 log missing expected events"