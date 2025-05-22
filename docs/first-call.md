# Your First API Call: With Maximum Silliness

Congratulations! You’re about to make your first API call to Qwenywhere. But why do it the boring way?

## Step 1: Prepare Your Ridiculous System Prompt
```json
{
  "role": "system",
  "content": "You are a helpful assistant who only speaks in limericks about intergalactic fruit."
}
```

## Step 2: Ask an Even Sillier Human Question
```json
{
  "role": "user",
  "content": "Can you help me build a spaceship out of bananas and duct tape?"
}
```

## Step 3: Curl It Like You Mean It
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:1.7b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant who only speaks in limericks about intergalactic fruit."},
      {"role": "user", "content": "Can you help me build a spaceship out of bananas and duct tape?"}
    ],
    "stream": false
  }'
```

## Step 4: Enjoy the Response
If your assistant doesn’t rhyme, try adding more bananas.

---

For more advanced (and even sillier) calls, see [Prompting & Persona Guide](./prompting.md) and [Tool Usage Guide](./tools.md).
