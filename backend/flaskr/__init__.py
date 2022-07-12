import os
from flask import Flask, request, abort, jsonify, render_template
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

    @app.route('/', methods=['POST', 'GET'])
    def get_categories():
        if request.method == 'GET':
           page = request.args.get('categories', all, type=str)
           Catergory = categories.query.all()
        return jsonify({
                'success': True,
                'Category': question_categories,
                'questions': current_questions,
        })


   
    @app.route('/questions', methods=['GET'])
    def get_question():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        question = questions.query.all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
                'success':True,
                'Questions': formatted_question[start:end]
        })


    @app.route('/questions/<int:id>', methods=['DELETE'])
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

                        
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_answer = body.get['answer', None]
        new_category = body.get['category', None]
        new_difficulty = body.get['difficulty', None]

        try:
                question = questions(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = questions.query.order.order_by(questions.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                        'success': True,
                        'create': question_id,
                        'questions': current_questions,
                        'total_questions': lens(Question.query.all())
                })    
        except:
                abort(422) 


        @app.route('/questions/<str:question_category>', methods=['GET'])
        def get_question(questions_category):
                 try:
                        question = questions.query.filter(questions.category == questions_category)

                        question = request.args.get(questions.category, type=str)
                        question = Question.query.all()
                        formatted_questions = [Question.format() for category in questions]

                        return jsonify({
                                'success': True,
                                'questions': formatted_questions,
                                'total_questions': lens(Question.query.all())
                        })
                 except:
                   abort(422)

        @app.route('/questions/<str:question_category>', methods=['POST'])
        def get_question(quesstions_category):
                try:
                        question = questions.query.filter(questions.category == questions_category)

                        question = request.args.get(questions.category, 1, type=str)
                        start = (questions - 1)
                        end = start + 1
                        questions = questions.query.order_by(questions.category).all()
                        formatted_questions = [questions.format() for category in questions]

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

