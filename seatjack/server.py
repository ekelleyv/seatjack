import json
import qrcode

from flask import Flask

from seatjack.db import Session
from seatjack.tables import ImageTweet


app = Flask(__name__)

@app.route('/')
def index():
    return "TEST"

@app.route('/tickets')
def tickets():
    session = Session()
    image_tweets = session.execute("select min(id), min(tweet_id) as tweet_id, min(tweet_body) as tweet_body, original_image_url from image_tweets where barcode_value IS NOT NULL group by original_image_url")

    ticket_output = []

    for tweet in image_tweets:
        ticket = {
            "id" : tweet[0],
            "tweet_id" : tweet[1],
            "tweet_body" : tweet[2],
            "image_url" : tweet[3]
        }
        ticket_output.append(ticket)

    return json.dumps(ticket_output)

@app.route('/image_view/<int:id>')
def image_view(id):
    return "Image view"

@app.route('/barcode_view/<int:id>')
def barcode_view(id):
    return "Barcode view"

@app.route('/barcode/<int:id>')
def barcode(id):
    return "Barcode"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1123, debug=True)
