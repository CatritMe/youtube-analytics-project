import os
from googleapiclient.discovery import build
import json

class YoutubeAPI:
    api_key: str = os.getenv('YOU-TUBE API-KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

class Channel(YoutubeAPI):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(channel['items'][0]['statistics']['viewCount'])


    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file):
        data = {'channel_id' : self.__channel_id,
                'title' : self.title,
                'description' : self.description,
                'url' : self.url,
                'subscriber_count' : self.subscriber_count,
                'video_count' : self.video_count,
                'view_count' : self.view_count}
        with open(os.path.abspath(file), 'w', encoding='utf=8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
