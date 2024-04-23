from quiz_backend.helper.openai_client import client
import json

def openai_question(category:str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={ "type": "json_object" },
        messages=[
            {'role':"system" , 'content':"You are the mcq generator in JSON OUTPUT"},
            {'role':'user' , 'content':f"Genrate me 1 mcq related to this category {category}"}
        ]
    )
    return json.loads(response.choices[0].message.content)