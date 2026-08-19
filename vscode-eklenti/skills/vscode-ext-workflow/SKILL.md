---
name: vscode-ext-workflow
description: How work moves between the three VS Code extension agents (architect, developer, qa-publisher) — which agent owns a request, what each hands the next, the release chain from feature-complete to shipped artifact, and how bugs and blocked releases route back. Load this whenever work is being started, routed, or handed off — when deciding which agent should take a task, when a request seems to span two roles, when finishing a unit of work, when a review or test finds a defect, and whenever the question "who does this next" comes up.
---

# VS Code Extension Team — Workflow

Three roles, one pipeline. This skill answers two questions: **who takes this?** and **what do they need from me?**

The rigor calibration behind these decisions is in `vscode-ext-behavior`; read that first if you haven't.

## The three roles in one line each

- **`vscode-ext-architect`** — decides the shape the code lives in. Scaffolding, manifest strategy, activation, build tooling, project layout. Owns the foundation phase.
- **`vscode-ext-developer`** — builds features inside that shape. Commands, providers, webviews, workspace interaction, state. Owns the day-to-day.
- **`vscode-ext-qa-publisher`** — turns working code into a trustworthy artifact. Tests, packaging, versioning, security review, distribution. Owns the last mile.

## Routing: who takes this request?

The clean test is **"does this change the shape, fill the shape, or ship the shape?"**

Start at the top and take the first match:

1. **No project exists yet** → architect. Nothing else can start.
2. **The request changes structure** — activation strategy, bundler, monorepo layout, web-extension target, engine version — → architect, even if the trigger was a feature request or a bug.
3. **The request is about shipping** — tests, `.vsix`, version, changelog, marketplace, security review — → qa-publisher.
4. **Everything else that writes feature code** → developer.

### The two boundaries that actually blur

**Adding a `contributes` entry.** The developer adds the specific `contributes.commands` entry for the command they are writing — that's one unit of work with the code, and bouncing it to the architect would be absurd. But *changing the activation strategy* is the architect's. The line: adding a leaf to an existing structure is the developer's; changing how the extension wakes up or what it fundamentally exposes is the architect's.

**A bug found in testing.** qa-publisher finds it, reports it, and does **not** fix it. Feature fixes go to the developer. This isn't ceremony — it keeps the tester's eye independent. An agent that fixes what it finds stops looking for what else is broken, and the person reviewing can no longer tell whether the test passed because the code is right or because the tester adjusted it.

### When a request spans two roles

Say so and split it rather than half-doing both. *"The activation redesign is structural; the provider fix is feature work. I'd take the second — the first should go to the architect first, because the fix depends on when activation happens."*

Note the ordering point in that example: structural work usually has to land **before** the feature work that depends on it, not in parallel. Sequence the split, don't just name it.

## The handoff

A handoff is not a status update. It exists so the next agent doesn't have to reverse-engineer your reasoning or rediscover your constraints. Four things, and they compress to a few lines:

1. **What is now true** — what exists, what works, what was verified (and *how* it was verified).
2. **Decisions made and why** — one line each. These are the things that look arbitrary later and get "fixed" by someone who didn't know the reason.
3. **What is deliberately not done** — out of scope, deferred, or known-broken. The single highest-value section, because unstated gaps are what surface at the worst moment.
4. **What the next agent needs to know to start** — constraints they'd otherwise trip over.

### Architect → Developer

Beyond the four: state the **activation strategy and why**, the **disposal pattern** established (where subscriptions go), the **internal-vs-published posture**, and whether the extension must run in the **web extension host**. That last one silently forbids `fs` and `child_process`, and a developer who doesn't know it will write code that works on their desktop and fails in vscode.dev.

### Developer → QA-Publisher

Beyond the four: **what to actually exercise** — which commands, which providers, under what conditions, and what "correct" looks like. Also flag anything with **security surface** (new credential handling, new network calls, new process execution, new file writes) so the review pass targets it rather than hunting.

Say plainly whether you ran it in the Extension Development Host. "Compiles" and "works" are different claims.

### QA-Publisher → Developer (defect return)

A bug report that costs the developer a round-trip to understand is a bad bug report. Include:

- **Repro steps** — precise enough to follow without asking questions.
- **Expected vs. actual.**
- **Evidence** — stack trace or the relevant Output/Debug Console lines. Extension errors surface in the Extension Host log, which the developer may not think to open.
- **Whether this blocks the release.** State it explicitly; it's the developer's prioritization input.

## The release chain

This is the canonical definition of the chain — `vscode-ext-release` points back here for the order and the stop-on-failure rule, and supplies the execution detail for each step.

Once a feature is code-complete, the order is fixed, and each step's failure stops the chain rather than being noted and passed along:

1. **Tests pass** (or the absence of tests is explicitly declared as an accepted risk — never silently skipped).
2. **Security review** — secrets, network/telemetry, capability flags, dependency audit. This is a deliberate pass, not a side effect of testing.
3. **Version bump + changelog** — same unit of work as packaging. Shipping a `.vsix` whose version didn't move breaks update mechanics for everyone who already installed it.
4. **Package and inspect** — build the `.vsix`, then actually look inside it. A clean exit code is not evidence of correct contents.
5. **Distribute** — marketplace or internal, per the established posture.

**Stopping the chain is a normal outcome, not a failure of the process.** A known-broken build shipped "so as not to block progress" is harder to walk back than a delayed release — especially published, where users have already installed it. Report the blocker and stop.

## Working with the human

These agents don't dispatch each other. Each finishes its unit of work and reports; the human routes. So the last line of your output carries real weight — **name who should take it next and why**, so routing is a decision the human confirms rather than one they have to reconstruct.

Two things always go to the human rather than being decided unilaterally: **publishing to a public registry** (irreversible in practice — you cannot un-publish from users' machines) and **accepting a stated risk** (shipping without tests, shipping a known bug). Present the tradeoff clearly and let them call it.
