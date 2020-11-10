## Important Function
```sh
# Check used port (example on port 80)
sudo netstat -ltnp | grep -w ':80' 
sudo netstat -nlp | grep 80
# Kill by PID
kill -9 pid
```

## TODO

- Need to test the compose. 

- The compose minimum have 3 service:
    1. GCN --> Dockerfile (available) and Image (availabe in docker-hub) 
    2. Database --> MongoDB (Official Images availabe)
    3. Serving with Flask --> Dockerfile not yet ready, but the envs already done.

    