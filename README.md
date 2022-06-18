# Trivia App

Trivia is a gaming site where the users are asked questions about interesting facts in many categories. This site lets you:
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


## Getting Started
Download the project code locally
[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. 

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

## Backend

### Installation

1. **Virtual Environment** - This keeps your dependencies for each project separate and organized. 
Initialize and activate a virtualenv using:
```
python -m virtualenv env
source env/bin/activate
```

Note - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

2. **PIP Dependencies** - Once the virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory on the terminal and running:
```
pip install -r requirements.txt
```
All required packages are included in the requirements file. 


3. **Set up the Database**
With Postgres running, create a `trivia` database:

```
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```
psql trivia < trivia.psql
```

4. **Run the development server**
To run the application run the following commands from the /backend directory: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).



### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. This project depends on Nodejs and Node Package Manager (NPM).

From the frontend folder(naviagate to /frontend directory), run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 
This frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected i.e Ensure the backend is already running in a terminal then open a new terminal and type the commands to run the frontend above.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404, 
    "message": "resource not found"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable
- 500: Internal server error

### Endpoints 
#### GET /categories
- Sample URL: `curl http://127.0.0.1:5000/categories`
- Request Arguments: None
- Response body:
  - Returns a dictionary of categories in which the keys are the ids and the values are the corresponding string of the category.
``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET /questions
- Sample URL: `curl http://127.0.0.1:5000/questions?page=1`
- Request Arguments: page - integer
- Response body:
  - Returns a list of random question objects, total number of questions, current category, and a dictionary of categories in which the keys are the ids and the values are the corresponding string of the category.
  - Questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
```{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "totalQuestions": 19
}
```

#### POST /questions - To create new questions
- Sample URL: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"New question", "answer":"New answer", "category":"5", "difficulty": "2"}'`
- Request Arguments: question, answer, category and difficulty.
- Response body:
  - Creates a new question using the submitted question, answer, category and difficulty. 
  - Returns the id of the created question and success value.
```
{
  "created": 24,
  "success": true
}
```

#### POST /questions - To search
- Sample URL: ` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"body"}'`
- Request Arguments: searchTerm
- Response body:
  - Returns a list of question objects, total number of questions that met the search term and current category string.
  - Returned questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
```{
  "currentCategory": "History",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "totalQuestions": 1
}
```

#### DELETE /questions/{id}
- Sample URL: `curl -X DELETE http://127.0.0.1:5000/questions/2`
- Request Arguments: id - integer
- Response body:
  - Deletes the question of the given ID if it exists. 
  - Returns success value and the id of the deleted question.
```{
  "deleted": 2,
  "success": true
}
```

#### GET /categories/id/questions
- Sample URL: `curl http://127.0.0.1:5000/categories/3/questions`
- Request Arguments: id - integer
- Response body:
  - Returns a list of question objects for the given category, total questions and current category.
  - Returned questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
```{
  "currentCategory": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "totalQuestions": 3
}
```

#### GET /quizzes
- Sample URL: ` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16, 17], "quiz_category": {"type": "Art", "id": "2"}}'`
- Request Arguments: quiz_category and previous_questions
- Response body:
  - Returns a random question object within the given category, if provided, and that is not one of the previous questions.
```{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }
}
```


## Deployment N/A

## Authors
Precious Michael

## Acknowledgements 
Coach Caryn and the Udacity team.