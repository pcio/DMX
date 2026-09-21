import json
from ollama import chat


SYSTEM_PROMPT = """
You control a DMX lighting system. Translate the user's request into exactly
one JSON command. Do not invent fixture IDs, groups, colours, scenes or effects.

Commands:
{"intent":"blackout"}
{"intent":"scene","name":"rock"}
{"intent":"color","target":"pars","color":"red","brightness":100}
{"intent":"effect","target":"tetra","effect":"strobe","value":100}
{"intent":"movement","target":"moving_head","movement":"pan","value":128}

Known targets: par_left, par_right, moving_head, tetra, pars, all
Known scenes: rock
Colours: red, green, blue, white, yellow, cyan, magenta, off
Effects: strobe, pulse, fade, none
Movements: pan, tilt, rotate

If the request cannot be represented, return {"intent":"unknown"}.
Return ONLY valid JSON.
"""


def ask_ai(text):
    response = chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        format="json",
    )
    return json.loads(response.message.content)
