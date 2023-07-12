import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Load the lessons JSON into memory when we start
with open('lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

@app.get("/lessons/<int:lesson_number>")
async def get_lesson(lesson_number: int):
    # Get the lesson with the given number from the in-memory dictionary
    lesson = lessons["lessons"].get(str(lesson_number))

    if lesson is not None:
        return lesson
    else:
        return {"error": "Lesson not found"}

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=3333)

if __name__ == "__main__":
    main()
