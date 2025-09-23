import os
import pytest
import pathlib

#  Helper: reads an event log file and returns its lines as a list
def read_log(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return f.readlines()

# Helper: parses a line and returns event number if valid
def parse_event_number(line):
    words = line.strip().split()
    if len(words) == 5 and words[:4] == ["This", "is", "event", "number"] and words[4].isdigit():
        if words[4][0] != "0":
            return int(words[4])
    return None

# Fixture: target1 and target2 log paths to test functions
@pytest.fixture(params=[
    pathlib.Path("output/target1/events.log"),
    pathlib.Path("output/target2/events.log")
], ids=["target1", "target2"])
def log_path(request) -> pathlib.Path:
    return request.param

#  Test case 1: Verify event log is not empty
def test_not_empty(log_path):
    content = read_log(log_path)
    assert len(content) > 0, f"Path {log_path} is empty"

#  Test case 2: Verify correct log format
#               - Ensure there are exactly 5 tokens in a line
#               - Ensure beginning is 'This is event number'
#               - Ensure ends with a positive integer, not starting with 0
def test_format(log_path):
    content = read_log(log_path)
    for line in content:
        #could use parse_event_number but I would prefer assert messages to be displayed for format test case
        words = line.split()
        
        assert len(words) == 5, f"Line does not have exactly 5 words: {line}"
        assert words[:4] == ["This", "is", "event", "number"], f"Bad format in line: {line}"
        assert words[4].isdigit() and words[4][0] != "0", f"Invalid event number in line: {line}"

#  Test case 3: Verify event numbers increase within a single log file
def test_order_within_log_in_indiv_log(log_path):
    last = 0
    content = read_log(log_path)
    for i in range(len(content)):
        num = parse_event_number(content[i])
        if num is not None:
            assert num > last, f"Event numbers are not increasing in {log_path}, on line {i}: {content[i]}"
            last = num

#  Test case 4: Verify no duplicate event numbers within a single log file
def test_no_duplicates_in_indiv_log(log_path):
    seen = set()
    content = read_log(log_path)
    for i in range(len(content)):
        num = parse_event_number(content[i])
        if num is not None:
            assert num not in seen, f"Duplicate event number {num} in {log_path}, on line {i}: {content[i]}"
            seen.add(num)

#  Test case 5: Verify no duplicate event numbers across all logs files
def test_no_duplicates_across_logs():
    log_paths = [
        pathlib.Path("output/target1/events.log"),
        pathlib.Path("output/target2/events.log")
    ]
    seen_target1 = set()
    seen_target2 = set()

    content_target1 = read_log(log_paths[0])

    for i in range(len(content_target1)):
        num = parse_event_number(content_target1[i])
        if num is not None:
            seen_target1.add(num)
    
    content_target2 = read_log(log_paths[1])
    for i in range(len(content_target2)):
        num = parse_event_number(content_target2[i])
        if num is not None:
            seen_target2.add(num)
    
    overlap = seen_target1.intersection(seen_target2)
    assert not overlap, f"Duplicate event number in both log files: count {len(overlap)}"

#  Test case 6: Verify no missing lines, all events from 1-1,000,000 are present across all log files
def test_no_missing_logs():
    log_paths = [
        pathlib.Path("output/target1/events.log"),
        pathlib.Path("output/target2/events.log")
    ]
    seen = set()
    for log_path in log_paths:
        content = read_log(log_path)
        for line in content:
            num = parse_event_number(line)
            if num is not None:
                seen.add(num)
    assert seen == set(range(1,1000001)), f"Events are missing or out of range, counted {len(seen)}"