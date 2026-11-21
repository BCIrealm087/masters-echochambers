# The prior hashtag-network study

The researcher supplied Revision 1 of *Political Hashtag Networks and Polarization in Brazil: A Machine Learning Analysis on Social Networks*. The figures and counts below are reported in that manuscript. This note records the version used at project setup and the parts relevant to the master’s research.

## What the graphs measured

| Component | What the manuscript reports | Location |
| --- | --- | --- |
| Collection and subset | ITED-Br contains 282 million posts. The study used posts and reposts from 3 October 2022 inclusive to 31 October exclusive. Separate queries covered Lula and Bolsonaro, including nicknames. | §§3.1–3.2, pp. 6–7 |
| Graph construction | A node represents a normalized hashtag. Two hashtags are connected when used together in a post. The edge weight counts co-occurrences. The Lula graph had 6,252 nodes and 163,474 edges. The Bolsonaro graph had 3,728 nodes and 156,654 edges. | §4, Fig. 2, p. 10 |
| Stance classification | Three political scientists assessed hashtags relative to each candidate. Consensus yielded 409 labeled seeds for Lula and 404 for Bolsonaro. Gaussian Fields and Harmonic Functions (GFHF) propagated pro, anti and neutral/undefined labels over the hashtag graph. | §§3.2–3.4.2, pp. 7–9 |
| Account score | For each candidate query, the study subtracted the number of anti-candidate hashtags an account used from its number of pro-candidate hashtags, then divided by its total hashtag count. The reported distribution included accounts with at least ten posts. | §4, Eq. 1 and Fig. 1, p. 9 |

One detail matters for future replication. Section 3.2 describes selecting the 500 most frequent hashtags per list for manual labeling. Section 3.4 describes a random sample. Record that discrepancy until the original selection procedure can be checked.

## What carries into the master’s research

The paper reports a dense central cluster and smaller interconnected sets of hashtags in both graphs. It offers themes and groups of users as possible explanations for why tags appear together (§4, pp. 10–12). Its limitations section notes that a hashtag-based sample can overrepresent partisan messaging and that the analysis omitted signals such as full text and information propagation (§7, pp. 16–17).

These results give the project a baseline for studying campaign vocabulary. Two accounts can use the same slogan without ever exchanging information. A study of echo chambers among accounts therefore needs to identify the people or accounts in each group and specify the observations that would support selective circulation or interaction. The choice of graph, evidence and validation procedure remains open.

## Source record

- Supplied file `HSSC_Political_Hashtag_Networks_and_Polarization_in_Brazil__Revision_1_.pdf`, 24 pages.
- SHA-256 of that revision is `90e0b4e7bc50b8511d367a982e61630c328b1ab28692b882cdba4d56223b5757`.
- The manuscript identifies ITED-Br in §3.1 and cites its construction paper as reference 14. [Interfaces dataset repository](https://github.com/Interfaces-UFSCAR/ITED-Br)
