# Flash Cards

Flash Cards is a feature-rich web application built on the Model-View-Controller (MVC) architecture using Flask, a popular Python web framework. It serves as a versatile tool for creating, managing, and reviewing flashcards, making it ideal for students, educators, and anyone looking to enhance their learning experience. With unit testing using Python's unittest and a RESTful API, it offers a robust and extensible platform for effective flashcard management.

<hr/>

This project utilizes a makefile for simple actions:

<h3>Makefile Commands:</h3>

    Action : Command
    ----------------
    install dependencies: make install
    testing: make test
    running in development environment: make development
    running in production environment: make production

<hr/>

<h3>How-to-run</h3>

1. Download and start MongoDB Community Edition for your system from the official [MongoDB Instructions](https://www.mongodb.com/docs/manual/installation/). You can use the default IP and Port settings. If they're adjusted you will need to match these settings within config.py.

2. Download this repository.

3. Within the root of the repository, run:

```
make install
```

4. Run the application.

```
make development
```

5. Access the application [http://localhost:5000/](http://localhost:5000/) and upload the flashcards in json format.

6. Review the uploaded flashcards [http://localhost:5000/flashcards-review](http://localhost:5000/flashcards-review)

<hr/>


View Routes:

    Route: /
    Method: GET
    Description: Serves the landing page.
    Flashcards Page

    Route: /flashcards-review
    Method: GET
    Description: Serves the flashcards review page.


API Endpoints:

    Route: /flashcard
    Method: POST
    Description: Creates a single flashcard with provided data.

    Route: /flashcards/batch
    Method: POST
    Description: Creates a batch of flashcards from an uploaded JSON file.

    Route: /flashcard/<card_id>
    Method: PUT
    Description: Updates a single flashcard by its ID.

    Route: /flashcard/<card_id>
    Method: DELETE
    Description: Deletes a single flashcard by its ID.

    Route: /flashcards/delete-all
    Method: DELETE
    Description: Deletes all flashcards.

    Route: /flashcards
    Method: GET
    Description: Retrieves all flashcards.

    Route: /flashcards/tags
    Method: GET
    Description: Retrieves flashcards filtered by tags.

<hr/>

### Changelog

#### Version 0.0.1 (2023-12-30)

- Added unit testing using Python's `unittest` framework.
- Built a RESTful API.
- Created a simple HTML view that allows for upload of JSON file and viewing/rotating through flashcards.

<hr/>

### Planned Implementations

- Redesign views: Update the views to have better aesthetics
- Setup Creating functionality: Add a form to create new flashcards.
- Setup Managing functionality: Add a form and button to adjust existing flashcard data.
- Download functionality: Create functionality to download existing database as json file.

<hr/>



