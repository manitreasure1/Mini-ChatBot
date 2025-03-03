
from app import create_app
# from app.extensoins import socketio

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)