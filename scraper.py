# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from api import get_video_entries, get_channel_entry, get_search_video_id


def show_video_entries(video_id: str):
    entries = get_video_entries(video_id)
    print('id: ', entries.id())
    print('title: ', entries.title())
    print('description: ', entries.description())
    print('channel_id: ', entries.channel_id())
    print('thumbnail_url: ', entries.thumbnail_url())
    print('published_at: ', entries.published_at())
    print('like_count: ', entries.like_count())
    print('dislike_count: ', entries.dislike_count())
    print('favorite_count: ', entries.favorite_count())
    print('comment_count: ', entries.comment_count())
    print('duration: ', entries.duration())
    print('channel_title: ', entries.channel_title())
    print('tags: ', entries.tags())
    print('category_id: ', entries.category_id())
    print('original_url: ', entries.original_url())
    print()


def show_channel_entries(channel_id: str):
    entries = get_channel_entry(channel_id)
    print('id: ', entries.id())
    print('title: ', entries.title())
    print('thumbnail_url: ', entries.thumbnail_url())
    print('view_count: ', entries.view_count())
    print('comment_count: ', entries.comment_count())
    print('subscriber_count: ', entries.subscriber_count())
    print('video_count: ', entries.view_count())
    print('customUrl: ', entries.custom_url())
    print('home_url: ', entries.home_url())
    print()


def show_search_video_ids(keyword: str, limit: int = 10):
    video_ids = get_search_video_id(keyword, int(limit))
    for video_id in video_ids:
        print(video_id)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--video_ids', nargs='+', type=str, help='video_idを指定して動画の情報を取得する')
    parser.add_argument('--channel_ids', nargs='+', type=str, help='channel_idを指定してチャンネル情報を取得する')
    parser.add_argument('--search_word', nargs='?', type=str, help='検索したいキーワードを指定してvideo_idを取得する')
    args = parser.parse_args()
    if args.video_ids:
        for video_id in args.video_ids:
            show_video_entries(video_id)
    if args.channel_ids:
        for channel_id in args.channel_ids:
            show_channel_entries(channel_id)
    if args.search_word:
        show_search_video_ids(args.search_word)
    if not args.video_ids and not args.channel_ids and not args.search_word:
        print('Try \'python scraper.py --help\'.')
