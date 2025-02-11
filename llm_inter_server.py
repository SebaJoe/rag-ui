from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import time

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

#openai.api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI()

global_message_chain = []

@app.route('/stream', methods=['GET', 'POST'])
def stream():
    # Get the prompt from the POST request's JSON body
    
    if request.method == 'POST':
        
        global global_message_chain
        data = request.get_json()
        message_chain = data.get('messages')
        global_message_chain = message_chain
    
    # def event_stream():
    #     for chunk in client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=message_chain,
    #         stream=True
    #     ):
    #         text = chunk.choices[0].delta.content
    #         if text:
    #             yield f"data: {text}\n\n"
    
        print(message_chain)
        
        return jsonify({'status': 'accepted'})
    
    # def event_stream():
    #     print(global_message_chain)
    #     tokens = "Hello, this is a mocked chatbot. How can I help you?".split(" ")
    #     for token in tokens:
    #         time.sleep(0.5)
    #         yield f"data: {token}\n\n"
    #     yield "data: [DONE]\n\n"
        
    def event_stream():
        for chunk in client.chat.completions.create(
            model="gpt-4o-mini",
            messages=global_message_chain,
            stream=True
        ):
            text = chunk.choices[0].delta.content
            if text:
                print(repr(text))
                text = text.replace('\n', "<NEWLINE>")
                yield f"data: {text}\n\n"
                
            if chunk.choices[0].finish_reason == "stop":
                yield "data: [DONE]\n\n"
    
    
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
