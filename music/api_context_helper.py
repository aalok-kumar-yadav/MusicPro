"""
    API helper is for calling Youtube API & getting desired data of songs
    there are helper function for Music View.
"""

from googleapiclient.discovery import build
import pafy
import requests
import json

# Google developer key for fetching data from youtube server
DEVELOPER_KEY = "AIzaSyDy7uIm3_OBOibaOpe34voXfvMeQfJuSpw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


# Helper function for searching song query
def get_search_result(search_query):
    search_response = youtube.search().list(
        q=search_query,
        part="id,snippet",
        maxResults=50
    ).execute()

    return_response = get_audio_context_list(search_response)
    return return_response


# Helper function for getting audio stream Url
def get_audio_stream_info(audio_id='gG2npfpaqsY'):
    return_response = {}
    stream_audio = {}

    audio_instance = pafy.new('https://www.youtube.com/watch?v='+audio_id)
    stream_audio['audio_id'] = audio_id
    stream_audio['title'] = audio_instance.title
    stream_audio['description'] = audio_instance.description
    stream_audio['thumbnail'] = audio_instance.thumb
    stream_audio['stream_url'] = audio_instance.getbestaudio().url
    stream_audio['duration'] = audio_instance.duration
    return_response['audio_stream'] = stream_audio
    return_response['related_audio'] = get_related_audio()
    return stream_audio


# Helper function for getting related audio
def get_related_audio(audio_id='gG2npfpaqsY'):
    print(audio_id)
    search_response = youtube.search().list(
        relatedToVideoId=audio_id,
        part="id,snippet",
        type='video',
        maxResults=15
    ).execute()

    related_list = get_audio_context_list(search_response)
    return related_list


# mini helper function for getting structured audio list
def get_audio_context_list(search_response):
    response_list = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == 'youtube#video':
            song_dict = {}
            song_dict['title'] = search_result['snippet']['title'][:30]
            song_dict['thumbnail'] = search_result['snippet']['thumbnails']['medium']['url']
            song_dict['description'] = search_result['snippet']['description'][:30]
            song_dict['audio_id'] = search_result['id']['videoId']
            song_dict['stream_url'] = ""

            response_list.append(song_dict)
    return response_list


# Helper function for retrieving video information
def get_video_info(audio_id):
    youtube.videos().list()
    search_response = youtube.videos().list(
        part='snippet, statistics',
        id=audio_id
    ).execute()

    context = {'viewCount': search_response['items'][0]['statistics']['viewCount'],
               'title': search_response['items'][0]['snippet']['title'],
               'description': search_response['items'][0]['snippet']['description'],
               'thumb': search_response['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
               }

    return context


# Helper function for getting recommended song
def get_recommended_song():
    recommended_list = get_search_result("mai ishaq ka raja song")
    return recommended_list[:10]


# Helper function for getting recommended song
def get_different_genre_song():
    genre_song_list = []
    return genre_song_list
