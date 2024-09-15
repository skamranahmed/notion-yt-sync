import scrapetube

class YoutubeClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YoutubeClient, cls).__new__(cls)
        return cls._instance
    
    def fetch_channel_videos(self, channel_url: str):
        video_data_list = []
        videos = scrapetube.get_channel(channel_url=channel_url, sort_by='newest')
        for video in videos:
            video_id = video['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_title = video['title']['runs'][0]['text']
            video_data_list.append({
                "id": video_id,
                "url": video_url,
                "title": video_title
            })
        return video_data_list