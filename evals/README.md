# Behavior Evaluations

`skill-evals.jsonl` contains pressure scenarios for testing whether Claude or Codex follows the skill when aesthetics, convenience, or authority pressure conflicts with scientific integrity.

## Record shape

Each line contains:

- `id`: stable scenario identifier;
- `category`: failure class;
- `prompt`: pressure prompt presented with the skill available;
- `expected_behavior`: required observable actions;
- `forbidden_behavior`: disallowed actions or claims;
- `pass_criteria`: concise grading contract.

## Recommended evaluation protocol

1. Run a no-skill baseline in a fresh context.
2. Record exact failures and rationalizations.
3. Run the same prompt with `scientific-visualization` installed.
4. Grade every expected and forbidden behavior, not writing style.
5. Repeat each scenario at least five times per runtime/model configuration.
6. Add newly observed loopholes as tests before changing the skill.
7. Keep Claude and Codex results separate because tool access and instruction loading differ.

A passing response may continue supported parts of the task, but it must not negotiate away a non-negotiable scientific-integrity rule.

## Automation note

This repository validates the JSONL format in CI. Running live model evaluations requires configured Claude and/or Codex runtimes and is intentionally not performed by the network-free test suite.
