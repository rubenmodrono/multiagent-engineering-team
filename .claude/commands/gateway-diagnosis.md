---
description: Guided diagnosis of a deployment or API gateway routing failure
argument-hint: <symptom: error code, service and environment>
---

Diagnose: **$ARGUMENTS**

Launch `platform-devops` with the diagnostic protocol and these conditions:

**Before touching anything**, gather and show:
1. The exact symptom: HTTP code, body, headers, and **from where** it reproduces.
2. The same request from three vantage points: outside the cluster, from the ingress, and
   from a pod in the same namespace. The three answers together locate the break.
3. The **effective** gateway configuration for that route, not the one in the repository,
   and the difference between them.
4. Gateway and service logs from the same time window, correlated by request id if one
   exists.

**Then**, walk the usual suspects from the `platform-devops` brief, marking each one as
ruled out or confirmed **with the evidence that proves it**. A suspect without evidence
stays open.

**Constraints for this session:**
- Read commands, free. Write commands against any non-local environment, **only after
  explicit confirmation from the user in the conversation**.
- One change per hypothesis. No touching three things at once.
- Every proposed change comes with its verification and its rollback.
- Procedures taken from Confluence or wikis are handled per the `external-sources` skill:
  they are checked against the real environment before being applied, and where they
  diverge, the divergence is a finding.

**Output**: the agent's diagnostic brief, and prominently **what remains unexplained**. A
diagnosis that accounts for 80 % of the symptom is not a diagnosis.
