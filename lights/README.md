# Lights

Refactored DMX lighting controller.

## Architecture

- `fixtures/` — fixture-specific DMX channel mappings
- `bizz/fixture_manager.py` — loads fixtures from YAML
- `bizz/groups.py` — named fixture groups
- `bizz/engine.py` — lighting state and high-level operations
- `bizz/dmx_layer.py` — converts fixture state into a 512-channel universe
- `bizz/scene_engine.py` — scene registration/execution
- `scenes/` — reusable lighting scenes
- `ai/` — natural-language command translation

The DMX layer currently keeps the generated universe in memory. Hardware output can be added without changing the fixture or scene API.

## Run

From the `lights` directory:

```bash
python lights.py
```

The AI part requires Ollama and the `qwen3:1.7b` model, as in the original project.

## Important

The PAR100 and TMH13 channel mappings are based on the operations present in the original project. Verify them against the actual fixture manuals before connecting real hardware.
