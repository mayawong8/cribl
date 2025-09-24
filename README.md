# cribl

## How to use:

run ./run_targets.sh from terminal 

```bash
docker compose -f docker-compose.dynamic.yml --project-name assignment --profile=app up -d --build #start app
docker compose -f docker-compose.dynamic.yml --project-name assignment run --rm --build tests pytest -v #exit code after test suite completes
docker compose -f docker-compose.dynamic.yml --project-name assignment --profile=app --profile=test down --remove-orphans #clean up

rm -rf ./output/target1 ./output/target2 #clean up generated logs (while testing 2 targets)


Assumptions:

- The agent receives a log with 1 to 1,000,000 event lines (incrementing by 1) formatted accordingly: "This is event number <positive integer that does not start with a 0>"
- Each event number is expected to be unique, without any gaps or duplicates

Splitter behavior:
- The splitter is intended to "receive data from an agent and randomly splits the data between 2 configured target hosts" 
- Splitter only splits on the first newline per chunk which can cause uneven distribution and cut lines across logs 
- I noticed some lines are cut

Strategy:

1.  Containerization: 
    - each host runs its own docker container which ensures isolated and reproducible environments
2. Orchestration
    - docker-compose manages service dependencies and networking. Start up order: targets --> splitter --> agent --> tests
3. Scalability
    - The pipeline can be extended by adding more target services. Additionally, the splitter distributes the load, making the system suitable for processing larger log volumes. I also dynamically create the docker-compose.dynamic.yml to support multiple targets.
4. Test Automation
    - the test container autonomously verifies correctness of log format, uniqueness of event numbers, and complete coverage of all expected events of events (1 to 1M events)



Test Cases:

1. Verify event log is not empty
2. Verify correct log format
    - Ensure there are exactly 5 tokens in a line
    - Ensure beginning is 'This is event number'
    - Ensure ends with a positive integer not starting with 0
3. Verify event numbers increase within a single log file
4. Verify no duplicate event numbers within a single log file
5. Verify no duplicate event numbers across all logs files
6. Verify no missing lines, all events from 1 to 1,000,000 are present across all log files

