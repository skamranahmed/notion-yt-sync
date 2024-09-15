from config import get_config
import requests

class NotionClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotionClient, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance

    def _configure(self):
        config = get_config()
        self._REQUEST_HEADERS = {
            "Authorization": f"Bearer {config.NOTION_INTERNAL_INTEGRATION_SECRET}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self._BASE_URL = config.NOTION_API_BASE_URL
        self._DATABASE_COLUMN_NAMES_MAP = {
            # keys are for code reference for ease of use, values are actual column names in the Notion database
            "TITLE": "Title",
            "LINK": "Link",
            "HAS_BEEN_WATCHED": "Has been watched?",
            "RECORD_CREATION_TIME": "Record Creation Time",
            "VIDEO_ID": "Video ID",
        }
    
    def fetch_most_recent_page_from_database(self, database_id: str):
        """
            Fetches the most recent page (entry/record) from the Notion database.
            In Notion terminology, each entry in the database is referred to as a page.
        """
        query_database_endpoint = f"{self._BASE_URL}/databases/{database_id}/query"
        payload = {
            "sorts": [
                {
                    "property": self._DATABASE_COLUMN_NAMES_MAP['RECORD_CREATION_TIME'],
                    "direction": "descending"
                }
            ],
            "page_size": 1
        }
        response = requests.post(
            url = query_database_endpoint,
            headers = self._REQUEST_HEADERS, 
            json = payload
        )
        return response.json()
    
    def extract_video_id_from_page(self, page_json):
        video_id_column_name = self._DATABASE_COLUMN_NAMES_MAP['VIDEO_ID']
        video_id_column = page_json['results'][0]['properties'][video_id_column_name]
        content = video_id_column['rich_text'][0]['text']['content']
        return content

    def create_page_in_database(self, database_id: str, video_title: str, video_link: str, video_id: str):
        """
            Creates a new page (entry/record) in the Notion database.
            In Notion terminology, each entry in the database is referred to as a page.
        """
        create_page_endpoint = f"{self._BASE_URL}/pages"
        payload = {
            "parent": { "database_id": database_id },
            "properties": {
                self._DATABASE_COLUMN_NAMES_MAP["TITLE"]: {
                    "title": [
                        {
                            "text": {
                                "content": video_title
                            }
                        }
                    ]
                },
                self._DATABASE_COLUMN_NAMES_MAP["LINK"]: {
                    "url": video_link
                },
                self._DATABASE_COLUMN_NAMES_MAP["HAS_BEEN_WATCHED"]: {
                    "checkbox": False
                },
                self._DATABASE_COLUMN_NAMES_MAP["VIDEO_ID"]: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": video_id
                            }
                        }
                    ]
                }
            }
        }
        response = requests.post(
            url = create_page_endpoint,
            headers = self._REQUEST_HEADERS, 
            json = payload
        )
        return response.json()
