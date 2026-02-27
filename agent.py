from tools import search_jobs, analyse_job, match_skills
from memory import JobDatabase

class InternshipAgent:
    def __init__(self):
        self.memory = JobDatabase()
        self.current_job = None
        self.current_skills = None

    def extract_key_info(self):
        if "data analyst" in self.goal.lower():
            return "data analyst"
        elif "investment banking" in self.goal.lower():
            return "investment banking"
        else:
            return self.goal

    def think(self):
        if not self.state["jobs_found"]:
            if self.state.get("search_attempted"):
                print("Thinking: no jobs found. Ending task.")
                self.state["completed"] = True
                return {"action": "finish"}
            print("Thinking: searching for jobs.")
            self.state["search_attempted"] = True
            return {"action": "search_jobs", "input": self.goal}
        elif not self.state["analysis_results"]:
            print("Thinking: analysing jobs.")
            return {"action": "analyse_job"}
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
        elif action == "analyse_job":
            analysis_results = []
            for job in self.state["jobs_found"]:
                skills = analyse_job(job)
                comparison = match_skills(skills)
                total_skills = len(skills)
                matched_count = len(comparison["matched_skills"])
                score = round((matched_count/total_skills) * 100, 2)
                analysis_results.append({
                    "job_title": job["title"],
                    "matched_skills": comparison["matched_skills"],
                    "missing_skills": comparison["missing_skills"],
                    "match_score_percent": score
                })
                analysis_results.sort(key=lambda x: x["match_score_percent"], reverse=True)
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

    def reflect(self):
        print("Reflection Phase:")
        if not self.state["analysis_results"]:
            print("No jobs were analysed.")
            return
        top_job = self.state["analysis_results"][0]
        print(f"Top match: {top_job['job_title']}")
        print(f"Match score: {top_job['match_score_percent']}%")
        if top_job["missing_skills"]:
            print("Skills to improve:")
            for skill in top_job["missing_skills"]:
                print(skill)
        else:
            print("You are fully qualified for this role based on listed skills.")