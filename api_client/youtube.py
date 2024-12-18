import scrapetube

class YoutubeClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YoutubeClient, cls).__new__(cls)
        return cls._instance
    
    def fetch_channel_videos(self, channel_url: str):
        videos = scrapetube.get_channel(channel_url=channel_url, sort_by='newest')
        has_videos = False
        for video in videos:
            has_videos = True
            video_id = video['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_title = video['title']['runs'][0]['text']
            yield {
                "id": video_id,
                "url": video_url,
                "title": video_title
            }
        if not has_videos:
            yield None