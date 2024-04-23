from openai import OpenAI
from quiz_backend.setting import opena_ai_api_key

client = OpenAI(api_key=opena_ai_api_key)