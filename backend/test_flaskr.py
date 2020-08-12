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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
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

    
    # Success: Delete question by id
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 2).one_or_none()
    #     print(question)

    #     # Asserting response correctness
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['questions'])
    #     self.assertLessEqual(data['total_questions'], 10)

        # Asserting db presistency
        # self.assertEqual(question, None)

    # Error: Delete question that doesn't exist
    def test_404_if_delete_non_existing_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Success: Add new question
    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        print(data)

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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()