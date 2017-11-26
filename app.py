#!/usr/bin/env python
# encoding: utf-8

import os
from flask import *
from kkbox_developer_sdk.auth_flow import KKBOXOAuth
from kkbox_developer_sdk.api import KKBOXAPI
from werkzeug.contrib.cache import SimpleCache
from youtube import *

import re
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)
app.name = u"KKBOX 歌單/排行榜"
app.description = u"使用 KKBOX Open API 做出來的小 demo。讓您可以用 Youtube 播放 KKBOX 歌單！"
cache = SimpleCache()

@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
	"""Converts newlines into <p> and <br />s."""
	value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
	paras = re.split('\n{2,}', value)
	paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
	paras = u'\n\n'.join(paras)
	return Markup(paras)

# refers to application_top
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
CLIENT_ID = 'YOUR_API_KEY'
CLIENT_SECRET = 'YOUR_API_SECRET'
auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
token = auth.fetch_access_token_by_client_credentials()
api = KKBOXAPI(token)
youtube = Youtube()

def get_chart_category():
	try:
		categories = api.chart_fetcher.fetch_charts().get('data')
		cache.set('chart_category', categories, timeout=60 * 60 * 12)
		return categories
	except Exception as e:
		return []

def get_playlist_category():
	try:
		categories = api.feature_playlist_category_fetcher.fetch_categories_of_feature_playlist().get('data')
		cache.set('playlist_category', categories, timeout=60 * 60 * 12)
		return categories
	except Exception as e:
		return []

def get_feature_playlists_category_info(category_id):
	try:
		feature_playlists = api.feature_playlist_category_fetcher.fetch_feature_playlist_by_category(category_id)
		cache.set('feature_playlists_info_' + category_id, feature_playlists, timeout=60 * 60 * 12)
		return feature_playlists
	except Exception as e:
		return []

def get_feature_playlists_in_category(category_id):
	try:
		feature_playlists = api.feature_playlist_category_fetcher.fetch_playlists_of_feature_playlist_category(category_id).get('data')
		cache.set('feature_playlists_' + category_id, feature_playlists, timeout=60 * 60 * 12)
		return feature_playlists
	except Exception as e:
		return []

def get_feature_playlists():
	try:
		feature_playlists = api.feature_playlist_fetcher.fetch_feature_playlists().get('data')
		cache.set('feature_playlists', feature_playlists, timeout=60 * 60 * 12)
		return feature_playlists
	except Exception as e:
		return []

def get_playlist(playlist_id):
	try:
		playlist = api.shared_playlist_fetcher.fetch_shared_playlist(playlist_id)
		tracks = playlist.get('tracks', {}).get('data', [])
		count = min(20, len(tracks))
		tracks = tracks[0:count]

		for track in tracks:
			name = track['name'].encode('utf-8')
			snippet = youtube.search(name, 1)
			items = snippet.get('items', [])
			if items.count > 0:
				track['youtube'] = items[0]
		playlist['tracks'] = tracks
		cache.set('playlist_' + playlist_id, playlist, timeout=60 * 60 * 1)
		return playlist
	except Exception as e:
		return {'title': '', 'description': '', 'tracks': []}

def get_playlist_page(playlist_id):
	categories = cache.get('chart_category')
	if categories == None:
		categories = get_chart_category()
	
	playlist_categories = cache.get('playlist_category')
	if playlist_categories == None:
		playlist_categories = get_playlist_category()

	playlist = cache.get('playlist_' + playlist_id)
	if playlist == None:
		playlist = get_playlist(playlist_id)
	return render_template('playlist.html',
		app=app, 
		categories=categories,
		playlist_categories=playlist_categories,
	 	playlist=playlist)

@app.route('/playlists/<playlist_id>')
def show_playlist(playlist_id):
	return get_playlist_page(playlist_id)

def get_category(category_id):
	categories = cache.get('chart_category')
	if categories == None:
		categories = get_chart_category()
	
	playlist_categories = cache.get('playlist_category')
	if playlist_categories == None:
		playlist_categories = get_playlist_category()

	feature_playlists_info = cache.get('feature_playlists_info' + category_id)
	if feature_playlists_info == None:
		feature_playlists_info = get_feature_playlists_category_info(category_id)

	feature_playlists = cache.get('feature_playlists_' + category_id)
	if feature_playlists == None:
		feature_playlists = get_feature_playlists_in_category(category_id)

	return render_template('index.html',
		app=app,
		feature_playlists_info=feature_playlists_info,
		feature_playlists=feature_playlists,
		playlist_categories=playlist_categories,
		categories=categories)

@app.route('/category/<category_id>')
def show_category(category_id):
	return get_category(category_id)

def get_homepage():
	categories = cache.get('chart_category')
	if categories == None:
		categories = get_chart_category()
	
	playlist_categories = cache.get('playlist_category')
	if playlist_categories == None:
		playlist_categories = get_playlist_category()

	feature_playlists = cache.get('feature_playlists')
	if feature_playlists == None:
		feature_playlists = get_feature_playlists()
	return render_template('index.html',
		app=app,
		feature_playlists=feature_playlists, 
		playlist_categories=playlist_categories,
		categories=categories)

@app.route('/')
def hello():
	return get_homepage()

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
