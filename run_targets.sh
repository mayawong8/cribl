set -e #exit if any commands fail
TARGETS=("target1" "target2")

#Creates an output folder for each target
for TARGET in "${TARGETS[@]}"; do
    mkdir -p "./output/$TARGET"
done

cat  > docker-compose.dynamic.yml << EOF
services:
#Dynamically generated target services for docker-compose file
EOF

for TARGET in "${TARGETS[@]}"; do
    cat >> docker-compose.dynamic.yml << EOF
    $TARGET:
        build: .
        command: ["node", "app.js", "target/"]
        volumes: ["./output/$TARGET:/usr/src/app/output"]
        profiles: ["app"]
        networks: [myapp]
EOF
done

cat >> docker-compose.dynamic.yml << EOF

    splitter:
        build: .
        command: ["node", "app.js", "splitter/"]
        depends_on:
EOF
#includes every target splitter is dependant on
for TARGET in "${TARGETS[@]}"; do
    echo "          - $TARGET" >> docker-compose.dynamic.yml
done

cat >> docker-compose.dynamic.yml << EOF
        profiles: ["app"]
        networks: [myapp]

    agent:
        build: .
        command: ["node", "app.js", "agent/"]
        depends_on: [splitter]
        profiles: ["app"]
        networks: [myapp]
  
    tests:
        build: 
            context: .
            dockerfile: Dockerfile.test
        volumes: ["./output:/tests/output"]
        profiles: ["tests"]
        networks: [myapp]


networks:
  myapp:
    driver: bridge

EOF

#start spp
docker compose -f docker-compose.dynamic.yml --project-name assignment --profile=app up -d --build
#run pytest suite
docker compose -f docker-compose.dynamic.yml --project-name assignment run --rm --build tests pytest -v
#stop all containers
docker compose -f docker-compose.dynamic.yml --project-name assignment --profile=app --profile=test down --remove-orphans

