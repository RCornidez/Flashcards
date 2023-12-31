# flashcardController.py

from flask import request, jsonify, render_template, Blueprint, current_app
from pymongo.errors import BulkWriteError
from models.flashcardModel import Flashcard
import json 

flashcard_blueprint = Blueprint('flashcard', __name__)


# View Routes
# Serve landing page
@flashcard_blueprint.route('/', methods=['GET'])
def landing_page():
    return render_template('index.html')

# Serve the flashcards page
@flashcard_blueprint.route('/flashcards-review', methods=['GET'])
def flashcards_page():
    return render_template('flashcards.html')






# REST API Routes

# Create a single flashcard
@flashcard_blueprint.route('/flashcard', methods=['POST'])
def save_flash_card():
    data = request.json
    flashcard = Flashcard(data['title'], data['content'], data.get('tags'))
    collection = current_app.config['db']['flashcards'] 
    collection.insert_one(flashcard.to_dict())
    return "Flash card saved", 201


# Create a batch of flashcards
@flashcard_blueprint.route('/flashcards/batch', methods=['POST'])
def batch_save_flash_cards():
    try:
        uploaded_file = request.files['jsonFile']

        if uploaded_file and uploaded_file.filename != '':
            # Read the content of the uploaded JSON file
            json_data = uploaded_file.read()

            # Parse the JSON data
            try:
                cards = json.loads(json_data)
            except json.JSONDecodeError as e:
                return f"Error parsing JSON data: {str(e)}", 400

            # Process and store the JSON data in MongoDB
            flashcards = [Flashcard(card['title'], card['content'], card.get('tags')).to_dict() for card in cards]
            collection = current_app.config['db']['flashcards']
            collection.insert_many(flashcards)
            return "Batch of flash cards saved", 201
        else:
            return "No file uploaded", 400
    except BulkWriteError as e:
        # Handle the exception
        error_message = str(e)
        return f"Error saving batch of flash cards: {error_message}", 500  # Return an error response with status code 500


# Update a single flashcard
@flashcard_blueprint.route('/flashcard/<card_id>', methods=['PUT'])
def edit_flash_card(card_id):
    updated_data = request.json
    flashcard = Flashcard(updated_data['title'], updated_data['content'], updated_data.get('tags'))
    collection = current_app.config['db']['flashcards']
    collection.update_one({'_id': card_id}, {"$set": flashcard.to_dict()})
    return f"Flash card {card_id} updated", 200


# Delete a single flashcards
@flashcard_blueprint.route('/flashcard/<card_id>', methods=['DELETE'])
def delete_flash_card(card_id):
    collection = current_app.config['db']['flashcards']
    collection.delete_one({'_id': card_id})
    return f"Flash card {card_id} deleted", 200

# Delete all flashcards
@flashcard_blueprint.route('/flashcards/delete-all', methods=['DELETE'])
def delete_all_flashcards():
    collection = current_app.config['db']['flashcards']
    result = collection.delete_many({})
    return f"Deleted {result.deleted_count} flashcards", 200

# Get all flashcards
@flashcard_blueprint.route('/flashcards', methods=['GET'])
def get_all_flash_cards():
    collection = current_app.config['db']['flashcards']
    cards = list(collection.find())

    # Convert each document to a Flashcard object
    flashcards = [Flashcard(card['title'], card['content'], card.get('tags')).to_dict() for card in cards]
    return jsonify(flashcards)

# Get all flashcards by tag
@flashcard_blueprint.route('/flashcards/tags', methods=['GET'])
def get_flash_cards_by_tags():
    tags = request.args.getlist('tags')  # Assuming tags are passed as query parameters
    query = {'tags': {'$in': tags}}
    collection = current_app.config['db']['flashcards']
    cards = list(collection.find(query))
    
    # Convert each document to a Flashcard object and then to a dictionary
    flashcards = [Flashcard(card['title'], card['content'], card.get('tags')).to_dict() for card in cards]
    return jsonify(flashcards)