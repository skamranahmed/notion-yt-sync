from unittest.mock import Mock, patch
import pytest

import requests

from api_client.notion import NotionClient, NotionAPIError

class TestNotionClient:
    @pytest.fixture
    def client(self):
        return NotionClient()
    
    @pytest.fixture
    def mock_post(self):
        with patch('requests.post') as mock:
            yield mock

    class TestFetchMostRecentPageFromDatabase:
        def test_fetch_most_recent_page_from_database_returns_non_200_status_code(self, client, mock_post):
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.raise_for_status.side_effect = requests.HTTPError()
            mock_post.return_value = mock_response
                
            exception_raised = False
            error_message = ""

            try:
                client.fetch_most_recent_page_from_database('database_id')
            except NotionAPIError as e:
                exception_raised = True
                error_message = str(e)

            assert exception_raised == True, "Expected NotionAPIError to be raised, but it was not raised"
            assert "notion api error #fetch_most_recent_page_from_database , got status code: 400" in error_message, "Expected error message did not match"

            assert mock_post.call_count == 1, "Expected mock_post to be called exactly once, but it was not called exactly once"

        def test_fetch_most_recent_page_from_database_returns_200_status_code(self, client, mock_post):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            exception_raised = False
            error_message = ""

            try:
                client.fetch_most_recent_page_from_database('database_id')
            except NotionAPIError as e:
                exception_raised = True
                error_message = str(e)

            assert exception_raised == False, "Expected NotionAPIError not to be raised, but it was raised"
            assert error_message == "", "Expected error message to be empty, but it was not empty"

            assert mock_post.call_count == 1, "Expected mock_post to be called exactly once, but it was not called exactly once"

        def test_fetch_most_recent_page_from_database_returns_200_status_code_but_with_empty_results(self, client, mock_post):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'object': 'list',
                'results': [],
                'next_cursor': None,
                'has_more': False,
                'type': 'page_or_database',
                'page_or_database': {},
                'request_id': '79701ac1-c6ff-4345-b4b0-c8c438258f19'
            }
            mock_post.return_value = mock_response

            exception_raised = False
            error_message = ""

            try:
                client.fetch_most_recent_page_from_database('database_id')
            except NotionAPIError as e:
                exception_raised = True
                error_message = str(e)

            assert exception_raised == False, "Expected NotionAPIError not to be raised, but it was raised"
            assert error_message == "", "Expected error message to be empty, but it was not empty"

            assert mock_post.call_count == 1, "Expected mock_post to be called exactly once, but it was not called exactly once"

        def test_fetch_most_recent_page_from_database_returns_200_status_code_with_non_empty_results(self, client, mock_post):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'object': 'list',
                'results': [{
                    'object': 'page',
                    'id': '104a0c22-0c52-816a-a606-db88c19e40af',
                    'created_time': '2024-09-17T18:13:00.000Z',
                    'last_edited_time': '2024-09-17T18:13:00.000Z',
                    'created_by': {'object': 'user', 'id': 'a3c09b4b-f1a0-4f0a-bb99-a7c7e739fe0d'},
                    'last_edited_by': {'object': 'user', 'id': 'a3c09b4b-f1a0-4f0a-bb99-a7c7e739fe0d'},
                    'cover': None,
                    'icon': None,
                    'parent': {'type': 'database_id', 'database_id': '9998849e-9ad0-4f53-9744-54da4772faac'},
                    'archived': False,
                    'in_trash': False,
                    'properties': {
                        'Record Creation Time': {'id': '%3Epj%3F', 'type': 'created_time', 'created_time': '2024-09-17T18:13:00.000Z'},
                        'Has been watched?': {'id': 'JWwd', 'type': 'checkbox', 'checkbox': False},
                        'Link': {'id': 'idU%7D', 'type': 'url', 'url': 'https://www.youtube.com/watch?v=JucD81ofaGY'},
                        'Video ID': {
                            'id': '%7Cy%3AN',
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {'content': 'JucD81ofaGY', 'link': None},
                                'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'},
                                'plain_text': 'JucD81ofaGY',
                                'href': None
                            }]
                        },
                        'Title': {
                            'id': 'title',
                            'type': 'title',
                            'title': [{
                                'type': 'text',
                                'text': {'content': 'MH370 - How One Person Destroyed 239 Lives', 'link': None},
                                'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'},
                                'plain_text': 'MH370 - How One Person Destroyed 239 Lives',
                                'href': None
                            }]
                        }
                    },
                    'url': 'https://www.notion.so/MH370-How-One-Person-Destroyed-239-Lives-104a0c220c52816aa606db88c19e40af',
                    'public_url': None
                }],
                'next_cursor': '104a0c22-0c52-81ae-beb0-fbb29c64a3b2',
                'has_more': True,
                'type': 'page_or_database',
                'page_or_database': {},
                'request_id': 'ecb1559f-9639-434a-aec3-d36c014bdba7'
            }
            mock_post.return_value = mock_response

            exception_raised = False
            error_message = ""

            try:
                client.fetch_most_recent_page_from_database('database_id')
            except NotionAPIError as e:
                exception_raised = True
                error_message = str(e)

            assert exception_raised == False, "Expected NotionAPIError not to be raised, but it was raised"
            assert error_message == "", "Expected error message to be empty, but it was not empty"

            assert mock_post.call_count == 1, "Expected mock_post to be called exactly once, but it was not called exactly once"