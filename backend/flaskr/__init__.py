import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # cors = CORS(app, resources={r"/api/*": {"origins"}})

    @app.after_request
    def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,')
            return response

    @app.route('/categories', method=['GET'])
    def get_categories():
        page = request.args.get('page', 1, type=int)
        categories = Categories.query.all()
        formatted_categories = [Category.format() for category in categories]

        return jsonify({
                'success':True,
                'categories': formatted_categories,
        })
   
    @app.route('/questions', method=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        question = Questions.query.all()
        formatted_question = [Question.format() for question in questions]

        return jsonify({
                'success':True,
                'questions': formatted_questions[start:end]
        })


    @app.route('/questions/<int:id>', method=['DELETE'])
    def delete_question(id):
        global questions 

        i = 0
        deleted = False

        for question in questions:
                if question['id'] == id:
                        questions.pop(i)
                        deleted = True

                i += 1 

        if deleted:
                return jsonify({
                        'success': True,
                        'deleted': question_id,
                        'questions': current_questions,

                })

                        
    @app.route('/questions', method=['POST'])
    def create_questions():
        body = request.get_json()
        new_answer = body.get['answer', None]
        new_category = body.get['category', None]
        new_difficulty = body.get['difficulty', None]

        try:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                        'success': True,
                        'create': question_id,
                        'questions': current_questions,
                        'total_questions': lens(Question.query.all())
                })    
        except:
                abort(422) 


        @app.route('/questions/<str:question_category>', method=['GET'])
        def get_questions(question_category):
                 try:
                        question = Question.query.filter(Question.category == question_category)

                        question = request.args.get(Question.category, type=str)
                        question = Question.query.all()
                        formatted_questions = [Question.format() for category in questions]

                        return jsonify({
                                'success': True,
                                'questions': formatted_questions,
                                'total_questions': lens(Question.query.all())
                        })
                 except:
                   abort(422)

        @app.route('/questions/<str:question_category>', method=['POST'])
        def get_questions(quesstion_category):
                try:
                        question = Question.query.filter(Question.category == question_category)

                        question = request.args.get(Question.category, 1, type=str)
                        start = (question - 1)
                        end = start + 1
                        questions = Question.query.order_by(Question.category).all()
                        formattd_questions = [Question.format() for category in questions]

                        return jsonify({
                                        'success': True,
                                        'questions': formatted_questions[start:end],
                                        'total_questions': lens(Question.query.all())
                        })    
                except:
                        abort(422) 

        @app.errorhandler(404)
        def not_found(error):
                return jsonify({
                        'success': False,
                        'error': 404,
                        'message': 'Not Found'
                }), 404

        @app.errorhandler(422)
        def unprocessable(error):
                 return jsonify({
                        'success': False,
                        'error': 422,
                        'message': 'Unprocessable'
                }), 422

    return app

