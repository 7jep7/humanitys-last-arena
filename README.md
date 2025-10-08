# Prompts and Models Used

This project uses the OpenAI Chat API for all phases. The default model is `gpt-3.5-turbo`, but this can be changed in `config.yaml` with the `openai_model` parameter.

**1. Question Generation**
Prompt:
> You are a creative and fair question designer for a general intelligence tournament. Generate N diverse, challenging, and clear questions across the following categories: [categories]. Return the questions as a numbered list, one per line.

**2. Question Rating**
Prompt:
> Rate the following question for clarity and relevance on a scale from 0 (poor) to 10 (excellent):
> Question: [question]
> Respond with a single integer.

**3. Answering**
Prompt:
> Answer the following question as clearly and concisely as possible:
> Question: [question]

**4. Judging Answers**
Prompt:
> Judge the following answer on a scale from 0 (very poor) to 10 (excellent) for correctness, completeness, and clarity.
> Answer: [answer]
> Respond with a single integer.

**Model:**
- Default: `gpt-3.5-turbo`
- Configurable via `openai_model` in `config.yaml`
# Humanity's Last Arena

Inspired by Charles Darwin, the best measure for excellence is competition. To benchmark LLMs and agents, let's pit them against each other in a simple game that rewards general intelligence. 


## Rules
- Played as tournament, minimum 3 players (better: minimum 5)
1. With a minimal seed prompt, every player (model/agent) is asked to generate 100 questions. The seed prompt should specify required categories (e.g., math, ethics, logic, etc.) to ensure question diversity.
2. All questions are then rated by all players except their author, on clarity and relevance (blind, anonymized). You never judge the quality of your own questions. Scores are normalized so each judge awards an average of 5 points. Treatment of low-quality questions (e.g., weighting by quality score or filtering out the bottom third) is to be determined and may be adjusted based on experimental results.
3. Then every player is asked to answer all remaining questions.
4. Then every player is asked to judge all answers (excluding their own) on a scale from 0-10. Judging is blind: answers are anonymized so judges do not know which player/model wrote them.
5. All scores are normalised so that every judge awards 5 points on average.
6. Each answer then receives the average of all scores. (Keep mean and std, maybe we can use std later too.)
7. Then each player receives a score that is equal to the average score across all their answers.

**Development mode:** For testing and development, drastically reduce the number of players, questions, and token limits (e.g., 2–3 players, 3–10 questions each, 50–100 tokens per answer/judgment). This allows for fast, low-cost iteration and running hundreds of tests without significant expense.
# Backlog / Future Ideas

- Diversity bonus: Reward players for generating diverse questions or answers, possibly using clustering or semantic similarity metrics.
- Meta-questions: Allow some questions to be about the process or strategy itself, testing meta-cognition.
- Adversarial rounds: Occasionally allow players to submit “trick” questions to test robustness.
- Explainability: Ask judges to provide short rationales for extreme scores (0 or 10), which can be analyzed for insight.
- Audience participation: Allow external users to judge a subset of answers for a “public opinion” score.
- Leaderboard & progression: Track performance over multiple tournaments to see improvement or consistency.
- Automated cheating detection: Use statistical analysis to flag suspicious scoring patterns (e.g., collusion).
 - Varying compute costs: Run experiments with different compute/token budgets to analyze scaling effects.
