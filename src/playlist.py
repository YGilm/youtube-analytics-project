import isodate
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()  # Загрузка переменных среды из файла .env
api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        """
        Инициализация объекта PlayList.
        Args: playlist_id (str): Идентификатор плейлиста.
        """
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.playlist_response = self.get_playlist_response()
        self.title = self.playlist_response['items'][0]['snippet']['title']
        self.playlist_videos = self.get_playlist_videos()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_video_response()

    def get_playlist_response(self):
        """
        Получение информации о плейлисте из YouTube API.
        Returns: dict: Ответ API с информацией о плейлисте.
        """
        return youtube.playlists().list(id=self.playlist_id, part='snippet').execute()

    def get_playlist_videos(self):
        """
        Получение списка видео в плейлисте из YouTube API.
        Returns: dict: Ответ API со списком видео в плейлисте.
        """
        return youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()

    def get_video_response(self):
        """
        Получение информации о видео из YouTube API.
        Returns: dict: Ответ API с информацией о видео.
        """
        return youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """
        Суммарная длительность плейлиста.
        Returns: datetime.timedelta: Объект timedelta с суммарной длительностью плейлиста.
        """
        duration_sum = timedelta(seconds=0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_sum += duration
        return duration_sum

    def show_best_video(self):
        """
        Получение ссылки на самое популярное видео из плейлиста (по количеству лайков).
        Returns: str: Ссылка на самое популярное видео.
        """
        most_liked_video = max(self.video_response['items'], key=self.get_like_count)
        return f"https://youtu.be/{most_liked_video['id']}"

    @staticmethod
    def get_like_count(video):
        """
        Получение количества лайков для видео.
        Args: video (dict): Информация о видео.
        Returns: int: Количество лайков.
        """
        return int(video['statistics']['likeCount'])
