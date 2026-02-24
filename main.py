import os
import sqlite3
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

## Database setup
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS jobs (
          title TEXT,
          location TEXT,
          skills TEXT
          )''')
conn.commit()

## Sample data
sample_jobs = [
    {
        "title": "Data Analyst Intern",
        "location": "London",
        "skills": ["Python", "Statistics", "Machine Learning", "Linear Algebra"]
    },
    {
        "title": "Investment Banking Summer Analyst",
        "location": "Manchester",
        "skills": ["Excel", "Financial Modelling", "Valuation", "PowerPoint"]
    }
]
sample_skills = ["Python", "Machine Learning", "Statistics", "PowerPoint", "Linear Algebra"]

## Tool definitions
def search_jobs(query: str):
    results = [job for job in sample_jobs if query.lower() in job["title"].lower()]
    for job in results:
        c.execute("INSERT INTO jobs VALUES (?, ?, ?)", (job["title"], job["location"], json.dumps(job["skills"])))
    conn.commit()
    return json.dumps(results)

def analyse_job(job_json: str):
    job = json.loads(job_json)
    return json.dumps(job["skills"])

def match_skills(job_skills_json: str):
    job_skills = json.loads(job_skills_json)
    matched = [skill for skill in job_skills if skill in sample_skills]
    missing = [skill for skill in job_skills if skill not in sample_skills]

    return json.dumps({
        "matched_skills": matched,
        "missing_skills": missing
    })

## Tool definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": "Search for internships by job title keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyse_job",
            "description": "Extract required skills from a job.",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_json": {"type": "string"}
                },
                "required": ["job_json"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "match_skills",
            "description": "Compare job skills with candidate's CV skills.",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_skills_json": {"type": "string"}
                },
                "required": ["job_skills_json"]
            }
        }
    }
]

## Planning stage
user_goal = "Find me data analyst internships and tell me which skills I am missing."

planning_prompt = f"""
You are an autonomous career agent.
The user's goal is: {user_goal}
Create a short step-by-step plan using available tools:
- search_jobs
- analyse_job
- match_skills
Return the plan as clearly set out steps.
"""

plan_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": planning_prompt}]
)

plan = plan_response.choices[0].message.content
print(f"Generated Plan:\n{plan}\n")

messages = [
    {"role": "user", "content": user_goal}
]

#messages = [
#        {"role": "system", "content": "You are a job application assistant. You help users find internships and analyse job requirements. You are truthful and only use the provided tools to answer questions about job searching and skill matching."},
#        {"role": "user", "content": "Find me data analyst internships in London and tell me what skills I need to work on."}
#    ]

response = client.chat.completions.create( # chat completion with tool calls
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)
message = response.choices[0].message

## Tool execution loop
while message.tool_calls:
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    print(f"Tool call: {tool_name} with args {tool_args}")
    if tool_name == "search_jobs":
        tool_response = search_jobs(tool_args["query"])
    elif tool_name == "analyse_job":
        tool_response = analyse_job(tool_args["job_json"])
    elif tool_name == "match_skills":
        tool_response = match_skills(tool_args["job_skills_json"])
    else:
        tool_response = json.dumps({"error": "Unknown tool"})
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": tool_response
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

print("\nFinal Response:")
print(message.content)

## Reflection stage
reflection_prompt = f"""
Evaluate this output from 1-10 for usefulness and clarity.
If it is below 8, rewrite it to improve it.
Output:
{message.content}
"""
reflection = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": reflection_prompt}]
)
print("\nReflection:")
print(reflection.choices[0].message.content)