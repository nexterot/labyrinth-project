cd websocket_server
python3 socket_server.py 1>log.txt 2>err.txt &

cd ../http_server
python3 server.py 1>log.txt 2>err.txt &

cd ../js_frontend
python3 -m "http.server" 1>log.txt 2>err.txt &
