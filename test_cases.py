import os
import pytest
import pathlib
import time
import re

# start with a wait to verify workflow of other applications is complete
# may need to be longer depending on size of input of agent
@pytest.fixture(scope="session", autouse=True)
def wait():
    time.sleep(5)

def read_log(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return f.readlines()

# verify correct format
@pytest.mark.parametrize("log_path", [
    pathlib.Path("output/target1/events.log"),
    pathlib.Path("output/target2/events.log")
])
def test_format(log_path):
    content = read_log(log_path)
    for line in content:
        words = line.split()
        
        assert len(words) == 5, f"Line does not have exactly 5 words: {line!r}"
        assert words[:4] == ["This", "is", "event", "number"], f"Bad format in line: {line!r}"
        assert words[4].isdigit(), f"Non numerical event number in line: {line!r}"

@pytest.mark.parametrize("log_path", [
    pathlib.Path("output/target1/events.log"),
    pathlib.Path("output/target2/events.log")
])
def test_order_within_log_in_indiv_log(log_path):
    last = 0
    content = read_log(log_path)
    for i in range(len(content)):
        words = content[i].split()
        if (len(words) == 5) and words[4].isdigit():
            num = int(words[4])
            assert num > last, f"Event numbers are not increasing in {log_path}, on line {i}: {content[i]}"
            last = num
        else: 
            continue

@pytest.mark.parametrize("log_path", [
    pathlib.Path("output/target1/events.log"),
    pathlib.Path("output/target2/events.log")
])
def test_no_duplicates_in_indiv_log(log_path):
    seen = set()
    content = read_log(log_path)
    for i in range(len(content)):
        words = content[i].split()
        if (len(words) == 5) and words[:4] == ["This", "is", "event", "number"] and words[4].isdigit():
            num = int(words[4])
            assert num not in seen, f"Event numbers is a duplicate {log_path}, on line {i}: {content[i]}"
            seen.add(num)
        else:
            continue

def test_no_duplicates_across_logs():
    log_paths = [
        pathlib.Path("output/target1/events.log"),
        pathlib.Path("output/target2/events.log")
    ]
    seen = set()
    for log_path in log_paths:
        content = read_log(log_path)
        for i in range(len(content)):
            words = content[i].split()
            if (len(words) == 5) and words[:4] == ["This", "is", "event", "number"] and words[4].isdigit():
                num = int(words[4])
                assert num not in seen, f"Event numbers duplicate across all log, on line {i}: {content[i]}"
                seen.add(num)
            else: 
                continue