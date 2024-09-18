from unittest.mock import Mock, patch
import pytest

from api_client.youtube import YoutubeClient

class TestYoutubeClient:
    @pytest.fixture
    def client(self):
        return YoutubeClient()
    
    @pytest.fixture
    def mock_get_channel(self):
        with patch('api_client.youtube.scrapetube.get_channel') as mock:
            yield mock

    class TestFetchChannelVideos:
        def test_fetch_channel_videos_returns_videos(self, client, mock_get_channel):
            mock_get_channel.return_value = iter([
                {
                    'videoId': '1234',
                    'title': {'runs': [{'text': 'video-title-1'}]},
                },
                {
                    'videoId': '5678',
                    'title': {'runs': [{'text': 'video-title-2'}]},
                },
            ])

            videos_list = list(client.fetch_channel_videos('https://www.youtube.com/c/ChannelName'))

            assert len(videos_list) == 2

            assert videos_list[0] == {
                'id': '1234',
                'url': 'https://www.youtube.com/watch?v=1234',
                'title': 'video-title-1'
            }

            assert videos_list[1] == {
                'id': '5678',
                'url': 'https://www.youtube.com/watch?v=5678',
                'title': 'video-title-2'
            }

            assert mock_get_channel.call_count == 1, "Expected mock_get_channel to be called exactly once, but it was not called exactly once"

        def test_fetch_channel_videos_returns_none_when_no_videos_are_found_in_channel(self, client, mock_get_channel):
            mock_get_channel.return_value = iter([])

            videos_generator = client.fetch_channel_videos('https://www.youtube.com/c/ChannelName')

            assert next(videos_generator) is None, "Expected None when no videos are found"

            assert mock_get_channel.call_count == 1, "Expected mock_get_channel to be called exactly once, but it was not called exactly once"

        
    
