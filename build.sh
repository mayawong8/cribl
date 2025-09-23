set -e #exit if any commands fail
docker compose --profile=app up -d --build #start app in the background
docker compose run --rm --build tests pytest -v
#docker compose --profile=tests up --build --exit-code-from tests #exit code after test suite completes
docker compose --profile=tests --profile=app down #clean up