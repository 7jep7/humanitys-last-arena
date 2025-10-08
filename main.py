import yaml
from player import Player

with open('config.yaml') as f:
    config = yaml.safe_load(f)

players = [Player(f"Player{i+1}", config['openai_api_key'], config) for i in range(config['num_players'])]


# Phase 1: Question generation
all_questions = []
for player in players:
    questions = player.generate_questions(categories=["math", "ethics", "logic"])
    all_questions.extend([(player.name, q) for q in questions])

print("Questions generated:")
for author, q in all_questions:
    print(f"{author}: {q}")

# Phase 2: Question rating
print("\nQuestion ratings:")
question_ratings = {}
for i, (author, q) in enumerate(all_questions):
    question_ratings[q] = {}
    for player in players:
        if player.name != author:
            rating = player.rate_questions([q])[0]
            question_ratings[q][player.name] = rating
            print(f"{player.name} rated '{q}' (by {author}): {rating}")

# Phase 3: Answering
print("\nAnswers:")
answers = []  # (question, author, answerer, answer)
for player in players:
    player_answers = player.answer_questions([q for _, q in all_questions])
    for (author, q), a in zip(all_questions, player_answers):
        answers.append((q, author, player.name, a))
        print(f"{player.name} answered '{q}' (by {author}): {a}")


# Phase 4: Judging answers
print("\nAnswer judgments:")
answer_judgments = {}  # (q, answerer) -> {judge: score}
for q, author, answerer, a in answers:
    key = (q, answerer)
    answer_judgments[key] = {}
    for player in players:
        if player.name != answerer:
            score = player.judge_answers([a])[0]
            answer_judgments[key][player.name] = score
            print(f"{player.name} judged answer to '{q}' by {answerer}: {score}")

# --- Aggregation and Results ---
import statistics

print("\n--- Aggregated Results ---")


# Aggregate question ratings (mean and std)
print("\nAverage question ratings (mean ± std):")
avg_question_ratings = {}
std_question_ratings = {}
for q, ratings in question_ratings.items():
    values = list(ratings.values())
    avg = statistics.mean(values) if values else 0
    std = statistics.stdev(values) if len(values) > 1 else 0
    avg_question_ratings[q] = avg
    std_question_ratings[q] = std
    print(f"'{q}': {avg:.2f} ± {std:.2f}")


# Aggregate answer scores (mean and std)
print("\nAverage answer scores (mean ± std):")
avg_answer_scores = {}
std_answer_scores = {}
for (q, answerer), scores in answer_judgments.items():
    values = list(scores.values())
    avg = statistics.mean(values) if values else 0
    std = statistics.stdev(values) if len(values) > 1 else 0
    avg_answer_scores[(q, answerer)] = avg
    std_answer_scores[(q, answerer)] = std
    print(f"Answer to '{q}' by {answerer}: {avg:.2f} ± {std:.2f}")

# Aggregate player scores (mean of their answers' scores)
print("\nPlayer scores (mean of their answers' scores):")
player_scores = {player.name: [] for player in players}
for (q, answerer), avg in avg_answer_scores.items():
    player_scores[answerer].append(avg)
for player, scores in player_scores.items():
    mean_score = statistics.mean(scores) if scores else 0
    print(f"{player}: {mean_score:.2f}")
