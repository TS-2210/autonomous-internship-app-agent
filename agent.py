from tools import search_jobs, analyse_job, match_skills
from planner import Planner
from memory import JobDatabase

class InternshipAgent:
    def __init__(self):
        self.memory = JobDatabase()
        self.planner = Planner()
        self.current_job = None
        self.current_skills = None
    
    def reflect(self):
        print("Reflection Phase:")
        for result in self.analysis_results:
            if len(result["missing_skills"]) == 0:
                print(f"{result['job_title']} is a strong match for your skills.")
            else:
                print(f"For {result['job_title']}, you should improve:")
                for skill in result["missing_skills"]:
                    print(skill)

    def think(self):
        if not self.state["jobs_found"]:
            print("Thinking: searching for jobs.")
            return {"action": "search_jobs", "input": self.goal}
        elif not self.state["analysis_results"]:
            print("Thinking: analysing jobs.")
            return {"action": "analyse_jobs"}
        else:
            print("Thinking: task complete.")
            self.state["completed"] = True
            return {"action": "finish"}
        
    def act(self, action_dict):
        action = action_dict["action"]
        if action == "search_jobs":
            results = search_jobs(action_dict["input"], self.memory)
            print("Jobs found:", results)
            self.state["jobs_found"] = results
        elif action == "analyse_jobs":
            analysis_results = []
            for job in self.state["jobs_found"]:
                skills = analyse_job(job)
                comparison = match_skills(skills)
                analysis_results.append({
                    "job_title": job["title"],
                    "matched_skills": comparison["matched_skills"],
                    "missing_skills": comparison["missing_skills"]
                })
            print("Analysis complete:", analysis_results)
            self.state["analysis_results"] = analysis_results
        elif action == "finish":
            print("Agent has finished the task.")

    def run(self, goal):
        print(f"Goal: {goal}")
        self.goal = goal
        self.state = {
            "jobs_found": [],
            "analysis_results": [],
            "completed": False
        }
        step_counter = 0
        max_steps = 5
        while not self.state["completed"] and step_counter < max_steps:
            print(f"Step {step_counter + 1}")
            action = self.think()
            self.act(action)
            step_counter += 1
        print("Final State:")
        print(self.state)
        print("Database contents:", self.memory.get_jobs())
        self.reflect()
