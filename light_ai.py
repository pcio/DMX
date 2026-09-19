import json
from ollama import chat


SYSTEM_PROMPT = """
You control a QTX Tetra 4-in-1 light.

You must translate the user's natural language into
a JSON command.

Available commands:

blackout:
{}

white:
{"action": "white"}

uv:
{"action": "uv"}

water:
{"action": "water", "value": 0-255}

fireball:
{"action": "fireball", "colour": "red|green|blue|redgreen|greenblue|redblue|all|off"}

laser:
{"action": "laser", "colour": "red|green|redgreen|off"}

strobe:
{"action": "strobe", "value": 0-255}

water_speed:
{"action": "water_speed", "value": 0-255}

fire_speed:
{"action": "fire_speed", "value": 0-255}

laser_rotate:
{"action": "laser_rotate", "value": 0-255}

auto1:
{"action": "auto1"}

auto2:
{"action": "auto2"}

sound1:
{"action": "sound1"}

sound2:
{"action": "sound2"}

If the user asks for something you cannot express
using these commands, return:

{"action": "unknown"}

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