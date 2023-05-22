import os
from dotenv import load_dotenv
# Импортируем build из googleapiclient.discovery позволяет создавать объекты для взаимодействия с YouTube API.
from googleapiclient.discovery import build
load_dotenv()
# задаем переменную нашего ключа API
api_key: str = os.getenv('YT_API_KEY')
# перемменная позволяет создавать объекты для взаимодействия с YouTube API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self._title = None
        self._description = None
        self._url = None
        self._subscriber_count = None
        self._video_count = None
        self._view_count = None
        self._fetch_channel_data()

    def _fetch_channel_data(self):
        channel = youtube.channels().list(
            part='snippet,statistics',
            id=self._channel_id
        ).execute()

        if 'items' in channel:
            item = channel['items'][0]
            self._title = item['snippet'].get('title')
            self._description = item['snippet'].get('description')
            self._url = f"https://www.youtube.com/channel/{self._channel_id}"
            self._subscriber_count = int(item['statistics'].get('subscriberCount', 0))
            self._video_count = int(item['statistics'].get('videoCount', 0))
            self._view_count = int(item['statistics'].get('viewCount', 0))

    @property
    def title(self):
        """Возвращает название канала."""
        return self._title

    @property
    def description(self):
        """Возвращает описание канала."""
        return self._description

    @property
    def url(self):
        """Возвращает ссылку на канал."""
        return self._url

    @property
    def subscriber_count(self):
        """Возвращает количество подписчиков канала."""
        return self._subscriber_count

    @property
    def video_count(self):
        """Возвращает количество видео на канале."""
        return self._video_count

    @property
    def view_count(self):
        """Возвращает общее количество просмотров канала."""
        return self._view_count

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате"""
