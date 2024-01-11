from src.channel import YoutubeAPI

class Video(YoutubeAPI):


    def __init__(self, video_id):
        self.video_id = video_id
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
            self.title: str = video_response['items'][0]['snippet']['title']
            self.url = f'https://youtu.be/{self.video_id}'
            self.view_count: int = int(video_response['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(video_response['items'][0]['statistics']['likeCount'])
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None



    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
