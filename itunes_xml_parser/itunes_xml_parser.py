#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""parse iTunes XML
Example:
   python itunes_xml_parse.py (itunes_xml_path)
"""

import os
import sys
import collections

import xml.etree.ElementTree as etree_dummy
from lxml import etree


def usage():
    print("usage: {0} (itunes_xml_path)".format(sys.argv[0]))


def dfs(root, depth):
    for child in root:
        print ("  " * depth, child.tag, ": ", child.text )
        dfs(child, depth + 1)

def artists_with_many_songs(song_info_list, top = 10):

    counter = collections.Counter()
    for song_info in song_info_list:
        # たまに"Artist"の項目が空のことがある
        if "Artist" not in song_info:
            continue
        # podcastは除外
        elif "Genre" in song_info and song_info["Genre"] == "Podcast":
            continue

        counter[ song_info["Artist"] ] += 1

    # 曲数の多いものの上位top個を返す
    return counter.most_common(10)
    
def most_played_songs(song_info_list, top = 10):
    top_ranked = sorted(song_info_list, key=lambda s: int(s.get("Play Count", "0")), reverse=True)[:top]
    return [ (i.get("Name", ""), i.get("Play Count", "0")) for i in top_ranked ]
    
def most_played_artists(song_info_list, top = 10):
    artist2play = collections.Counter()
    for song_info in song_info_list:
        if "Artist" in song_info and "Play Count" in song_info:
            artist2play[ song_info["Artist"] ] += int(song_info["Play Count"])

    return artist2play.most_common(top)
    
def release_year(song_info_list):
    release_year = collections.Counter()
    for song_info in song_info_list:
        if "Year" in song_info:
            y = int(song_info["Year"])
            release_year[y] = release_year.get(y, 0) + 1
    return release_year

def play_times_histogram(song_info_list):
    pass
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    # XMLを読み込み
    xml_path = sys.argv[1]
    tree = etree.parse(xml_path)
    
    root = tree.getroot()

    # dfs(root, 1)

    songs = root.findall('./dict/dict/dict')

    # 曲ごとの情報を取得
    song_info_list = [] 
    for song in songs:
        song_info = {}
        key = ""
        for element in song:
            if element.tag == "key":
                key = element.text
            else:
                # TODO: keyの種類によって, 文字列から適切な型に変換すべき
                song_info[ key ] = element.text
        song_info_list.append( song_info )

        # for k,v in song_info.items():
        #     print(k, ": ", v)
        
        
    print(len(song_info_list))

    print(artists_with_many_songs(song_info_list, 30))

    print(most_played_songs(song_info_list, 30))

    print(most_played_artists(song_info_list, 30))

    print(release_year(song_info_list))

    
        
    

