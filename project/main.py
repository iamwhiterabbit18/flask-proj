from website import create_app, socketio

app = create_app();

if __name__ == '__main__':
  socketio.run(app, debug=True, host="192.168.1.39", port=5000)