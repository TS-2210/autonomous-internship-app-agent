class Planner:
    def create_plan(self, goal):
        return [
            {"action": "search_jobs", "input": "Data Analyst"},
            {"action": "analyse_job"},
            {"action": "match_skills"}
        ]