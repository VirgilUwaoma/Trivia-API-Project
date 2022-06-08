'''testing endpoints'''
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
        self.database_path = "postgresql://{}/{}".format(
                             'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        '''test getting all categories'''
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), Category.query.count())

    def test_404_error_sent_bad_category_request(self):
        '''test bad categories request'''
        res = self.client().get('/categories/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_questions(self):
        '''tests getting questions'''
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_error_requesting_invalid_questions_page(self):
        '''test bad question page request'''
        res = self.client().get('/questions?page=300')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        '''test  deleting question by id'''
        question_id = 9
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_422_error_deleting_non_existing_question(self):
        '''test error deleting non existing question by id'''
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        '''tests adding a new question'''
        new_question = {
            "question": 'question',
            "answer": 'answer',
            "difficulty": 5,
            "category": 5
        }
        total_questions_before = Question.query.count()
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions = Question.query.count()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions, total_questions_before + 1)

    def test_422_error_create_question(self):
        '''tests 422 error adding a new question'''
        new_question = {
            'question': 'new_question',
            'answer': 'new_answer',
            'category': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_question(self):
        '''tests question searching'''
        search_term = {"searchTerm": 'what'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(
            data['total_questions'],
            Question.query.filter(Question.question.ilike(
                f'%{search_term["searchTerm"]}%')).count()
            )
        self.assertTrue(data["questions"])

    def test_404_error_search_questions(self):
        '''tests bad search request'''
        new_search = {
            'searchTerm': '',
        }
        res = self.client().post('/questions/search', json=new_search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_by_categories(self):
        '''tests getting all question by categories'''
        category_id = 3
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(
            data['total_questions'],
            Question.query.filter(Question.category == category_id).count()
            )
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])

    def test_404_error_get_questions_by_category(self):
        '''tests error getting all question by categories'''
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_the_quiz(self):
        '''tests playing the quiz'''
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {'type': 'Entertainment', 'id': 5}
            }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_error_play_the_quiz(self):
        '''tests 404 error playing the quiz'''
        new_quiz = {'quiz_category': {'type': 'Entertainment', 'id': 5}}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
