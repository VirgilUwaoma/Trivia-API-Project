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

    # def test_get_categories(self):
    #     '''test getting all categories'''
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['categories'])
    #     self.assertEqual(len(data['categories']), Category.query.count())

    # def test_get_paginated_questions(self):
    #     '''tests getting questions'''
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['categories']))

    # def test_delete_question(self):
    #     '''test  deleting question by id'''
    #     question_id = 5
    #     res = self.client().delete(f'/questions/{question_id}')
    #     data = json.loads(res.data)
    #     question = Question.query.filter(
    #         Question.id == question_id).one_or_none()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], question_id)
    #     self.assertEqual(question, None)

    # def test_create_question(self):
    #     '''tests adding a new question'''
    #     new_question = {
    #         "question": 'question',
    #         "answer": 'answer',
    #         "difficulty": 5,
    #         "category": 5
    #     }
    #     total_questions_before = Question.query.count()
    #     res = self.client().post('/questions', json=new_question)
    #     data = json.loads(res.data)
    #     total_questions = Question.query.count()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(total_questions, total_questions_before + 1)

    # def test_search_question(self):
    #     '''tests question searching'''
    #     search_term = {"searchTerm": 'what'}
    #     res = self.client().post('/questions/search', json=search_term)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(
    #         data['total_questions'],
    #         Question.query.filter(Question.question.ilike(
    #             f'%{search_term["searchTerm"]}%')).count()
    #         )
    #     self.assertTrue(data["questions"])

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
