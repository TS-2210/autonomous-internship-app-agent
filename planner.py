class Planner:
    def create_plan(self, goal):
        if "data analyst" in goal.lower():
            query = "Data Analyst"
        elif "investment banking" in goal.lower():
            query = "Investment Banking"
        else:
            query = goal

        return [
            {"action": "search_jobs", "input": query},
            {"action": "analyse_job"}
        ]