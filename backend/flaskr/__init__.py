from crypt import methods
import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, selection):
    'pagination helper function'
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    '''create and configure the app'''
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories')
    def get_categories():
        '''retrieve all categories'''
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in selection}
        if len(categories) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'categories': categories
        })

    @app.route('/questions')
    def retrieve_questions():
        '''retrieve all questions'''
        selection = Question.query.order_by(Question.id).all()
        questions = pagination(request, selection)
        categories = Category.query.order_by(Category.id).all()
        if len(questions) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'categories': {
            category.id: category.type for category in categories
            },
          'questions': questions,
          'total_questions': len(selection),
          'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''delete a question using its id'''
        try:
            question = Question.query.filter(
              Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
              'success': True,
              'deleted': question.id
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(422)
        question = body.get("question")
        answer = body.get("answer")
        difficulty = body.get("difficulty")
        category = body.get("category")

        try:
            new_question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)
            new_question.insert()
            return jsonify({
              'success': True,
              'created': new_question.id
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        if search_term:
            search_questions = Question.query.filter(
              Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
              'success': True,
              'questions': [
                question.format() for question in search_questions
                ],
              'total_questions': len(search_questions),
              'current_category': None
            })
        abort(404)

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):
        try:
            questions = Question.query.filter(Question.category == id).all()
            return jsonify({
              'success': True,
              'questions': [
                question.format() for question in questions
              ],
              'total_questions': len(questions),
              'current_category': id
            })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        try:
            body = request.get_json()
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                      Question.id.notin_((previous_questions))).all()
            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(
                  available_questions) > 0 else None
            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

    # '''
    # @TODO: 
    # Create error handlers for all expected errors 
    # including 404 and 422. 
    # '''
    return app
