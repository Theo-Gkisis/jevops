# jevops

AI-powered log triage for DevOps — JEV flags the noise, Claude explains the root cause.

JevOps ingests logs from your services, uses [JEV](https://typesafe.ai) to cheaply flag and
cluster anomalies at scale, then has Claude generate a plain-language root-cause explanation
for each unique issue — so you go from raw log noise to actionable findings in seconds.

## Status

Milestone 1 in progress: local log parsing, clustering, and CLI report — no AI calls yet.
JEV and Claude integration land in later milestones.

## Usage (once Milestone 1 lands)

```bash
jevops analyze sample_logs/app.log
```
