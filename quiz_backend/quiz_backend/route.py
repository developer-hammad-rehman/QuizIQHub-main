from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlmodel import Session
from quiz_backend.controllers.admin_controllers import admin_login, set_category , set_quiz_level ,  set_questions , set_choice
from quiz_backend.db.db_connector import createTable
from contextlib import asynccontextmanager
from quiz_backend.utils.exception import NotFoundException, ConflictException, InvalidInputException
from quiz_backend.controllers.user_controllers import signupFn, loginFn
from typing import Annotated
from .utils.exception import NotFoundException, ConflictException, InvalidInputException
from quiz_backend.controllers.quiz_controllers import get_categrios, get_question, get_quiz_diff
from quiz_backend.db.db_connector import get_session
from quiz_backend.controllers.openai_apis.question_generate import openai_question

# Define async context manager for application lifespan
@asynccontextmanager
async def lifeSpan(app: FastAPI):
    """
    Async context manager to handle application lifespan events.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Nothing is yielded.
    """
    print("Creating tables...")
    createTable()
    yield

# Create FastAPI application instance with custom lifespan event handler
app = FastAPI(title="OAuth2 Microservice",
              description="A multi-user OAuth2 microservice with login/password signin and Google signin features.",
              version="1.0.0",
              terms_of_service="https://quiz_app.vercel.app/terms/",
              lifespan=lifeSpan,
              contact={
                  "name": "Muhammad Ahsaan Abbasi",
                  "url": "http://localhost:8000/contact/",
                  "email": "mahsaanabbasi@gmail.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
              },
              servers=[
                  {
                      "url": "http://localhost:8000",
                      "description": "Local server"
                  },
              ],)

# add middleware for cors error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

# Exception handlers for custom exceptions


@app.exception_handler(NotFoundException)
def not_found(request: Request, exception: NotFoundException):
    """
    Exception handler for NotFoundException.

    Args:
        request (Request): The HTTP request.
        exception (NotFoundException): The NotFoundException instance.

    Returns:
        JSONResponse: JSON response with 404 status code and error message.
    """
    return JSONResponse(status_code=400, content=f"{exception.not_found} Not found")


@app.exception_handler(ConflictException)
def conflict_exception(request: Request, exception: ConflictException):
    """
    Exception handler for ConflictException.

    Args:
        request (Request): The HTTP request.
        exception (ConflictException): The ConflictException instance.

    Returns:
        JSONResponse: JSON response with 404 status code and error message.
    """
    return JSONResponse(status_code=409, content=f"This {exception.conflict_input} already exists!")


@app.exception_handler(InvalidInputException)
def invalid_exception(request: Request, exception: InvalidInputException):
    """
    Exception handler for InvalidInputException.

    Args:
        request (Request): The HTTP request.
        exception (InvalidInputException): The InvalidInputException instance.

    Returns:
        JSONResponse: JSON response with 404 status code and error message.
    """
    return JSONResponse(status_code=400, content=f"Invalid {exception.invalid_input}!")

# Define route for home endpoint


@app.get("/")
def home():
    """
    Route for home endpoint.

    Returns:
        str: Welcome message.
    """
    return "Welcome to the Quiz Project..."


@app.post("/api/userSignup")
def userSignup(response: Response, token_data: Annotated[dict, Depends(signupFn)]):
    if token_data:
        print(token_data["refresh_token"]
              ["refresh_expiry_time"].total_seconds())
        response.set_cookie(key="access_token",
                            value=token_data["access_token"]["token"],
                            expires=int(
                                token_data["access_token"]["access_expiry_time"].total_seconds())
                            )
        response.set_cookie(key="refresh_token",
                            value=token_data["refresh_token"]["token"],
                            max_age=int(
                                token_data["refresh_token"]["refresh_expiry_time"].total_seconds())
                            )

        return "You have registered successfully"
    raise NotFoundException("User")


@app.post("/api/Signin")
def userSignin(request: Request, response: Response, token_data: Annotated[dict, Depends(loginFn)]):
    if token_data:
        print(token_data["refresh_token"]
              ["refresh_expiry_time"].total_seconds())
        print(request.headers)
        response.set_cookie(key="access_token",
                            value=token_data["access_token"]["token"],
                            expires=int(
                                token_data["access_token"]["access_expiry_time"].total_seconds())
                            )
        response.set_cookie(key="refresh_token",
                            value=token_data["refresh_token"]["token"],
                            max_age=int(
                                token_data["refresh_token"]["refresh_expiry_time"].total_seconds())
                            )

        return "You have logged in successfully"
    raise NotFoundException("User")


# @app.get("/api/getUser")
# def getUser(user: str):
#     """
#     Route to get user details.

#     Args:
#         user (str): User identifier.

#     Returns:
#         str: Success message if user found, else raises NotFoundException.
#     """
#     if user == "bilal":
#         raise NotFoundException("User")
#     return "User has been found"




@app.get('/api/get_category')
def categories_route(session : Annotated[Session , Depends(get_session)]):
    return get_categrios(session)



@app.get('/api/get_quiz_level')
def quiz_level_route(id : int ,  session : Annotated[Session , Depends(get_session)]):
    return get_quiz_diff(category_id=id , session=session)



@app.get('/api/quiz_question')
def quiz_question_route(quiz_level_id : int , session : Annotated[Session , Depends(get_session)]):
    return get_question(question_level_id=quiz_level_id , session=session)


@app.post('/api/admin_login')
def admin_auth(admin = Depends(admin_login)):
    return admin


@app.post('/api/catgory_add')
def admin_auth(add_catgory = Depends(set_category)):
    return add_catgory


@app.post('/api/quiz_level')
def add_quiz_level_route(route_func = Depends(set_quiz_level)):
    return route_func



@app.post('/api/add_question')
def add_quiz_question(route_func = Depends(set_questions)):
    return route_func


@app.post('/api/add_choices')
def add_choices_route(route_func = Depends(set_choice)):
    return route_func


@app.get('/api/openai_question')
def ai_route(route_func = Depends(openai_question)):
    return route_func