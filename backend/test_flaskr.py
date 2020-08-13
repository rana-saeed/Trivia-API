import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "Whose autobiography is entitled 'Catcher in the Rye'?",
            "answer": "J.D Salinger",
            "category": 2,
            "difficulty": 4
        }

        self.new_incomplete_question = {
            "question": "Whose autobiography is entitled 'Catcher in the Rye'?",
            "category": 2,
            "difficulty": 4
        }

        self.new_invalid_question = {
            "question": 22.66,
            "answer": "J.D Salinger",
            "category": 2,
            "difficulty": 4
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    GET '/categories' tests
    '''
    # Success: Get all categories from db
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        categories = Category.query.count()

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

        # Asserting db presistency
        self.assertEqual(data['total_categories'], categories)
       
    
    '''
    GET '/questions' tests
    '''
    # Success: Get all questions from db and paginate results (max 10 questions per page)
    def test_get_paginated_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        questions = Question.query.count()
        categories = Category.query.count()

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertLessEqual(data['total_questions'], 10)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

        # Asserting db presistency
        self.assertEqual(len(data['categories']), categories)

    # Error: Get questions from a page that doesn't exist
    def test_404_if_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Error: Get questions for a category that doesn't exist
    def test_400_if_invalid_category_get_all_questions(self):
        res = self.client().get('/questions?category=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    
    '''
    DELETE '/questions/<int:question_id>' tests
    '''
    # Success: Delete question by id
    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['questions'])
        self.assertLessEqual(data['total_questions'], 10)

        # Asserting db presistency
        self.assertEqual(question, None)

    # Error: Delete question that doesn't exist
    def test_404_if_delete_non_existing_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''
    POST '/questions' add question tests
    '''
    # Success: Add new question
    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == data['added']).one_or_none()

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['added'])
        self.assertTrue(data['questions'])
        self.assertLessEqual(data['total_questions'], 10)

        # Asserting db presistency
        self.assertNotEqual(question, None)

    # Error: Add question with missing paramters
    def test_400_if_missing_parameters_in_add_question(self):
        res = self.client().post('/questions', json=self.new_incomplete_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Error: Add question with invalid paramters
    def test_422_if_invalid_parameters_in_add_question(self):
        res = self.client().post('/questions', json=self.new_invalid_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    '''
    POST '/questions' search for question tests
    '''
    # Success: Search for string with results in database
    def test_search_for_questions(self):
        res = self.client().post('/questions', json={'search': 'the'})
        data = json.loads(res.data)

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['search_term'])
        self.assertGreater(len(data['questions']), 0)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    # Success: Search for string without results in database
    def test_search_for_questions_without_results(self):
        res = self.client().post('/questions', json={'search': 'dsfsdfdfdf'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['search_term'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], None)

    # Success: Search for string in specific category with results in database
    def test_search_for_questions(self):
        res = self.client().post('/questions', json={'search': 'the', 'current_category': 'Art'})
        data = json.loads(res.data)

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['search_term'])
        self.assertGreater(len(data['questions']), 0)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 2)


    '''
    POST '/quizzes' tests
    '''
    # Success: Quiz returns next question in all categories
    def test_next_question_in_quiz_all_categories(self):
        res = self.client().post('/quizzes', json={'questions_per_play': 5, 'previous_questions': [10, 12], 'quiz_category': {'id': 0, 'type': 'click'}})
        data = json.loads(res.data)

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotIn(data['question'], [10, 12])

    # Success: Quiz returns next question in specified category
    def test_next_question_in_quiz_specified_category(self):
        res = self.client().post('/quizzes', json={'questions_per_play': 5, 'previous_questions': [], 'quiz_category': {'id': 2, 'type': 'Art'}})
        data = json.loads(res.data)

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)

    # Success: Quiz returns next question in specified category with all questions already asked
    def test_next_question_in_quiz_specified_category_with_previous_questions(self):
        res = self.client().post('/quizzes', json={'questions_per_play': 5, 'previous_questions': [13, 14, 15], 'quiz_category': {'id': 3, 'type': 'Geography'}})
        data = json.loads(res.data)

        # Asserting response correctness
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)

    # Error: Quiz start with missing paramters
    def test_400_if_missing_parameters_in_quiz(self):
        res = self.client().post('/quizzes', json={'questions_per_play': 5, 'quiz_category': {'id': 2, 'type': 'Art'}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Error: Quiz start with invalid paramters
    def test_422_if_invalid_parameters_in_quiz(self):
        res = self.client().post('/quizzes', json={'questions_per_play': 'fff', 'previous_questions': ['ffs', 'sfs'], 'quiz_category': {'id': 2, 'type': 'Art'}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()