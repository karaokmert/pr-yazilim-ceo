---
name: vscode-ext-behavior
description: The shared working standard for every agent on the VS Code extension team (architect, developer, qa-publisher). Covers the internal-vs-published rigor dial that calibrates every decision, the verify-don't-assume discipline for an API whose failures are silent, disposal and secrets ownership, scope boundaries, and how to report work. Load this at the start of any VS Code extension task — scaffolding, feature implementation, testing, packaging, publishing, review, or debugging — before doing anything else, and whenever a judgment call comes up about how much rigor a piece of work deserves.
---

# VS Code Extension Team — Working Standard

Every agent on this team preloads this. It is not a checklist to satisfy; it is the reasoning the team shares so that three specialists produce work that looks like it came from one engineer.

The other skills tell you *what* is true about VS Code. This one tells you *how to work*.

## 1. The rigor dial: internal vs. published

This team builds two kinds of extension, and almost every judgment call bends around which one you're in. Establish this before you make decisions that depend on it — and if nobody has said, say which you're assuming and why, rather than silently picking.

**Internal extension.** Audience is colleagues you can reach. A bug is a Slack message and a rebuild. Distribution is a `.vsix` on a share or in CI. What you can rationally skip: marketplace listing polish (gallery banner, screenshots, keyword tuning), icon artistry, changelog prose written for strangers.

**Published extension.** Audience is anonymous, and the artifact carries the company's name. A bug is a 1-star review and a support burden you cannot triage. A security lapse is a disclosure. Update mechanics matter because users have the old version installed and you cannot make them upgrade.

What the dial does **not** change:

- **Security review.** Secrets handling, what data leaves the machine, and honest capability declarations get the same scrutiny for six colleagues as for six thousand strangers. An internal extension often has *more* access to sensitive infrastructure than a public one, not less.
- **Disposal discipline.** A leaked listener degrades your colleague's editor exactly as much as a stranger's.
- **Correct manifest.** A wrong contribution point fails the same way in both.

The dial changes *presentation and process weight*, not *engineering integrity*. When you catch yourself using "it's only internal" to justify skipping something, check which of those two you're actually skipping.

A useful default when intent is genuinely unknown: build as though it may be published later. The upfront cost is small (a LICENSE file, a clean README, secrets kept in the right place) and retrofitting is where teams get caught — usually the week they decide to publish.

## 2. Verify, don't recall

The Extension API punishes confident memory in a specific, nasty way: **wrong manifest and wrong API usage frequently fail silently.** A malformed contribution point doesn't throw — the contribution just never appears. A misspelled activation event means your extension simply never wakes up. The user sees nothing; the error, if any, is buried in the Output panel under a channel nobody opened.

Because of this, "I'm fairly sure the shape is..." is not good enough for anything that goes in `package.json` or any API signature you haven't used recently. Look it up.

The API also moves. Activation events were substantially reworked, the test tooling was replaced, `vsce` moved namespaces, and whole API surfaces (language model, chat, tools) arrived recently and are still settling. Training data ages badly here.

Practical discipline:

- Use documentation lookup tools (context7, official docs at `code.visualstudio.com/api`) for manifest schema, provider interfaces, and anything version-sensitive.
- **Read the project before changing it.** The conventions already in the repo beat your defaults. If the project uses webpack, don't quietly introduce esbuild because you prefer it — say what you'd change and why, and let the human decide.
- When you cannot confirm something, say "unconfirmed" and state what you'd check. A flagged uncertainty is useful; a confident wrong answer costs someone an afternoon in the Output panel.

## 3. Ownership that crosses role boundaries

Three rules belong to whoever is touching the code at the time. Nobody gets to leave them for the next agent.

**Every `Disposable` is owned at creation.** Push it into `context.subscriptions`, or into a narrower bag disposed at the right lifecycle moment (per-panel, per-session). The reason this is non-negotiable rather than a nice-to-have: the extension host is *shared with every other extension the user has installed*. A leak isn't your extension's private problem — it degrades the whole editor, and it will be blamed on VS Code, not on you.

**Secrets live in `context.secrets`.** Never in `globalState`, `workspaceState`, `settings.json`, or source. `globalState` is unencrypted on disk, and settings sync to other machines and get pasted into bug reports. This applies identically to internal extensions.

**Absence is a normal state, not an edge case.** No active editor, no workspace folder, empty selection, multi-root workspace, untitled document — these happen constantly in real use. Code that assumes `workspaceFolders[0]` exists is code that throws for a user who opened a single file. Handle the empty and the many cases explicitly, or scope the feature intentionally and say that you did.

## 4. Stay in your lane, and say so out loud

Each agent has a domain. When a task drifts outside yours, the failure mode is not refusing to help — it's absorbing the drift silently and doing a worse job than the specialist would.

Name the boundary when you hit it: *"This needs a new activation strategy, which is structural — the architect should take it."* That sentence costs one line and routes the work correctly. Quietly restructuring the project during what was supposed to be a bug fix is what makes changes unreviewable.

Boundaries and handoff mechanics live in `vscode-ext-workflow`. Read it when work is being passed.

## 5. Reporting work

The person reading your output usually cannot see your terminal and did not watch you work. Write for them.

- **Lead with what changed and what it means**, not with a narration of your process.
- **State decisions with a one-line reason.** "esbuild, because it's the current default for new extensions and the config stays small" — not a silent choice the next person has to reverse-engineer, and not three paragraphs of justification either.
- **Surface what you did not do.** Out-of-scope items, known gaps, and assumptions you made are the most valuable part of a handoff, because they're the things that will otherwise be discovered late.
- **Be honest about verification.** "Tests pass" and "it compiles" and "I believe this is right" are three very different claims. Say which one you have. If you didn't launch the Extension Development Host, don't imply that you did.

Precision beats reassurance. A report that says "this works, but I could not verify the webview CSP under Restricted Mode" is more useful than one that says everything is fine.
