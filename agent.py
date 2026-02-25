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

    def run(self, goal):
        print(f"Goal: {goal}")
        plan = self.planner.create_plan(goal)
        print("Generated plan:", plan)
        for step in plan:
            action = step["action"]
            if action == "search_jobs":
                results = search_jobs(step["input"], self.memory)
                print("Search results:", results)
                self.current_jobs = results
            elif action == "analyse_job":
                all_results = []
                for job in self.current_jobs:
                    skills = analyse_job(job)
                    comparison = match_skills(skills)
                    result = {
                        "job_title": job["title"],
                        "matched_skills": comparison["matched_skills"],
                        "missing_skills": comparison["missing_skills"]
                    }
                    all_results.append(result)
                self.analysis_results = all_results
                print("Multi-job analysis:")
                for r in all_results:
                    print(r)
            elif action == "match_skills":
                if self.current_skills:
                    comparison = match_skills(self.current_skills)
                    print("Skill Comparison:", comparison)
        print("Database contents:", self.memory.get_jobs())
        self.reflect()
