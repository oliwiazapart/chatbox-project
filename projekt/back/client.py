import websocket
import json

def on_message(ws, message):
    response = json.loads(message)
    print(f"A: {response['answer']} \n" )

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    queries = ["Can you recommend perfumes with oriental notes?"]
    for query in queries:
        print(f"Q: {query}")
        message = {"question": query}
        ws.send(json.dumps(message))

if __name__ == "__main__":
    websocket_url = "ws://127.0.0.1:8000/ws"
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
