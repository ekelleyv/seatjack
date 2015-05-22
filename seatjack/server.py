# -*- coding: utf-8 -*-

import json
from StringIO import StringIO

import qrcode
from flask import Flask
from flask import render_template, send_file
import bleach

from seatjack.db import Session
from seatjack.tables import ImageTweet


app = Flask(__name__)

print "STARTING SERVER"

def _get_tickets():
    session = Session()
    image_tweets = session.execute("select min(id), min(tweet_id) as tweet_id, min(tweet_body) as tweet_body, original_image_url from image_tweets where barcode_value IS NOT NULL group by original_image_url ORDER BY created_at DESC")

    ticket_output = []

    for tweet in image_tweets:
        ticket = {
            "id" : tweet[0],
            "tweet_id" : tweet[1],
            "tweet_body" : bleach.linkify(tweet[2].decode('utf-8')),
            "image_url" : tweet[3]
        }
        ticket_output.append(ticket)
    return ticket_output

def _get_ticket(ticket_id):
    session = Session()
    tweet = session.query(ImageTweet).filter(ImageTweet.id == ticket_id).first()

    ticket = {
        "id" : tweet.id,
        "tweet_id" : tweet.tweet_id,
        "tweet_body" : bleach.linkify(tweet.tweet_body.decode('utf-8')),
        "image_url" : tweet.original_image_url,
        "barcode_value" : tweet.barcode_value
    }
    return ticket

def _make_qrcode(value):
    b = qrcode.make(value, border=2)
    return b

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'png')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/')
def index():
    print "in get home"
    from seatjack.config import DATABASE_URL
    print DATABASE_URL
    return render_template('tickets.html', tickets=_get_tickets())

@app.route('/tickets')
def tickets():
    ticket_output = _get_tickets()

    return json.dumps(ticket_output)

@app.route('/summary/<int:ticket_id>')
def summary(ticket_id):
    return render_template('summary.html', ticket=_get_ticket(ticket_id))

@app.route('/ticket/<int:ticket_id>')
def barcode_view(ticket_id):
    return render_template('ticket.html', ticket=_get_ticket(ticket_id))

@app.route('/barcode/<int:ticket_id>')
def barcode(ticket_id):
    ticket = _get_ticket(ticket_id)
    barcode = _make_qrcode(ticket["barcode_value"])
    return serve_pil_image(barcode)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1123, debug=True)
