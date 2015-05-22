from StringIO import StringIO

import requests
import zbar
from PIL import Image as pImage

from seatjack.db import Session
from seatjack.tables import ImageTweet

class TicketParser(object):

    def _barcode_from_image(self, url):
        r = requests.get(url)
        # print r.status_code

        f = StringIO(r.content)
        img = pImage.open(f).convert('L')

        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')

        width, height = img.size
        zbar_image = zbar.Image(width, height, 'Y800', img.tostring())

        scanner.scan(zbar_image)

        for symbol in zbar_image:
            print symbol.data
            return symbol.data


    def parse(self):
        session = Session()

        tweets = session.query(ImageTweet).filter(ImageTweet.parsed == 0).all()

        for i, tweet in enumerate(tweets):
            print i
            barcode = self._barcode_from_image(tweet.original_image_url)
            if barcode:
                tweet.barcode_value = barcode
            tweet.parsed = 1
            session.commit()





if __name__ == '__main__':
    tp = TicketParser()
    tp.parse()



