#from crypt import methods
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

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

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*" : {"origins": '*'}})
    #CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories_list = {}
            for category in categories:
                id = category.id
                value = category.type
                categories_list[id] = value

            return jsonify(
                {
                    #"success": True,
                    "categories": categories_list,
                }
            )
        except:
            abort(500)

    @app.route('/questions', methods=['GET', 'POST'])
    def questions():
        if request.method == 'GET':
            questions = Question.query.all()
            random.shuffle(questions)
            current_questions =  paginate_questions(request, questions)
            categories = Category.query.order_by(Category.id).all()
            categories_list = {}
            for category in categories:
                id = category.id
                value = category.type
                categories_list[id] = value

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "questions": current_questions,
                    "totalQuestions": len(Question.query.all()),
                    "currentCategory": "History",
                    "categories": categories_list
                }
            )

        #else:
        if request.method == 'POST':
            body = request.get_json()

            new_question = body.get("question")
            new_answer = body.get("answer")
            new_category = body.get("category")
            new_difficulty = body.get("difficulty")

            search = body.get("searchTerm", None)

            try:
                if search:
                    selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search))
                    )
                    current_questions = paginate_questions(request, selection)

                    return jsonify(
                        {
                            "currentCategory": "History",
                            "questions": current_questions,
                            "totalQuestions": len(selection.all()),
                        }
                    )

                else:
                    question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                    question.insert()

                    return jsonify(
                        {
                            "success": True,
                            "created": question.id
                        }
                    )

            except:
                abort(422)
            
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:    
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": id,
                }
            )

        except:
            abort(422)

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        try:
            selection = Question.query.filter(Question.category == id).all()
            current_questions = paginate_questions(request, selection)
            category = Category.query.filter(Category.id == id).first()

            return jsonify(
                {
                    "currentCategory": category.type,
                    "questions": current_questions,
                    #"totalQuestions": len(selection),
                    "totalQuestions": len(selection)
                }
            )
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        #print(body)
        quiz_category = body.get('quiz_category')
        previous_question = body.get('previous_questions')
        
        try:
            category = quiz_category['id']
            next_question = None
            
            if category != 0:
                selection = Question.query.filter(
                    db.and_(
                    Question.category == category,
                    Question.id.not_in(previous_question),
                    )).all()
                #print(selection)
            else:
                selection = Question.query.filter(Question.id.not_in(previous_question)).all()
                    
            if len(selection) > 0:
                questions = [question.format() for question in selection]
                next_question = random.choice(questions)
            
            return jsonify({
                "question": next_question
            })
        
        except:
            abort(405)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "bad request"
            }), 
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
            }),
            422,
        )


    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
            }),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "Internal server error"
            }),
            405,
        )

    return app

