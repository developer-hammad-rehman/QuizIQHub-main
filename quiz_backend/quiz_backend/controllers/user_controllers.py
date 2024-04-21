from datetime import timedelta
from quiz_backend.controllers.auth_controllers import generateAccessAndRefreshToken
from quiz_backend.setting import access_expiry_time, refresh_expiry_time
from quiz_backend.utils.exception import ConflictException, InvalidInputException, NotFoundException
from quiz_backend.models.user_models import LoginModel, SignupModel, User, Token
from sqlmodel import Session, select
from quiz_backend.controllers.auth_controllers import decodeToken, generateAccessAndRefreshToken, verifyPassword, passswordIntoHash
# from quiz_backend.utils.imports import (
#     User, Token, UserModel, LoginModel, Session, select, passswordIntoHash, verifyPassword, generateToken, decodeToken, ConflictException, InvalidInputException, NotFoundException, Annotated, Depends)
from quiz_backend.models.user_models import SignupModel, User, Token, LoginModel
from ..utils.exception import ConflictException, InvalidInputException, NotFoundException
from quiz_backend.controllers.auth_controllers import passswordIntoHash, verifyPassword, generateToken, decodeToken
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import quiz_backend.setting as
from quiz_backend.db.db_connector import get_session
# Initialize OAuth2 password bearer for authentication
auth_schema = OAuth2PasswordBearer(tokenUrl="")


DBSession = Annotated[Session, Depends(get_session)]


def signupFn(user_form: SignupModel, session: DBSession):
    """
    Function to sign up a new user.

    Args:
        user_form (UserModel): The user details provided during sign up.
        session (Session): The database session.

    Returns:
        dict: A dictionary containing access and refresh tokens.
    """
    # Check if user already exists
    users = session.exec(select(User))
    for user in users:
        is_email_exist = user.user_email == user_form.user_email
        is_password_exist = verifyPassword(
            user.user_password, user_form.user_password)

        if is_email_exist and is_password_exist:
            raise ConflictException("email and password")
        elif is_email_exist:
            raise ConflictException("email")
        elif is_password_exist:
            raise ConflictException("password")

    # Hash the user's password
    hashed_password = passswordIntoHash(user_form.user_password)
    # Create a new user
    user = User(user_name=user_form.user_name,
                user_email=user_form.user_email, user_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate access and refresh tokens for the new user
    data = {
        "user_name": user.user_name,
        "user_email": user.user_email,
        "access_expiry_time": access_expiry_time,
        "refresh_expiry_time": refresh_expiry_time
    }
    print(data)
    token_data = generateAccessAndRefreshToken(data)

    # Save the refresh token in the database
    token = Token(user_id=user.user_id,
                  refresh_token=token_data["refresh_token"]["token"])
    session.add(token)
    session.commit()

    return token_data


def loginFn(login_form: LoginModel, session: DBSession):
    """
    Function to log in a user.

    Args:
        login_form (OAuth2PasswordRequestForm): The login form data.
        session (Session): The database session.

    Returns:
        dict: A dictionary containing access and refresh tokens.
    """
    print(login_form)
    users = session.exec(select(User))
    for user in users:
        user_email = user.user_email
        verify_password = verifyPassword(
            user.user_password, login_form.user_password)

        # Check if provided credentials are valid
        if user_email == login_form.user_email and verify_password:
            data = {
                "user_name": user.user_name,
                "user_email": user.user_email,
                "access_expiry_time": access_expiry_time,
                "refresh_expiry_time": refresh_expiry_time
            }
            token_data = generateAccessAndRefreshToken(data)

            # update the refresh token in the database
            token = session.exec(select(Token).where(
                Token.user_id == user.user_id)).one()
            token.refresh_token = token_data["refresh_token"]["token"]
            session.add(token)
            session.commit()
            session.refresh(token)
            return token_data
    else:
        raise InvalidInputException("Email or Password")


def getUser(token: Annotated[str, Depends(auth_schema)], session: Session):
    """
    Function to get user details using an access token.

    Args:
        token (str): The access token.
        session (Session): The database session.

    Returns:
        User: The user object.
    """
    try:
        if token:
            # Decode the access token to get user data
            data = decodeToken(token)
            user_email = data["user_email"]
            user = session.exec(select(User).where(
                User.user_email == user_email)).one()
            return user
    except:
        raise NotFoundException("Token")
