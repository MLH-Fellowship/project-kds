import unittest
from peewee import *

from app import TimelinePost, get_time_line_post

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        
        # Close connection to db.
        test_db.close()
        
    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe',
email='john@example.com', content='Hello World, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe',
email='jane@example.com', content='Hello World, I\'m Jane!')
        assert second_post.id == 2
        
        # Get timeline posts and assert that they are correct
        all_posts = get_time_line_post()
        for post in all_posts:
            assert all_posts[post][0]['id'] == 2
            assert all_posts[post][1]['id'] == 1