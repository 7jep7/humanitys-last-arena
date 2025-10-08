
import openai
from openai import OpenAI
import yaml

class Player:
    def __init__(self, name, api_key, config):
        self.name = name
        self.api_key = api_key
        self.config = config
        self.client = OpenAI(api_key=self.api_key)


    def generate_questions(self, categories):
        prompt = (
            f"You are a creative and fair question designer for a general intelligence tournament. "
            f"Generate {self.config['questions_per_player']} diverse, challenging, and clear questions "
            f"across the following categories: {', '.join(categories)}. "
            f"Return the questions as a numbered list, one per line."
        )
        response = self.client.chat.completions.create(
            model=self.config.get('openai_model', 'gpt-3.5-turbo'),
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=self.config.get('token_limit_question_gen', 1000),
            temperature=0.7
        )
        content = response.choices[0].message.content
        # Parse numbered list
        questions = [line.split('. ', 1)[-1].strip() for line in content.split('\n') if line.strip() and line[0].isdigit()]
        # Fallback if parsing fails
        if not questions:
            questions = [content.strip()]
        return questions[:self.config['questions_per_player']]


    def rate_questions(self, questions):
        ratings = []
        for q in questions:
            prompt = (
                f"Rate the following question for clarity and relevance on a scale from 0 (poor) to 10 (excellent):\n"
                f"Question: {q}\n"
                f"Respond with a single integer."
            )
            response = self.client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=[{"role": "system", "content": "You are a fair and critical judge."},
                          {"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.0
            )
            content = response.choices[0].message.content
            try:
                rating = int(''.join(filter(str.isdigit, content.strip())))
            except Exception:
                rating = 5
            ratings.append(min(max(rating, 0), 10))
        return ratings


    def answer_questions(self, questions):
        answers = []
        for q in questions:
            prompt = (
                f"Answer the following question as clearly and concisely as possible:\n"
                f"Question: {q}"
            )
            response = self.client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=[{"role": "system", "content": "You are a helpful and knowledgeable assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=self.config.get('token_limit_answer', 100),
                temperature=0.7
            )
            content = response.choices[0].message.content
            answers.append(content.strip())
        return answers


    def judge_answers(self, answers):
        scores = []
        for a in answers:
            prompt = (
                f"Judge the following answer on a scale from 0 (very poor) to 10 (excellent) for correctness, completeness, and clarity.\n"
                f"Answer: {a}\n"
                f"Respond with a single integer."
            )
            response = self.client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-3.5-turbo'),
                messages=[{"role": "system", "content": "You are a fair and critical judge."},
                          {"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.0
            )
            content = response.choices[0].message.content
            try:
                score = int(''.join(filter(str.isdigit, content.strip())))
            except Exception:
                score = 5
            scores.append(min(max(score, 0), 10))
        return scores
