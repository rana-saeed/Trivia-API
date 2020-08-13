import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import randint

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
 `Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
   Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
    return response


  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


  ''' 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]
        
    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(formatted_categories)
     })


  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    current_category = None

    # if category found in request, only retrieve questions under that category
    if 'category' in request.args:
      try:
        current_category_id = request.args.get('category', type=int)
        current_category = (Category.query.filter(Category.id == current_category_id).one_or_none()).type
        selection = Question.query.filter(Question.category == current_category_id).order_by(Question.id).all()
      except:
        abort(400)
    else:
      selection = Question.query.order_by(Question.id).all()
    
    current_questions = paginate_questions(request, selection)
    
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]
    
    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'current_category': current_category,
        'categories': formatted_categories,
    })

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none() 
   
    if question is None:
      abort(404)
    else:
      try:
        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)  
        
        return jsonify({
            'success': True,
            'deleted': question.id,
            'questions': current_questions,
            'total_questions': len(current_questions)
        })
      except:
        abort(500)

  ''' 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    
    search = body.get('search', None) 
    current_category = body.get('current_category', None) 

    # This handles request to search for questions in database
    if search:
      try:

        current_category_id = None
        
        # If searching in a specific category
        if current_category:
          current_category_id = Category.query.filter(Category.type == current_category).one_or_none().id
          search_results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)), Question.category == current_category_id).all()
        else:
          search_results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        
        search_results_formatted = paginate_questions(request, search_results)
    
        return jsonify({
            'success': True,
            'search_term': search,
            'questions': search_results_formatted,
            'total_questions': len(search_results_formatted),
            'current_category': current_category_id
        })
      except:
        abort(500)
    #This handles request to add new question to database
    else:
      if None in(question, answer, category, difficulty):
        abort(400)
      
      if isinstance(question, str) == False: 
        abort(422)

      try:
        question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)       

        return jsonify({
                'success': True,
                'added': question.id,
                'questions': current_questions,
                'total_questions': len(current_questions)
        })
      except:
        abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_questions_fors_quiz():
    body = request.get_json()

    questions_per_play = body.get('questions_per_play', None)
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    if None in(questions_per_play, previous_questions, quiz_category):
        abort(400)
    
    try:
      # Get questions for all categories
      if quiz_category['id'] == 0:
        questions = Question.query.all()
        
      # Get questions for specific category
      else:
        questions = Question.query.filter(Question.category == quiz_category['id']).all()
    
      # Handles case if available questions are less than questions per play
      force_end = False
      if len(questions) < questions_per_play and (len(questions) - len(previous_questions)) == 0:
        force_end = True
        return jsonify({
              'success': True,
              'question': None,
              'force_end': force_end
          })

      random_question_num = randint(0,len(questions)-1)

      # Validate that new question was not in previous questions
      while questions[random_question_num].id in previous_questions:
        random_question_num = randint(0,len(questions)-1)

      print(random_question_num )
      question = questions[random_question_num].format()

      return jsonify({
              'success': True,
              'question': question,
              'force_end': force_end
          })
    except:
      abort(422)

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422
    
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
      }), 500

  return app

    