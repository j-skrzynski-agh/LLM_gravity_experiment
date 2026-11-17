#!/usr/bin/env bash
# Reruns the whole study as it was done for the paper. Already finished requests are skipped,
# so after an interruption just run the same command again.
set -euo pipefail
cd "$(dirname "$0")"

python run.py --check                                   # every reference passes, every mutant fails its own test

# Study 1: FULL + ablations, 5 models x 3 repetitions
python run.py --name main --models chatgpt,deepseek,gemini,qwen,llama --reps 3 --budget 10
# Study 1: erosion, four feature changes
python run.py --name main --models chatgpt,deepseek,gemini,qwen,llama --reps 3 --budget 10 --erosion
# Study 1: erosion, one refactoring on five modules
python run.py --name main --models chatgpt,deepseek,gemini,qwen,llama --reps 3 --budget 2 --erosion --refactor \
  --apps uploads,appointments,library,parking,gradebook

# Study 2: 3 models answer, 3 judges grade
python study2.py --name main --models chatgpt,deepseek,gemini --judges chatgpt,qwen,claude --reps 3 --budget 10

# Analysis
python run.py --name main --report
python study2.py --name main --report
python analyze.py
