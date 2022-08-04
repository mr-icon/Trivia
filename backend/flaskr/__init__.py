import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app,resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,')
            return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id:category.type for category in categories}
        return jsonify({
                'success': True,
                'categories': formatted_categories,
                'total_category': len(formatted_categories)
        })


   
        @app.route('/questions')
        def retrieve_questions():
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                if len(current_questions) == 0:
                        abort(404)
                
                categories = Category.query.all()
                formatted_categories = {category.id:category.type for category in categories}

                return jsonify(
                {
                        'success': True,
                        'questions': current_questions,
                        'categories': formatted_categories,
                        'total_question': len(selection),
                }
                )


    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_questions(id):
        global question 

        i = 0
        deleted = False

        for question in questions:
                if question['id'] == id:
                        question.pop(i)
                        deleted = True

                i += 1 

        if deleted:
                return jsonify({
                        'success': True,
                        'deleted': question_id,
                        'total_questions': len(question.query.all())

                })


    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get['question', None]
        new_answer = body.get['answer', None]
        new_category = body.get['category', None]
        new_difficulty = body.get['difficulty', None]
        searchTerm = body.get['searchTerm', None]

        try:
                if searchTerm:
                        selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{searchTerm}%'))
                        current_questions = paginate_questions(request, selection)

                        return jsonify({
                                'success': True,
                                'questions': current_questions,
                                'total_questions': len(selection.all())
                        })
                else:
                        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                        question.insert()

                        selection = Question.query.order.order_by(Question.id).all()
                        current_questions = paginate_questions(request, selection)

                        return jsonify({
                                'success': True,
                                'create': question.id,
                                'questions': current_questions,
                                'total_questions': lens(Question.query.all())
                        })    
        except:
                abort(422) 


        @app.route('/categories/<int:category_id>/questions', methods=['GET'])
        def get_category(category_id):
                categories = Category.query.filter(Category.id == category_id).one_or_none()

                if categories is None:
                        abort(404)
                try:
                        selection = Question.query.filter(Question.category == category_id).all()
                        current_questions = paginate_questions(request, selection)

                        return jsonify({
                                'success': True,
                                'questions': current_questions,
                                'total_questions': lens(Question.query.all())
                        })
                except:
                   abort(422)       

        @app.route('/quizzes', methods=['POST'])
        def random_quizzes():

                data = request.get_json()
                category = data.get('category', None)
                previous_questions = data.get('previous_questions', None)

                try:
                        if category['id'] == 0:
                               question_list = Question.query.filter(Question.id.notin_(previous_questions)).all()
                        else:
                              question_list = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

                        formatted_questions = [question.format() for question in question_list] 
                        random_quizzes =  random.choice(formatted_questions)

                        return jsonify({
                                        'success': True,
                                        'questions': random_quizzes,
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

        @app.errorhandler(400)
        def unprocessable(error):
                 return jsonify({
                        'success': False,
                        'error': 400,
                        'message': 'Bad request'
                }), 400

        @app.errorhandler(405)
        def unprocessable(error):
                 return jsonify({
                        'success': False,
                        'error': 405,
                        'message': 'Method not allowed'
                }), 405

        @app.errorhandler(500)
        def unprocessable(error):
                 return jsonify({
                        'success': False,
                        'error': 500,
                        'message': 'Internal server error'
                }), 500
    return app

