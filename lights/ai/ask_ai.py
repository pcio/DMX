import json
from ollama import chat


SYSTEM_PROMPT = """
You control a lighting system with multiple lamps and effects. Color, intensity and prenamed scenes are available for use.

You must translate the user's natural language into a JSON command.

Available commands:

blackout:
{}

scene:
{"intent": "scene", "name": "scene1"}

color:
{"intent": "color",
 "color": "red|green|blue|white|redgreen|bluewhite|greenblue|redgreenblue|bluepurple|greenwhite|greenbluepurple|redgreenwhite|bluepurplewhite|greenbuewhite|greenbluepurplewhite|off",
 "brightness": 0-255
}

effect:
{"intent": "effect",
 "effect": "none|fade|strobe|pulse",
 "brightness": 0-255
}

movement:
{"intent": "movement",
 "movement": "none|pan|tilt|rotate"
}


If the user asks for something you cannot express
using these commands, return:

{"intent": "unknown"}

Return ONLY valid JSON.
"""


def ask_ai(text):

    response = chat(
        model="qwen3:1.7b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ],
        format="json"
    )

    return json.loads(response.message.content)