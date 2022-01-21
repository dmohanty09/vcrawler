import sys
import os

from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors

CHANNEL_NAME = 'smosh'
PLAYLIST_ID = 'PLShD8ZZW7qjkTzS17ENOnfpk6Sq220k1z'

CACHE_DIR = './cache'
TRANSCRIPTS_DIR = CACHE_DIR + '/video_transcripts'

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

api_service_name = "youtube"
api_version = "v3"

class YoutubeScraper:

    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    def __init__(self):
        self.youtube = googleapiclient.discovery.build(api_service_name,
                                                       api_version,
                                                       developerKey=YoutubeScraper.GOOGLE_APPLICATION_CREDENTIALS)

    def get_most_popular(self, page_token=None):
        print('Getting first 5 popular videos..')
        request = self.youtube.videos().list(
            part="statistics",
            chart="mostPopular",
            pageToken=page_token,
            regionCode="US"
        )
        response = request.execute()
        return response

    def get_playlist_by_id(self, playlist_id, page_token=None):
        print('Getting first 5 playlist videos..')
        request = self.youtube.playlistItems().list(
            part="snippet",
            pageToken=page_token,
            playlistId = playlist_id
        )
        response = request.execute()
        return request, response

    def get_playlist(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId = playlist_id
        )
        response = request.execute()
        print(response)
        v_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
        self.transcribe_videos(v_ids)
        request = self.youtube.playlistItems().list_next(request, response)
        while(request is not None):
            response = request.execute()
            print(response)
            v_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
            self.transcribe_videos(v_ids)
            request = self.youtube.playlistItems().list_next(request, response)

    def transcribe_video(self, video_id):
        print(f'Transcribing Video ID: {video_id}')
        formatted_list = []
        filename = os.path.join(TRANSCRIPTS_DIR, video_id + '.csv')
        try:
            if not os.path.isfile(filename):
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                formatted_list = [f'{line["start"]};{line["text"]}' for line in transcript]
                f = open(filename, "w")
                print(filename, ': ', formatted_list, ' -> ', '\n'.join(formatted_list))
                f.write('\n'.join(formatted_list))
                f.close()
        except Exception as e:
            print(e, file=sys.stderr)
            f = open(filename, "w")
            print(filename, ': ', formatted_list, ' -> ', '\n'.join(formatted_list))
            f.write('\n'.join(formatted_list))
            f.close()

    def transcribe_videos(self, v_ids):
        print('vids: ' + str(v_ids))
        # import pdb
        # pdb.set_trace()
        for vid in v_ids:
            print(vid)
            self.transcribe_video(vid)

if __name__ == '__main__':
	scraper = YoutubeScraper()
	scraper.get_playlist(PLAYLIST_ID)