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
    CORS(app)

    @app.after_request
    def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,')
            return response

    @app.route('/categories', methods=['POST', 'GET'])
    def get_categories():
        if request.method == 'GET':
           page = request.args.get('categories', 1, type=int)
           categories = Category.query.all()
        return jsonify({
                'success': True,
                'categories': Question_category,
        })


   
        @app.route("/questions")
        def retrieve_questions():
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_Question(request, selection)

                if len(current_questions) == 0:
                        abort(404)

                return jsonify(
                {
                        "success": True,
                        "questions": current_questions,
                        "total_question": len(Question.query.all()),
                }
                )


    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        global Question 

        i = 0
        deleted = False

        for question in Question:
                if Question['id'] == id:
                        Question.pop(i)
                        deleted = True

                i += 1 

        if deleted:
                return jsonify({
                        'success': True,
                        'deleted': Question_id,
                        'questions': current_questions,

                })

                        
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get['question', None]
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
                        'create': question,
                        'questions': current_questions,
                        'total_questions': lens(Question.query.all())
                })    
        except:
                abort(422) 


        @app.route('/questions/<str:question_category>', methods=['GET'])
        def get_question(Question_category):
                 try:
                        question = Question.query.filter(Question.category == Question_category)

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

        @app.route('/questions/<str:question_category>', methods=['POST'])
        def get_question(Question_category):
                try:
                        question = Question.query.filter(Question.category == Question_category)

                        question = request.args.get(Question.category, 1, type=str)
                        start = (Question - 1)
                        end = start + 1
                        questions = Question.query.order_by(Question.category).all()
                        formatted_questions = [Question.format() for category in Question]

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

