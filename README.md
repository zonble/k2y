# k2y

This is a simple web site running at https://k2y.herokuapp.com/, which
helps you to play playlists from [KKBOX](https://kkbox.com) without a
KKBOX account, since what we play are corresponding videos found on
[Youtube](https://youtube.com) instead of audio streaming from KKBOX.

The web site is built upon KKBOX's
[Python Developer SDK](https://github.com/KKBOX/OpenAPI-Python)
and [Flask](http://flask.pocoo.org/) web framework.

## Installation

To run the web site, you need

* A KKBOX API key. You can obtain one from KKBOX's
  [developer site](https://developer.kkbox.com/).
* A Youtube API Key. Please visit
  [Google Developer Console](https://console.developers.google.com)

Please edit `app.py` and `youtube.py` to input your KKBOX and Youtube
API key. Then please install all of the dependencies:

  pip install -r requirements.txt

Now, you can run the site by the following command

  python app.py

That's all!
