from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных среды из файла .env

api_key = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео"""

    def __init__(self, video_id: str):
        """
        Инициализация экземпляра с идентификатором видео.
        Получение и установка фактического названия видео с помощью вызова API.
        """
        self._video_id = video_id
        self._title = None
        self._description = None
        self._url = None
        self._view_count = None
        self._like_count = None

        try:
            self._fetch_video_data()
        except IndexError:
            print('Видео не найдено')

    def _fetch_video_data(self):
        """
        Получает данные о видео с помощью YouTube API.
        """
        video = youtube.videos().list(
            part='snippet,statistics',
            id=self._video_id
        ).execute()

        if 'items' in video:
            item = video['items'][0]
            self._title = item['snippet'].get('title')
            self._description = item['snippet'].get('description')
            self._url = f"https://www.youtube.com/watch?v={self._video_id}"
            self._view_count = int(item['statistics'].get('viewCount', 0))
            self._like_count = int(item['statistics'].get('likeCount', 0))
    def __str__(self):
        """
        Возвращает строковое представление экземпляра класса Video.

        :return: Строковое представление экземпляра класса Video.
        """
        return self._title

    @property
    def title(self):
        return self._title

    @property
    def like_count(self):
        return self._like_count


class PLVideo(Video):
    """Класс для видео в плейлисте"""

    def __init__(self, video_id: str, playlist_id: str):
        """
        Инициализация экземпляра с идентификатором видео и идентификатором плейлиста.
        """
        super().__init__(video_id)
        self._playlist_id = playlist_id
