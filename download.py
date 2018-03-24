# -*- coding: utf-8 -*-
import os
from pytube import YouTube
from argparse import ArgumentParser

# 保存するパス
PATH = os.getcwd() + '/videos'


def download_mp4(video_ids):
    for video_id in video_ids:
        url = 'https://www.youtube.com/watch?v={}'.format(video_id)
        yt = YouTube(url=url)
        print('\"' + yt.title + '\" is downloading.')
        files = os.listdir(PATH)
        if yt.title+".mp4" in files:
            print("already exist.")
            continue
        yt.streams.first().download(output_path=PATH)


if __name__ == '__main__':
    parser = ArgumentParser(description='Youtube動画のmp4をダウンロードするスクリプト')
    parser.add_argument('--target', nargs='+', type=str, help='video_idを指定する', required=True)
    args = parser.parse_args()
    video_ids = args.target
    print('start download.')
    if not os.path.exists(PATH):
        os.mkdir('videos')
    download_mp4(video_ids)
    print('finish.')
