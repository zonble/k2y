#!/usr/bin/env python
# encoding: utf-8

import urllib
import urllib2
import json

YOUTUBE_SEARCH_API_END_POINT = 'https://www.googleapis.com/youtube/v3/'
YOUTUBE_KEY = 'YOUR_YOUTUBE_API_KEY'

class Youtube:
	def fetch_url(self, url):
		# print url
		f = urllib2.urlopen(url)
		r = f.read()
		return json.loads(r)

	def search(self, keyword, maxResults=50, page_token = ''):
		path = YOUTUBE_SEARCH_API_END_POINT + 'search?'
		parameters = {
			'key': YOUTUBE_KEY,
			'q': keyword,
			'part': 'snippet',
			'maxResults': maxResults,
			'pageToken': page_token,
			'fields': 'nextPageToken,pageInfo,items(id,snippet(title,thumbnails(medium(url),standard(url))))'
		}
		url = path + urllib.urlencode(parameters)
		return self.fetch_url(url)

	def fetch_channels_of_user(self, user_name, page_token = ''):
		path = YOUTUBE_SEARCH_API_END_POINT + 'channels?'
		parameters = {
			'key': YOUTUBE_KEY,
			'forUsername': user_name,
			'part': 'snippet',
			'maxResults': 50,
			'pageToken': page_token,
			'fields': 'nextPageToken,pageInfo,items(id,snippet(title,thumbnails(medium(url),standard(url))),contentDetails)'
		}
		url = path + urllib.urlencode(parameters)
		return self.fetch_url(url)

	def fetch_playlists_in_channel(self, channel_id, page_token = ''):
		path = YOUTUBE_SEARCH_API_END_POINT + 'playlists?'
		parameters = {
			'key': YOUTUBE_KEY,
			'channelId': channel_id,
			'part': 'snippet',
			'maxResults': 50,
			'pageToken': page_token,
			'fields': 'nextPageToken,pageInfo,items(id,snippet(title,thumbnails(medium(url),standard(url))),contentDetails)'
		}
		url = path + urllib.urlencode(parameters)
		return self.fetch_url(url)

	def fetch_videos_in_playlist(self, playlist_id, page_token = ''):
		path = YOUTUBE_SEARCH_API_END_POINT + 'playlistItems?'
		parameters = {
			'key': YOUTUBE_KEY,
			'playlistId': playlist_id,
			'part': 'snippet',
			'maxResults': 50,
			'pageToken': page_token,
			# 'fields': 'nextPageToken,pageInfo,items(id,snippet(title,thumbnails(medium(url),standard(url))),contentDetails)'
		}
		url = path + urllib.urlencode(parameters)
		return self.fetch_url(url)

	def fetch_videos_in_channel(self, channel_id):
		path = YOUTUBE_SEARCH_API_END_POINT + 'search?'
		parameters = {
			'key': YOUTUBE_KEY,
			'channelId': channel_id,
			'part': 'snippet',
			'order': 'date',
			'maxResults' : 50
		}
		url = path + urllib.urlencode(parameters)
		return self.fetch_url(url)
