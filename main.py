from config import get_config
from api_client.notion import NotionClient
from api_client.youtube import YoutubeClient
from typing import List, Dict
import logging

def process_channel(notion_client: NotionClient, youtube_client: YoutubeClient, channel_config: Dict) -> int:
    channel_name = channel_config['name']
    logging.info(f"Started fetching videos for the channel name: {channel_name}")
    
    most_recent_page = notion_client.fetch_most_recent_page_from_database(channel_config['notion_database_id'])
    latest_video_id = notion_client.extract_video_id_from_page(most_recent_page)

    channel_videos_sorted_by_latest_first = youtube_client.fetch_channel_videos(channel_config['channel_url'])

    new_videos_to_be_inserted_in_notion: List[Dict] = []

    for video in channel_videos_sorted_by_latest_first:
        if latest_video_id == video['id']:
            logging.info(
                f'Stopped fetching videos for the channel name: {channel_name}, '
                f'since we already have `{latest_video_id}` '
                'as the latest Video ID stored in Notion'
            )
            break
        else:
            logging.info(f"Got new video with title: `{video['title']}` to be inserted in Notion, for the channel name: {channel_name}")
            # inserting every video at the first index, so that the latest video is at the last index
            # hence, when iterating through this list and creating the page record in notion
            # the record for the latest video will be created at last, hence it will have the latest created_at time
            new_videos_to_be_inserted_in_notion.insert(0, video)

    logging.info(f"Got {len(new_videos_to_be_inserted_in_notion)} new videos to be inserted in Notion for the channel name: {channel_name}")
    
    for video in new_videos_to_be_inserted_in_notion:
        notion_client.create_page_in_database(
            database_id = channel_config['notion_database_id'],
            video_title = video['title'],
            video_link = video['url'],
            video_id = video['id']
        )
        logging.info(f"Inserted video title: `{video['title']}` in the database of channel name: {channel_name}")
    
    return len(new_videos_to_be_inserted_in_notion)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
    config = get_config()

    notion_client = NotionClient()
    youtube_client = YoutubeClient()

    for channel_config in config.YOUTUBE_CHANNELS_CONFIG_JSON:
        total_videos_inserted = process_channel(notion_client, youtube_client, channel_config)
        logging.info(f"Total new videos inserted for the channel name: {channel_config['name']} is {total_videos_inserted}")
        
if __name__ == "__main__":
    main()