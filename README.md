## Code Challenge - Python

Develop a Python script that:
- processes AI agent logs
- extracts useful insights
- presents the results in a structured format.

## Requirements:
The logs contain records in the following format:
```
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
```

The script should:
- [ ] Count the number of messages by type
   - [ ] INFO
   - [ ] ERROR
   - [ ] WARNING 
- [ ] Display the most frequently used phrases.
- [ ] Display the most common errors 
   - [ ] and their frequencies

Example Output:
```
Log Summary:
- INFO messages: 42
- ERROR messages: 8
- WARNING messages: 5

Top 3 AI Responses:
1. "Hello! How can I help you today?" (12 times)
2. "I'm sorry, I didn't understand that." (7 times)
3. "Please provide more details." (5 times)

Most Common Errors:
1. Model Timeout after 5000ms (3 times)
2. API Connection Failure (2 times)
```

---

## Running the project
- Run, in the root of the project:
  - `./run.sh`
- Follow the instructions on the script output
