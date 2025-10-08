import yaml
from player import Player
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

with open('config.yaml') as f:
    config = yaml.safe_load(f)

players = [
    Player(
        player_cfg['name'],
        config['openai_api_key'],
        {**config, 'openai_model': player_cfg['model']}
    )
    for player_cfg in config['players']
]



# Phase 1: Question generation
print("\n[Phase 1] Generating questions...")
all_questions = []
for player in tqdm(players, desc="Players", unit="player"):
    questions = player.generate_questions(categories=["math", "ethics", "logic"])
    all_questions.extend([(player.name, q) for q in questions])

print("Questions generated:")
for author, q in all_questions:
    print(f"{author}: {q}")



# Phase 2: Question rating (short test: assign all ratings to 5)
print("\n[Phase 2] Rating questions (all ratings set to 5 for test)...")
question_ratings = {}
for i, (author, q) in enumerate(tqdm(all_questions, desc="Questions", unit="q")):
    question_ratings[q] = {}
    for player in players:
        if player.name != author:
            rating = 5  # Normalized test rating
            question_ratings[q][player.name] = rating
            print(f"{player.name} rated '{q}' (by {author}): {rating}")


# Phase 3: Answering
print("\n[Phase 3] Answering questions...")
answers = []  # (question, author, answerer, answer)
for player in tqdm(players, desc="Players", unit="player"):
    player_answers = player.answer_questions([q for _, q in all_questions])
    for (author, q), a in zip(all_questions, player_answers):
        answers.append((q, author, player.name, a))
        print(f"{player.name} answered '{q}' (by {author}): {a}")





# Phase 4: Judging answers (AI-based)
print("\n[Phase 4] Judging answers (AI-based)...")
answer_judgments = {}  # (q, answerer) -> {judge: score}
for q, author, answerer, a in tqdm(answers, desc="Answers", unit="ans"):
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
avg_question_ratings = {}
std_question_ratings = {}
for q, ratings in question_ratings.items():
    values = list(ratings.values())
    avg = statistics.mean(values) if values else 0
    std = statistics.stdev(values) if len(values) > 1 else 0
    avg_question_ratings[q] = avg
    std_question_ratings[q] = std

# Aggregate answer scores (mean and std)
avg_answer_scores = {}
std_answer_scores = {}
for (q, answerer), scores in answer_judgments.items():
    values = list(scores.values())
    avg = statistics.mean(values) if values else 0
    std = statistics.stdev(values) if len(values) > 1 else 0
    avg_answer_scores[(q, answerer)] = avg
    std_answer_scores[(q, answerer)] = std

# Aggregate player scores (mean of their answers' scores)
player_scores = {player.name: [] for player in players}
for (q, answerer), avg in avg_answer_scores.items():
    player_scores[answerer].append(avg)
player_score_means = {player: statistics.mean(scores) if scores else 0 for player, scores in player_scores.items()}

# Display results using pandas
print("\nQuestion Ratings Table:")
df_q = pd.DataFrame([
    {"question": q, "mean": avg_question_ratings[q], "std": std_question_ratings[q]} for q in avg_question_ratings
])
print(df_q.to_string(index=False))

print("\nAnswer Scores Table:")
df_a = pd.DataFrame([
    {"question": q, "answerer": answerer, "mean": avg_answer_scores[(q, answerer)], "std": std_answer_scores[(q, answerer)]}
    for (q, answerer) in avg_answer_scores
])
print(df_a.to_string(index=False))

print("\nPlayer Scores:")
df_p = pd.DataFrame([
    {"player": player, "mean_score": player_score_means[player]} for player in player_score_means
])
print(df_p.to_string(index=False))

# Optional: Box and whisker plot for answer scores
try:
    plt.figure(figsize=(10, 6))
    box_data = [
        [avg_answer_scores[(q, answerer)] for (q, answerer) in avg_answer_scores if answerer == player]
        for player in player_score_means
    ]
    plt.boxplot(box_data, labels=list(player_score_means.keys()))
    plt.title("Distribution of Answer Scores by Player")
    plt.ylabel("Score")
    plt.xlabel("Player")
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"[Plotting error] {e}")
