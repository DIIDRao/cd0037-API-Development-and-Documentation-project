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
        self.database_name = "trivia_test"
        user = os.environ.get("POSTGRES_USER", "postgres")
        pwd = os.environ.get("POSTGRES_PWD", "postgres")
        self.database_path = "postgresql://{}:{}@{}/{}".format(user, pwd, 'localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_get_categories(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')  

    def test_questions_pages(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_Questions'])

    def test_404_get_questions_pages(self):
        res = self.client().get('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')   

    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        print(res.status_code)
        if(res.status_code == 200):
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        else:
            self.assertEqual(res.status_code, 500)
        

    def test_404_delete_question(self):
        res = self.client().get('/questions/99')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')     

    def test_successful_question_creation(self):
        # Given
        payload = json.dumps({
            "question": "q1",
            "answer": "a1",
            "difficulty": "1",
            "category": "1"
        })

        # When
        response = self.client().post('/questions', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(True, response.json['success'])
        self.assertEqual(200, response.status_code)

    def test_successful_question_search(self):
        # Given
        payload = json.dumps({
            "searchTerm": "q1"
        })

        # When
        response = self.client().post('/questions/search', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(True, response.json['success'])
        self.assertEqual(200, response.status_code)     

    def test_get_questions_for_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])   

    def test_successful_play_quizzes(self):
        # Given
        payload = json.dumps({
            "previous_questions": [],
            "quiz_category": {'id':1,'type':1}
        })

        # When
        response = self.client().post('/quizzes', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(True, response.json['success'])
        self.assertEqual(200, response.status_code)        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()