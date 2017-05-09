cd websocket_server
python3 socket_server.py &

cd ../http_server
python3 server.py &

cd ../js_frontend
./start_server.sh &

