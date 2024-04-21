from typing import Optional
from sqlmodel import SQLModel, Field

# Defining the Admin model using SQLModel
class Admin(SQLModel, table=True):
    # Define fields with optional primary key
    admin_id: Optional[int] = Field(None, primary_key=True)
    admin_email: str  # Admin's email address
    admin_name: str   # Admin's name
    admin_password: str  # Admin's password