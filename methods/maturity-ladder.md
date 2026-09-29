# Application-Maturity Ladder (D3)

Six levels. A work sits at the **highest level whose observable test it passes**,
based on what the paper itself reports (not aspirations in the conclusion).

| Level | Value | Observable test |
|---|---|---|
| 1 | `benchmark-research` | Evaluated only on ML metrics against a benchmark; no domain party or workflow named. |
| 2 | `domain-research` | Addresses a named Earth-science/domain question; results interpreted in domain terms, but no user or workflow in the loop. |
| 3 | `workflow-relevant` | Explicitly maps outputs onto an existing operational workflow's inputs (the workflow is named), without a built system. |
| 4 | `decision-support-prototype` | A working system a domain user can query to support a decision; demonstrated on real cases; not in routine use. |
| 5 | `operational-prototype` | Running in or beside a real operational environment on live/recurring data, in trial with the operating organization. |
| 6 | `deployed` | In routine operational use; the paper/system documentation states operational adoption. |

Rules of thumb:
- A benchmark paper *about* disasters is level 1, not a disasters application —
  the domain tag records the topic; maturity records the use.
- "Could be used by first responders" (future tense, no system) caps at level 2;
  a named workflow mapping raises it to 3.
- When the abstract can't distinguish 4 vs 5, characterize as the lower level
  and note the ambiguity — never round up.
