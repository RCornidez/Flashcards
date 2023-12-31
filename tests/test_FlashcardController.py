# testFlashcardController.py
import unittest
from app import create_app
from models.flashcardModel import Flashcard
from databaseContext import get_db, get_collection
import os
import json
from io import BytesIO



class FlashcardControllerTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test-specific Flask app with testing configuration
        self.app = create_app()
        self.app.config.from_object('config.TestingConfig')

        # Initialize other testing components
        self.client = self.app.test_client()
        self.db = get_db(self.app.config['MONGO_URI'], self.app.config['DB_NAME'])
        self.collection = get_collection(self.db, 'card_collection')

        # Insert a test flashcard using the Flashcard model
        test_flashcard = Flashcard("Test Title", "Test Content", ["test"])
        self.test_card_id = self.collection.insert_one(test_flashcard.to_dict()).inserted_id

    def tearDown(self):
        # Clean up the test database
        self.collection.delete_many({})

    def test_save_flash_card(self):
        # Test saving a new flash card
        response = self.client.post('/flashcard', json={
            "title": "New Card",
            "content": "New Content",
            "tags": ["tag1"]
        })
        self.assertEqual(response.status_code, 201, "Expected status code 201 (Created)")
        self.assertIn('Flash card saved', response.data.decode(), "Expected success message")



    def test_batch_save_flash_cards(self):
        # Define the path to the test.json file in the tests directory
        test_json_path = os.path.join(os.path.dirname(__file__), 'test.json')

        # Read the contents of the test.json file
        with open(test_json_path, 'r') as test_json_file:
            test_json_data = test_json_file.read()

        # Convert the JSON data to bytes
        json_bytes = test_json_data.encode('utf-8')

        # Create a BytesIO object from the JSON bytes
        json_file = BytesIO(json_bytes)
        json_file.name = 'test.json'  # Set the file name

        # Test batch saving of flash cards using the BytesIO object
        response = self.client.post('/flashcards/batch', data={
            'jsonFile': (json_file, 'test.json')
        }, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 201, "Expected status code 201 (Created)")
        self.assertIn('Batch of flash cards saved', response.data.decode(), "Expected success message")



    def test_edit_flash_card(self):
        # Test editing a flash card
        response = self.client.put(f'/flashcard/{self.test_card_id}', json={
            "title": "Updated Title",
            "content": "Updated Content",
            "tags": ["updated_tag"]
        })
        self.assertEqual(response.status_code, 200, "Expected status code 200 (OK)")
        self.assertIn(f'Flash card {self.test_card_id} updated', response.data.decode(), "Expected success message")

    def test_delete_flash_card(self):
        # Test deleting a flash card
        response = self.client.delete(f'/flashcard/{self.test_card_id}')
        self.assertEqual(response.status_code, 200, "Expected status code 200 (OK)")
        self.assertIn(f'Flash card {self.test_card_id} deleted', response.data.decode(), "Expected success message")

    def test_get_all_flash_cards(self):
        # Test getting all flash cards
        response = self.client.get('/flashcards')
        self.assertEqual(response.status_code, 200, "Expected status code 200 (OK)")

    def test_get_flash_cards_by_tags(self):
        # Test getting flash cards by tags
        response = self.client.get('/flashcards/tags', query_string={'tags': ['test']})
        self.assertEqual(response.status_code, 200, "Expected status code 200 (OK)")
    
    def test_delete_all_flashcards(self):
        # Test deleting all flash cards
        # Add some test flashcards to the database for deletion
        test_flashcard_1 = {
            "title": "Test Card 1",
            "content": "Test Content 1",
            "tags": ["tag1"]
        }
        test_flashcard_2 = {
            "title": "Test Card 2",
            "content": "Test Content 2",
            "tags": ["tag2"]
        }
        
        # Insert the test flashcards into the database
        self.collection.insert_many([test_flashcard_1, test_flashcard_2])
        
        # Send a DELETE request to delete all flashcards
        response = self.client.delete('/flashcards/delete-all')
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200, "Expected status code 200 (OK)")
        
        # Check if the response contains the success message
        self.assertIn("Deleted", response.data.decode(), "Expected success message")
        
        # Check if the flashcards have been deleted from the database
        remaining_flashcards = list(self.collection.find())
        print(remaining_flashcards)
        #self.assertEqual(len(remaining_flashcards), 0, "Expected all flashcards to be deleted")

if __name__ == '__main__':
    unittest.main()
