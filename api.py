# -*- coding: utf-8 -*-
import requests
import dateutil.parser
import isodate

# ここにYouTubeのAPI_KEYを入れる
AUTH_KEY = ''


class VideoEntry:
    """動画の情報を取得する"""
    def __init__(self, items):
        self.items = items

    def id(self):
        return self.items['id']

    def title(self) -> str:
        return self.items['snippet']['title']

    def channel_id(self) -> str:
        return self.items['snippet']['channelId']

    def description(self) -> str:
        return self.items['snippet']['description']

    def thumbnail_url(self) -> str:
        t = self.items['snippet']['thumbnails']
        return (t.get('standard') or t.get('high') or t.get('medium') or t.get('default')).get('url') or ''

    def published_at(self):
        snippet = self.items['snippet']
        return dateutil.parser.parse(snippet['publishedAt']) if 'publishedAt' in snippet else None

    def view_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['viewCount']) if 'viewCount' in statistics else None

    def like_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['likeCount']) if 'likeCount' in statistics else None

    def dislike_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['dislikeCount']) if 'dislikeCount' in statistics else None

    def favorite_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['favoriteCount']) if 'favoriteCount' in statistics else None

    def comment_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['commentCount']) if 'commentCount' in statistics else None

    def duration(self):
        content_details = self.items.get('contentDetails', {})
        if 'duration' in content_details:
            return int(isodate.parse_duration(content_details['duration']).total_seconds())
        else:
            return None

    def channel_title(self):
        return self.items['snippet'].get('channelTitle') or ''

    def tags(self):
        snippet = self.items['snippet']
        return ','.join(snippet['tags']) if 'tags' in snippet else ''

    def category_id(self):
        snippet = self.items['snippet']
        return int(snippet['categoryId']) if 'categoryId' in snippet else None

    def original_url(self):
        return 'https://www.youtube.com/watch?v={}'.format(self.id())


def get_video_entries(video_id):
    endpoint = ('https://www.googleapis.com/youtube/v3/videos'
                '?id={id}&key={key}'
                '&part=status,statistics,snippet,contentDetails'
                '&hl=ja'
                ).format(id=video_id, key=AUTH_KEY)
    r = requests.get(endpoint)
    json_data = r.json()
    items = json_data['items'][0]
    return VideoEntry(items)


class ChannelEntry:
    """チャンネルの情報を取得する"""
    def __init__(self, items):
        self.items = items

    def id(self):
        return self.items['id']

    def title(self) -> str:
        return self.items['snippet']['title']

    def thumbnail_url(self):
        t = self.items['snippet']['thumbnails']
        return (t.get('high') or t.get('medium') or t.get('default') or {}).get('url') or ''

    def view_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['viewCount']) if 'viewCount' in statistics else None

    def comment_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics['commentCount']) if 'commentCount' in statistics else None

    def subscriber_count(self):
        statistics = self.items.get('statistics', {})

        if len(statistics) <= 0 or statistics.get('hiddenSubscriberCount', False):
            return None
        return int(statistics.get('subscriberCount', 0))

    def video_count(self):
        statistics = self.items.get('statistics', {})
        return int(statistics.get('videoCount', 0)) if 'videoCount' in statistics else None

    def custom_url(self):
        snippet = self.items['snippet']
        return 'https://www.youtube.com/user/{}'.format(snippet['customUrl']) if 'customUrl' in snippet else None

    def home_url(self):
        return 'https://www.youtube.com/channel/{}'.format(self.id())


def get_channel_entry(channel_id):
    endpoint = ('https://www.googleapis.com/youtube/v3/channels'
                '?part=id,snippet,statistics'
                '&id={id}&key={key}'
                '&hl=ja'
                ).format(id=channel_id, key=AUTH_KEY)
    r = requests.get(endpoint)
    json_data = r.json()
    items = json_data['items'][0]
    return ChannelEntry(items)


def get_search_video_id(keyword, limit):
    """動画を検索して結果のvideo_idリストを返す"""
    video_ids = []
    params = {"key": AUTH_KEY, "part": "snippet", "q": keyword,
              "maxResults": limit, "order": "date", "type": "video"}
    url = 'https://www.googleapis.com/youtube/v3/search'
    r = requests.get(url, params=params)
    json_data = r.json()
    for item in json_data["items"]:
        video_id = item["id"]["videoId"]
        video_ids.append(video_id)
    return video_ids
