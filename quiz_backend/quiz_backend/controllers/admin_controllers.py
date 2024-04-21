from typing import Annotated
from passlib.context import CryptContext
from quiz_backend.db.db_connector import get_session
from quiz_backend.setting import admin_name , admin_password
from quiz_backend.models.quiz_models import Category
from sqlmodel import SQLModel, Session, select
from fastapi import Depends, HTTPException, Response


class Admin(SQLModel):
    admin_name : str
    admin_password:str 


pwd = CryptContext(schemes="bcrypt")


def admin_login(admin_details : Admin , response :Response):
    if admin_details.admin_name == admin_name:
        if pwd.verify(admin_details.admin_password , admin_password):
            response.set_cookie('email' , admin_name , max_age=300)
            return {'message' : 'You are login'}
        else:
            raise HTTPException(status_code=404 , detail="Password is Invalid")
    else:
        raise HTTPException(status_code=404 , detail="Email is Invalid")
    

def is_name(session:Session , catgory_name:str):
    statment = select(Category).where(catgory_name == Category.category_name)
    result = session.exec(statment).first()
    if result:
        return True
    else:
        return False


def set_category(category:Category , session : Annotated[Session , Depends(get_session)]):
    is_exist = is_name(session=session , catgory_name=category.category_name)
    if is_exist:
           raise HTTPException(status_code=404 , detail="Already Exist")
    else:
         session.add(category)
         session.commit()
         session.refresh(category)
         return category