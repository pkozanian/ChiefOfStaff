---
name: critique-loop
description: "Run a specialist reviewer in a loop until it has nothing left to say: pre-warm the evidence, critique, triage, hand execution to a cheaper model, re-verify, repeat. Use when asked to review something until it's clean, run a critique loop, or iterate with a specialist agent to exhaustion."
---

# /critique-loop

Drive a specialist subagent through **assess → plan → implement → re-assess** until it reports nothing
left worth saying. One review pass finds the obvious; a loop finds what the fixes *break*.

```
/critique-loop brain-experience-author brain/  # voice, until clean
/critique-loop brain-rigor-critic brain/       # coherence, until clean
/critique-loop <agent> <target>
```

## Read First

The target surface, the specialist's own file (`.claude/agents/<agent>.md`) for its lenses and
boundaries, and `AGENTS.md` — the house rules a recommendation has to fit within.

**Get the principal's opt-in first.** A thorough critic runs 10-20 minutes per round and several
rounds is normal. Say roughly what it will cost before starting.

## The loop

### 0. Pre-warm — before *every* round, not just the first

**The highest-leverage step and the easiest to skip.** A critic that assembles its own evidence spends
its budget on setup and reaches judgment with little left. Run `python3 tests/run.py`, collect the
files in scope, hand over **paths, not prose**, and say outright: *"the evidence is gathered, do not
build a harness"* — critics default to building one.

**Kill stale infrastructure first.** Leftover servers from earlier rounds are not merely untidy: one
served a critic an *old copy* of the page and silently invalidated its entire first pass.
`pgrep -f http.server` and clear them. Prefer a harness that owns and kills its own server.

### 1. Critique

Dispatch the specialist read-only. Require:
- **Severity ranking** (HIGH / MEDIUM / LOW) **including taste findings**, labelled `LOW (taste)`.
  Taste is why you hired a specialist; let it speak, and let the principal weigh it.
- **`file:line`, why it falls short, and an exact fix** — replacement text, not a direction.
- **An explicit termination phrase**: *"If you have nothing left at any severity including taste,
  reply with exactly NOTHING FURTHER and nothing else."* Without a defined exit, a critic will always
  find something and the loop never ends.
- **From round 2 on**: list what was applied, ask it to **verify those landed as intended** and to
  flag **anything the fixes introduced**.
- **Ask what it couldn't observe**, and fold the answer into the next round. This is how the loop gets
  sharper instead of just longer.

### 2. Triage — your job, not the critic's

Apply the unambiguous ones. **Route genuine forks to the principal** (AskUserQuestion) — a fork is one
the critic itself flags as a trade-off, or one that changes identity or direction; two or three per
loop, batched, not one per round. **Decline things with reasons** and say so in the next prompt so
they aren't re-raised. A good critic will tell you when *not* to do something; honour that.

### 3. Implement — hand off to a cheaper model

Dispatch a `general-purpose` agent with `model: sonnet`. Give it the **exact** fixes, numbered, plus
the invariants it must not break, an explicit **do-not-touch** list, *"if something conflicts with
what you find, stop and report rather than improvising"*, and a **report contract**: every item
applied or skipped-with-reason, plus the verification commands run.

Verify that report rather than trusting it. One agent stated a file didn't reference another when it
did — the fix was fine, the claim wasn't.

### 4. Re-verify, then loop

Re-run the checks and re-read what changed: the specific thing this round was meant to fix, and that
nothing global regressed. **Expect your own fixes to break something** — in one loop, round 2's fix
introduced a defect only round 3 caught. That regression is the loop's whole justification.

Stop when the critic returns the termination phrase. Two or three rounds is common; six is not absurd
for a surface with many states.

## Cross-cutting

- **Every round gets fresh evidence.** Never let a critic judge a stale copy.
- **Cover all the states, not the convenient ones** — for a prompt corpus, every host and every entry
  path. States nobody exercises are where findings hide.
- **Watch for the critic being wrong.** One predicted a change would read badly, then judged the
  result and withdrew the concern. Ask it to check its own predictions.
- **Land it as one PR** whose commit message says what the loop found *and* what you deliberately
  declined. The declines are as informative as the fixes.

## Output Habit

Rounds run, findings applied, the termination signal, and — most usefully — **the two or three
findings that would have shipped otherwise**. Note anything the loop could *not* judge: it optimises
against checks and a critic's taste, not against a human actually using the thing.
