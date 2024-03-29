# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
## Endpoints
GET '/categories'

GET '/questions'

DELETE '/questions/<int:question_id>'

POST '/questions'

POST '/quizzes'

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: 
    1. An object with a single key, `categories`, that contains a object of id: category_string key:value pairs. 
    2. A boolean `success`, indicating if categoris retrieval from database was successful or not.
    3. An int `total_categories`, indicating total number of categories found.
    4. A status code of `200` in case of success or `404` in case no categories found.

- Sample Response:
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "success": true, 
  "total_categories": 2
}
```

#### GET '/questions'
- Fetches a dictionary of questions in which the keys are the ids and the value is the remaining attributes of questions object uncluding: question, answer, diffuclty, category
- Request Arguments:
    1. `(Optional)`Category: id of category to get questions under it.
    2. `(Optional)`Page: number of page to view questions on.
- Returns: 
    1. An object with a single key, `questions`, that contains an array of object question of id, question, answer, diffuclty and category.
    2. An object with a single key, `categories`, that contains a object of id: category_string key:value pairs. 
    3. A boolean `success`, indicating if questions retrieval from database was successful or not.
    4. A string `current_category`, indicating type of category we are currently displaying questions for. Value will be `null` in case no category specified.
    5. An int `total_questions`, indicating total number of questions per current page.
    
    6. A status code of `200` in case of success or `404` in case no questions or page found or `400` in case of invalid request (e.g. invalid category id).

- Sample Response:
```
{ 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ]
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "success": true,
  "current_category": "Art",
  "total_questions": 2
}
```

#### DELETE '/questions/<int:question_id>'
- Deletes a question from the database based on specified `question_id` in URL.
- Request Arguments: None
- Returns: 
    1. An int `deleted`, indicating the id of the question deleted.
    2. An object with a single key, `questions`, that contains an array of object question of id, question, answer, diffuclty and category.
    3. A boolean `success`, indicating if categoris retrieval from database was successful or not.
    4. An int `total_questions`, indicating total number of questions remaining.
    5. A status code of `200` in case of success or `404` in case no question found or `500` in case of internal database operation error.

- Sample Response:
```
{
  "deleted": 5,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    .
    .
    .
    .
    .
    .
  ],
  "success": true,
  "total_questions": 10
}
```

#### POST '/questions'
- Adds a question to the database based on attached JSON body.
- Request Arguments: None
- Request Body: JSON of question object
  ```
  {
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
    "answer": "Maya Angelou",
    "category": 2,
    "difficulty": 4
  }
  ```
- Returns: 
    1. An int `added`, indicating the id of the question added.
    2. An object with a single key, `questions`, that contains an array of object question of id, question, answer, diffuclty and category.
    3. A boolean `success`, indicating if categoris retrieval from database was successful or not.
    4. An int `total_questions`, indicating total number of questions remaining.
    5. A status code of `200` in case of success or `400` in case no missing parameters in body or `422` in case of invalid request body.

- Sample Response:
```
{
  "added": 4,
  "questions": [
    .
    .
    .
    .
    .
    .,
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 10
}
```

#### POST '/questions'
- The second version of this endpoint searches for a specfied string in questions.
- Request Arguments: None
- Request Body: JSON of search term and current category if specified
  ```
  {
    "search": "Whose",
    "current_category": "Art"
  }
  ```
- Returns: 
    1. A string `search_term`, indicating the value searched for.
    2. An object with a single key, `questions`, indicating all found questions that partially or fully match the search term.
    3. A boolean `success`, indicating if search operation was successful or not.
    4. An int `total_questions`, indicating total number of search results found.
    5. An int `current_category`, indicating id of category we are currently displaying results for. Value will be `null` in case no category specified.
    6. A status code of `200` in case of success or `500` in case of internal database operation error.

- Sample Response:
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 2,
      "difficulty": 4,
      "id": 25,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "search_term": "Whose",
  "success": true,
  "total_questions": 1,
  "current_category": null
}
```

#### POST '/quizzes'
- Retreives next random question that was not previously asked in games session for a specific or for all categoris to play trivia game.
- Request Arguments: None
- Request Body: JSON of quiz category object, list of previously asked questions in game session and `Optiona` number of questions per quiz.s
  ```
  {
    "questions_per_play": 5,
    "previous_questions": [19],
    "quiz_category": {"id": 2, "type": "Art"}
  }
  ```
  ###### NOTE
  For all categories use:
  ```
  "quiz_category": {"id": 0, "type": "click"}
  ```
- Returns: 
    1. An object with a single key, `questions`, indicating next question to be asked in game session.s
    2. A boolean `success`, indicating if retrieving next question was successful or not.
    3. A status code of `200` in case of success or `400` in case no missing parameters in body or `422` in case of invalid request body.

- Sample Response:
```
{
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```