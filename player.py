import openai
import yaml

class Player:
    def __init__(self, name, api_key, config):
        self.name = name
        self.api_key = api_key
        self.config = config
        openai.api_key = api_key

    def generate_questions(self, categories):
        # Minimal stub: returns dummy questions
        return [f"Question {i+1} from {self.name}" for i in range(self.config['questions_per_player'])]

    def rate_questions(self, questions):
        # Minimal stub: returns random ratings
        return [5 for _ in questions]

    def answer_questions(self, questions):
        # Minimal stub: returns dummy answers
        return [f"Answer to '{q}' by {self.name}" for q in questions]

    def judge_answers(self, answers):
        # Minimal stub: returns random scores
        return [5 for _ in answers]
