"""Study 2: which implicit requirements of realistic user requests end up in generated code.

The 11 requests and their 33 implicit requirements are in study2_tasks.yaml.

Conditions
    BARE  the one-sentence request, as a user would write it
    FULL  the same request followed by the list of its implicit requirements

The answers are whole applications, so they cannot be unit-tested. Instead, each answer is graded
by LLM judges. A judge sees the original request, the full answer and the requirements to check,
but never the prompt the model received, so it cannot tell BARE from FULL. For each requirement
it returns met / not met with a one-sentence reason, and whether the answer contains code at all.

Every answer is saved as one JSON file in results/<name>/study2/ together with all verdicts.
After each run the files are copied into results/<name>/results_study2.csv
(one row per answer, requirement and judge).

Usage
    python study2.py --name main_2 --models chatgpt,deepseek,gemini --judges chatgpt,qwen,claude --reps 3 --budget 10
    python study2.py --name main_2 --rejudge claude --budget 5   # add a judge to existing answers
    python study2.py --name main_2 --report                      # rebuild the CSV file

Models, prices, retries and the budget limit come from run.py.
"""
import argparse
import hashlib
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

import run

TASKS = run.ROOT / "study2_tasks.yaml"

JUDGE_PROMPT = """You are reviewing code written by an AI assistant for this user request:
<request>
{request}
</request>

The assistant's full answer:
<answer>
{answer}
</answer>

For each requirement below, decide whether the delivered code satisfies it. Judge only what
the code actually does. Comments, TODOs or advice such as "in production you should..." do not
count. If the code does not address a requirement, it is not satisfied.

Requirements:
{requirements}

Reply with JSON only, in this form:
{{"_code": true or false, "<ID>": {{"met": true or false, "reason": "one sentence"}}, ...}}
Set "_code" to false if the answer contains no implementation at all (for example only
questions back to the user or general advice)."""


def load_tasks():
    return yaml.safe_load(TASKS.read_text())["tasks"]


def task_hash(task):
    return hashlib.sha256(json.dumps(task, sort_keys=True).encode()).hexdigest()[:12]


def judge(judge_model, task, answer):
    """Grade one answer. Return (verdict, raw judge response, cost).

    verdict = {"reqs": {ID: {"met": bool or None, "reason": str}}, "has_code": bool or None};
    None means the judge did not return valid JSON.
    """
    ids = [r["id"] for r in task["requirements"]]
    if judge_model == "mock":
        rnd = random.Random(answer + task["id"] + judge_model)
        return {"reqs": {i: {"met": rnd.random() < 0.5, "reason": "mock"} for i in ids}, "has_code": True}, "", 0
    reqs = "\n".join(f"- {r['id']}: {r['text']}" for r in task["requirements"])
    prompt = JUDGE_PROMPT.format(request=task["prompt"].strip(), answer=answer, requirements=reqs)
    r = run.call(judge_model, prompt, run.ROOT)
    try:
        data = json.loads(re.search(r"\{.*\}", r["response"], re.S).group(0))
        verdict = {"reqs": {i: {"met": bool(data[i]["met"]), "reason": str(data[i].get("reason", ""))} for i in ids},
                   "has_code": bool(data.get("_code", True))}
    except Exception as e:
        verdict = {"reqs": {i: {"met": None, "reason": f"judge error: {e}"} for i in ids}, "has_code": None}
    return verdict, r["response"], r["cost_usd"]


def generate(a, tasks, out):
    judges = a.judges.split(",")
    for model in a.models.split(","):
        for task in tasks:
            for cond in ["BARE", "FULL"]:
                for rep in range(a.reps):
                    path = out / f"{task['id']}__{model}__{cond}__{rep}.json"
                    if path.exists():
                        continue
                    prompt = task["prompt"].strip()
                    order = []
                    if cond == "FULL":
                        reqs = task["requirements"][:]
                        random.Random(f"{task['id']}{model}{rep}").shuffle(reqs)
                        order = [r["id"] for r in reqs]
                        prompt += "\n\nRequirements:\n" + "\n".join(f"- {r['text']}" for r in reqs)
                    try:
                        answer = run.call(model, prompt, run.ROOT)
                        verdicts, responses, judge_cost = {}, {}, 0.0
                        for j in judges:
                            verdicts[j], responses[j], cost = judge(j, task, answer["response"])
                            judge_cost += cost
                    except run.CallFailed as e:
                        print(f"[skipped] {path.stem}: {e}")
                        continue
                    answer.pop("code")  # judges read the whole answer, not only the extracted code
                    run.save_json(path, {"task": task["id"], "task_hash": task_hash(task), "model": model,
                                         "condition": cond, "rep": rep, "requirement_order": order, **answer,
                                         "verdicts": verdicts, "judge_responses": responses,
                                         "judge_cost_usd": judge_cost})
                    first = verdicts[judges[0]]["reqs"]
                    met = sum(1 for v in first.values() if v["met"])
                    print(f"{path.stem}: {met}/{len(first)} met according to {judges[0]}"
                          f"{' TRUNCATED' if answer['truncated'] else ''} | spent {run.SPENT['usd']:.3f} USD")


def rejudge(out, judges):
    """Add verdicts of new judges to existing answers, without generating the answers again."""
    tasks = {t["id"]: t for t in load_tasks()}
    for f in sorted(out.glob("*.json")):
        d = json.loads(f.read_text())
        missing = [j for j in judges if j not in d["verdicts"]]
        if not missing or d["task"] not in tasks:
            continue
        for j in missing:
            try:
                d["verdicts"][j], d["judge_responses"][j], cost = judge(j, tasks[d["task"]], d["response"])
            except run.CallFailed as e:
                print(f"[skipped] {f.stem} / {j}: {e}")
                continue
            d["judge_cost_usd"] += cost
        run.write_atomic(f, json.dumps(d, indent=1, default=str))
        print(f"{f.stem}: + {', '.join(missing)} | spent {run.SPENT['usd']:.3f} USD")
    save_csv(out)


def save_csv(out):
    """Rebuild results_study2.csv: one row per answer, requirement and judge."""
    reqs = {r["id"]: r for t in load_tasks() for r in t["requirements"]}
    header = ["experiment", "run_id", "timestamp", "task", "task_hash", "model", "model_id", "condition",
              "rep", "req_id", "category", "in_prompt", "judge_model", "met", "has_code", "truncated",
              "judge_reason", "input_tokens", "output_tokens", "cost_usd", "judge_cost_usd", "seconds", "json_file"]
    rows = []
    for f in sorted(out.glob("*.json")):
        d = json.loads(f.read_text())
        for j, v in d["verdicts"].items():
            for rid, r in v["reqs"].items():
                rows.append([d["experiment"], d["run_id"], d["timestamp"], d["task"], d["task_hash"], d["model"],
                             d["model_id"], d["condition"], d["rep"], rid, reqs[rid]["category"],
                             d["condition"] == "FULL", j, "" if r["met"] is None else int(r["met"]),
                             "" if v["has_code"] is None else int(v["has_code"]), int(d["truncated"]),
                             r["reason"], d["input_tokens"], d["output_tokens"], d["cost_usd"],
                             d["judge_cost_usd"], d["seconds"], f"study2/{f.name}"])
    run.write_csv(out.parent / "results_study2.csv", [header] + rows)
    print(f"Saved {out.parent.relative_to(run.ROOT)}/results_study2.csv ({len(rows)} rows)")


def main():
    p = argparse.ArgumentParser(description="Study 2: implicit requirements graded by LLM judges.")
    p.add_argument("--name", default="test", help="experiment name, results go to results/<name>/study2/")
    p.add_argument("--models", default="mock", help="models that answer, comma-separated keys of run.MODELS")
    p.add_argument("--judges", default="mock", help="judge models, comma-separated")
    p.add_argument("--reps", type=int, default=3)
    p.add_argument("--budget", type=float, default=1.0, help="spending limit in USD for this run")
    p.add_argument("--tasks", help="only these task IDs, comma-separated")
    p.add_argument("--rejudge", help="add these judges to existing answers, comma-separated")
    p.add_argument("--report", action="store_true", help="only rebuild the CSV file")
    a = p.parse_args()
    out = run.ROOT / "results" / a.name / "study2"

    if (a.report or a.rejudge) and not any(out.glob("*.json")):
        sys.exit(f"No Study 2 results in results/{a.name}/study2. Check --name.")
    if a.report:
        return save_csv(out)
    if a.rejudge:
        run.SPENT["budget"] = a.budget
        return rejudge(out, a.rejudge.split(","))

    models = a.models.split(",") + a.judges.split(",")
    for m in models:
        run.settings(m)
    tasks = load_tasks()
    hashes = {t["id"]: task_hash(t) for t in tasks}
    if a.tasks:
        tasks = [t for t in tasks if t["id"] in a.tasks.split(",")]
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.json"):  # do not mix results of different versions of a task
        d = json.loads(f.read_text())
        if hashes.get(d["task"]) != d["task_hash"]:
            sys.exit(f"Task {d['task']} changed since earlier runs. Use a new --name.")
    run.guard_settings(out, a.models.split(","))
    run.RUN.update(experiment=a.name, out=out,
                   run_id=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-") + run.os.urandom(2).hex())
    run.SPENT["budget"] = a.budget

    log = {"study": 2, "run_id": run.RUN["run_id"], "started": run.now(), "args": vars(a),
           "script_sha": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12], "tasks": hashes,
           "models": {m: run.MODELS[m][2:] for m in set(models)},
           "settings": {m: run.settings(m)[:2] for m in set(models)}}
    try:
        generate(a, tasks, out)
        log["status"] = "complete"
    except run.BudgetExceeded:
        log["status"] = "budget_reached"
        print(f"Budget of {a.budget} USD reached. Run again to continue.")
    log.update(finished=run.now(), spent_usd=round(run.SPENT["usd"], 6))
    with open(out.parent / "runs.jsonl", "a") as fh:
        fh.write(json.dumps(log) + "\n")
    save_csv(out)
    if log["status"] != "complete":
        sys.exit(2)


if __name__ == "__main__":
    main()
