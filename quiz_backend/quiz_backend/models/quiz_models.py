from typing import Optional
from sqlmodel import SQLModel, Field

# Define Category model
class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(None, primary_key=True)
    category_name: str  # Name of the category
    category_description: str  # Description of the category

# Define QuizLevel model with foreign key relationship to Category
class QuizLevel(SQLModel, table=True):
    quiz_level_id: Optional[int] = Field(None, primary_key=True)
    quiz_level: str  # Level of the quiz
    category_id: int  = Field(int, foreign_key="category.category_id")  # Foreign key relationship to Category

# Define Quiz model with foreign key relationship to QuizLevel
class Quiz(SQLModel, table=True):
    question_id: Optional[int] = Field(None, primary_key=True)
    question: str  # Question for the quiz
    quizLevel_id: Optional[int]  = Field(int, foreign_key="quizlevel.quiz_level_id")  # Foreign key relationship to QuizLevel


    
# Define Choices model with foreign key relationship to Quiz
class Choices(SQLModel, table=True):
    choice_id: Optional[int] = Field(None, primary_key=True)
    quiz_id: int  = Field(int, foreign_key="quiz.question_id")  # Foreign key relationship to Quiz
    choice: str  # Choice for the question
    status: bool = False  # Status of the choice (correct or incorrect)
