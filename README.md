# Echo chambers in Brazil’s 2022 presidential election

This Computer Science master’s project studies whether groups of accounts found in Twitter data collected by Interfaces during Brazil’s 2022 presidential election continue to amplify sources within their own group in a later period. The source is the Interfaces Twitter Elections Dataset (ITED-Br). The earlier manuscript reports 282 million posts in the parent collection. Each analysis in this project will describe the subset it actually uses.

The structural study builds a directed repost graph and tests whether groups learned earlier predict whose work accounts amplify later. It measures excess internal reposting against a reference that preserves sharer activity and original-post popularity within day and collection context. A separate prediction comparison measures what group membership adds beyond prior sharing relationships.

The first circulation extension compares which distinct originals groups amplify. The priority language extension tests whether recurring cultural references in Brazilian Portuguese describe those groups or improve prediction after accounting for topic and stance. It uses the comparison between members’ own writing and what they amplify about Lula and Bolsonaro. This connects the earlier hashtag study to an independent test of how particular ways of speaking recur across people and channels. Political alignment, opportunities to share opposing material, and trust each require the corresponding evidence.

The October coverage audit established that the recorded actions can support a chronological pilot. M3 is the active empirical study, with discovery and holdout evaluation governed by its registered protocol. [Coverage audit](docs/reports/m2-repost-coverage-audit.md) · [M3 protocol](docs/reports/m3-repost-pilot-specification.md)

## Working documents

| Document | What to find there |
| --- | --- |
| [Research progress](STATUS.md) | Current milestone, active task, evidence of completion and dated handoffs |
| [Integrated thesis direction](docs/reports/thesis-direction-synthesis.md) | Research questions, prioritization, execution sequence and decisions for the later studies |
| [Computational pipeline](docs/reports/thesis-computational-pipeline.md) | Event reconstruction, discovery, held-out evaluation and extension procedures |
| [Project instructions](AGENTS.md) | How to develop, document and archive work in this repository |
| [What counts as echo-chamber evidence?](docs/reports/reflexive-report-8.md) | Research questions, competing definitions and the evidence required for each interpretation |
| [Prior study](docs/prior-study.md) | The earlier hashtag graphs, stance labels and limits on their interpretation |

The Interfaces team maintains the [ITED-Br dataset repository](https://github.com/Interfaces-UFSCAR/ITED-Br).
