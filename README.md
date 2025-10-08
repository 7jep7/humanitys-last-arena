# Humanity's Last Arena

Inspired by Charles Darwin, the best measure for excellence is competition. To benchmark LLMs and agents, let's pit them against each other in a simple game that rewards general intelligence. 


## Rules
- Played as tournament, minimum 3 players (better: minimum 5)
1. With a minimal seed prompt, every player (model/agent) is asked to generate 100 questions. The seed prompt should specify required categories (e.g., math, ethics, logic, etc.) to ensure question diversity.
2. Then every player is asked to answer all questions.
3. Then every player is asked to judge all answers (excluding their own) on a scale from 0-10. Judging is blind: answers are anonymized so judges do not know which player/model wrote them.
4. All scores are normalised so that every judge awards 5 points on average.
5. Each answer then receives the average of all scores. (Keep mean and std, maybe we can use std later too.)
6. Then each player receives a score that is equal to the average score across all their answers.
7. Compute constraints: To ensure fairness, we limit compute costs (e.g., tokens or API cost). For example: question generation (single seed prompt, max 10,000 tokens total), answering (max 500 tokens per answer), and judging (max 100 tokens per judgment). These limits are configurable.
# Backlog / Future Ideas

- Diversity bonus: Reward players for generating diverse questions or answers, possibly using clustering or semantic similarity metrics.
- Meta-questions: Allow some questions to be about the process or strategy itself, testing meta-cognition.
- Adversarial rounds: Occasionally allow players to submit “trick” questions to test robustness.
- Explainability: Ask judges to provide short rationales for extreme scores (0 or 10), which can be analyzed for insight.
- Audience participation: Allow external users to judge a subset of answers for a “public opinion” score.
- Leaderboard & progression: Track performance over multiple tournaments to see improvement or consistency.
- Automated cheating detection: Use statistical analysis to flag suspicious scoring patterns (e.g., collusion).
 - Varying compute costs: Run experiments with different compute/token budgets to analyze scaling effects.
