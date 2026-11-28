# Project instructions

These instructions apply throughout `BCIrealm087/masters-echochambers`, the working archive for the *Masters Degree – Echochambers* project. Start a session by reading [research progress](STATUS.md) and the material linked from the active task.

## Research scope

- Use the [integrated thesis direction](docs/reports/thesis-direction-synthesis.md) to plan new work and the registered protocol linked in [STATUS.md](STATUS.md) to execute the active study. Prioritize directed graph discovery and held-out validation, followed by item circulation and a repertoire study where coverage supports it.
- Develop computational methods for building graphs from documented subsets of ITED-Br, detecting candidate echo chambers and studying language and information circulation within and across them. Use sociopolitical interpretation to frame questions and explain what the methods can establish.
- Use the [prior study](docs/prior-study.md) as a baseline for hashtag co-occurrence and candidate-relative stance. When proposing a new graph, state what one node and one edge represent. Distinguish hashtag communities, account communities and groups defined by a stance label.
- Explain what observable evidence warrants an echo-chamber interpretation. Keep community detection and the evidence used to validate that interpretation explicit. For example, if shared hashtags define a group, finding the same hashtags within it provides no independent check.
- Treat a linguistic repertoire as a pattern of references and uses in observed communication. For tests involving language, distinguish authorship from amplification, learn features within the training period, and use independent evidence for interpretation. Keep candidate sets and scored actions comparable when attributing predictive gain to new features. Record coverage and use an untouched evaluation interval for confirmation after data-informed redesign.
- Identify the evidence behind claims about people. A repost records an act of sharing. A claim about endorsement, trust, belief or exposure needs its own justification. Preserve relevant Portuguese wording and election context when interpreting political language.

## Milestones and the research record

- Keep [STATUS.md](STATUS.md) as the single record of the current milestone and task. At task start, give the objective, status and completion condition. At meaningful checkpoints, record what changed, link the evidence, and note any blocker or open decision. At completion, date the handoff, summarize the result and update the active task.
- Archive substantive work on GitHub as it progresses. Commit the relevant documents, code or shareable results together with the tracker update. Use relative links to the evidence so a later reader can follow the history from a checkout.
- Make routine organizational decisions within the agreed scope. Record consequential choices and their rationale near the affected work. Respect the stage boundary set by the researcher. For setup, report completion before beginning another milestone.

## Roadmap execution

Unless the researcher explicitly specifies a different workflow, prioritize steps the assistant can carry out autonomously. Use available tools to do the research, analysis and verification, and use scripts when they help make repeatable work reproducible. Carry routine decisions and checks through to completion.

Include a human task only when a critical input is beyond the automated workflow’s capabilities or when credible validation requires independent human judgment. State what is needed and why, ask for the minimum input required, and continue any work that can proceed independently.

## Large data runs

- Treat performance as a design requirement for scripts that process substantial data. Time a representative workload on the Ubuntu research host that stores ITED-Br, identify bottlenecks, and estimate the full run cost. Take available CPU cores, RAM, disk space, storage throughput, and other active workloads into account when choosing worker counts, memory limits, and batch sizes.
- Attempt and benchmark feasible changes that could bring a run from tens of hours down to a few hours. Consider reusing expensive intermediate work, reducing scans and data movement, and parallelizing independent work within host limits. Check that optimizations preserve the registered method and reproducibility. Record measured gains and consequential tradeoffs with the run.
- Before launching a job expected to take several hours, profile representative inputs, including plausible worst-case stages or strata. Consider algorithmic changes and implementation options such as compact data layouts, cache-friendly access, batching independent work, CPU SIMD, and GPU offloading where supported by the host. Benchmark promising options against the current implementation using end-to-end throughput for completed work, including memory use, transfer costs, and rejected attempts where relevant. Verify that the chosen optimization preserves the required results or sampling distribution.
- Archive measured performance in the relevant report under `docs/reports/` as meaningful batches or stages finish, with a final summary at job completion. Record workload size, host and worker settings, elapsed time, throughput, observed bottlenecks, and the effects of attempted optimizations or interruptions where relevant. Distinguish measured results from runtime estimates and link shareable evidence from `STATUS.md`. Review comparable past runs when designing or sizing a new job and use their measurements to inform runtime estimates, implementation choices and scheduling.
- Prefer resumable execution when the overhead is modest. Save completed work in independently verifiable units, such as batches or seed runs, and reuse it after an interruption when the inputs and settings match. Write outputs atomically so partial files can be retried safely. For unattended jobs, prefer a launch method that can survive SSH or Codex disconnection and saves progress and errors locally.
- When a long background job will run while Codex or agents wait or work elsewhere, consider a practical way to notify the researcher on completion or failure. Choose a mechanism suited to how the researcher accesses the host and use an existing authorized notification channel when available. Include the job status and the location of the local log or results.

## Research reports for the advisor

Keep a dated Markdown report in `docs/reports/` for each substantive research milestone. Update it when an analysis changes a conclusion, a methodological decision affects the study, or an unresolved question needs discussion. Link the report from [STATUS.md](STATUS.md) and keep routine task updates in the tracker.

Write for a master’s advisor who knows the field and may be reading the report without the repository or conversation at hand. Give it a descriptive title, the milestone and the date. Open with the research question, the main finding or decision so far, and why it matters for the thesis. Organize the body around the following questions, adapting the depth to the work completed.

1. **What did we do, and why?** Describe the relevant work and the reasoning behind consequential choices. For empirical work, identify the dataset slice, unit of analysis and method. For a design or literature milestone, explain the alternatives considered and what informed the choice.
2. **What did we learn?** State each important conclusion alongside the evidence that supports it. Include informative negative or inconclusive results. Use a labeled table or figure when it makes a comparison easier to assess. Link to the supporting analysis or cite the relevant source.
3. **How far does the evidence reach?** Explain uncertainty, alternative interpretations and limits on generalization. For example, if a group primarily reposts its own members, report the observed sharing pattern and explain what further evidence a claim about trust would require.
4. **What follows?** Identify the next research step and any specific decision where the advisor’s feedback would help.

## Data and reproducibility

- On the Ubuntu research machine, the ITED-Br corpus is at `/data/dados/twitter/corpus`. All local user accounts can read the dataset. Read the source files in place and write analysis outputs to a separate working directory.
- Keep source extracts, tweet text, account-level records, re-identifiable intermediate files and credentials out of Git. Use `data/local/` for local research data and `runs/local/` for working outputs. Archive a description or manifest for restricted inputs and review aggregates and examples before committing them.
- For an empirical result, record the input version or snapshot, query or selection rules, time window and timezone, relevant preprocessing, graph or model settings, software version, random seed where applicable, and the command or notebook that produced it. Report the counts needed to understand exclusions and reproduce the result.
- Attribute claims from earlier work to their source. Mark decisions still under discussion and distinguish hypotheses, reproduced results and new findings. Add directories, dependencies and automation when there is concrete work for them to support.
