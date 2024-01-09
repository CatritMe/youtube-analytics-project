import isodate
import datetime

from src.channel import YoutubeAPI
from src.video import Video

class PlayList(YoutubeAPI):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_info = self.youtube.playlists().list(id=self.playlist_id,
                                                      part='snippet',
                                                      ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        duration = datetime.timedelta(0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        max_like_count = 0
        for video_id in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
        if like_count == max_like_count:
            return f"https://youtu.be/{video_id}"
