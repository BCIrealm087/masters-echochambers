# Project instructions

These instructions apply throughout `BCIrealm087/masters-echochambers`, the working archive for the *Masters Degree – Echochambers* project. Start a session by reading [research progress](STATUS.md) and the material linked from the active task.

## Research scope

- Develop computational methods for building graphs from documented subsets of ITED-Br, detecting candidate echo chambers and studying language and information circulation within and across them. Use sociopolitical interpretation to frame questions and explain what the methods can establish.
- Use the [prior study](docs/prior-study.md) as a baseline for hashtag co-occurrence and candidate-relative stance. When proposing a new graph, state what one node and one edge represent. Distinguish hashtag communities, account communities and groups defined by a stance label.
- Explain what observable evidence warrants an echo-chamber interpretation. Keep community detection and the evidence used to validate that interpretation explicit. For example, if shared hashtags define a group, finding the same hashtags within it provides no independent check.
- Identify the evidence behind claims about people. A repost records an act of sharing. A claim about endorsement, trust, belief or exposure needs its own justification. Preserve relevant Portuguese wording and election context when interpreting political language.

## Milestones and the research record

- Keep [STATUS.md](STATUS.md) as the single record of the current milestone and task. At task start, give the objective, status and completion condition. At meaningful checkpoints, record what changed, link the evidence, and note any blocker or open decision. At completion, date the handoff, summarize the result and update the active task.
- Archive substantive work on GitHub as it progresses. Commit the relevant documents, code or shareable results together with the tracker update. Use relative links to the evidence so a later reader can follow the history from a checkout.
- Make routine organizational decisions within the agreed scope. Record consequential choices and their rationale near the affected work. Respect the stage boundary set by the researcher. For setup, report completion before beginning another milestone.

## Data and reproducibility

- Keep source extracts, tweet text, account-level records, re-identifiable intermediate files and credentials out of Git. Use `data/local/` for local research data and `runs/local/` for working outputs. Archive a description or manifest for restricted inputs and review aggregates and examples before committing them.
- For an empirical result, record the input version or snapshot, query or selection rules, time window and timezone, relevant preprocessing, graph or model settings, software version, random seed where applicable, and the command or notebook that produced it. Report the counts needed to understand exclusions and reproduce the result.
- Attribute claims from earlier work to their source. Mark decisions still under discussion and distinguish hypotheses, reproduced results and new findings. Add directories, dependencies and automation when there is concrete work for them to support.
