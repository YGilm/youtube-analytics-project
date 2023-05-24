from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных среды из файла .env

api_key = os.getenv('YT_API_KEY')
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

    def print_info(self):
        """Выводит информацию о канале на консоль."""
        print(f"Название канала: {self._title}")
        print(f"Описание канала: {self._description}")
        print(f"Ссылка на канал: {self._url}")
        print(f"Количество подписчиков: {self._subscriber_count}")
        print(f"Количество видео: {self._video_count}")
        print(f"Общее количество просмотров: {self._view_count}")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return youtube

    def to_json(self, file_path):
        """Сохраняет значения атрибутов экземпляра Channel в JSON-файл."""
        data = {
            'id': self._channel_id,
            'title': self._title,
            'description': self._description,
            'url': self._url,
            'subscriber_count': self._subscriber_count,
            'video_count': self._video_count,
            'view_count': self._view_count
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    @property
    def title(self):
        """Возвращает название канала."""
        return self._title

    @property
    def video_count(self):
        """Возвращает количество видео на канале."""
        return self._video_count

    @property
    def url(self):
        """Возвращает ссылку на канал."""
        return self._url