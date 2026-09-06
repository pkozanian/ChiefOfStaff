---
name: integration-hosts
description: The agent tools Chief of Staff runs on (Claude Code, Codex) and how each host's plumbing maps.
type: role
---

# Hosts (which tool Chief of Staff runs on)

Chief of Staff is **one folder** — `brain/` (shipped) + `memory/` (this principal) — that runs on more than
one **agentic host**. Every supported host is **file-based and local**: the agent reads and writes
the same `memory/` tree on disk, so the structured memory, the `memory/overrides/` overlay, and the
**confidential code-name registry** work identically. Only the *plumbing* (boot file, connectors,
scheduled briefs, command invocation) differs.

## Supported hosts

| Host (what you are) | Runs inside (what the principal installed) | Boot file | Connectors | Scheduled briefs | Commands |
|------|------|-----------|------------|------------------|----------|
| **Claude Code** | the **Claude** desktop app | `CLAUDE.md` → `@AGENTS.md` | **Connectors** (＋ / claude.ai) | **Routines** (routine tools) | `/onboard`, `/routines` |
| **Codex** | the **ChatGPT** desktop app | `AGENTS.md` (direct) | **Plugins** (Install) | **Scheduled** | plain requests ("onboard me") |
| *Any other `AGENTS.md`-aware tool* | that tool's app | `AGENTS.md` (direct) | MCP / that tool's connectors | that tool's scheduler / a headless run + cron | plain requests / that tool's commands |

**Which name to use, and when.** The two columns above are not interchangeable:

- **Branch on the host name** (`Claude Code`, `Codex`) — it is what you detect, what `memory/meta.md`
  records as `host:`, and what every fork below keys off.
- **Say the app name** ("the Claude desktop app", "the ChatGPT desktop app") **whenever you address the
  principal.** They installed an app; "Codex" and "Claude Code" are your names, not theirs, and a
  principal who reads "open the folder in Codex" may not know what you are referring to.

Where you are naming a UI path, name the app and then the path, since the wording belongs to the app:
*"in the ChatGPT desktop app: New chat → Choose Project → Add folders ChatGPT can read"*.

**Local folder only.** Point the tool at *this folder* (Codex: **New chat → Choose Project → Add folders
ChatGPT can read → this folder → Create Project**). A **cloud** session clones the repo honoring
the principal's `memory/`
would be **absent** → always run Chief of Staff **locally**.

## Detect + record the host
Early in onboarding (or on first run), note which host you're on and record it in `memory/meta.md`
as `host: claude-code | codex | other`. Use it to branch the guidance below. If you can't
tell, ask the principal once.

**Also infer the machine's OS and default browser — don't ask.** Where there's an execution surface,
detect them and record alongside `host:` as `os: macos | windows | linux` and
`browser: chrome | edge | brave | arc | safari | firefox | other`. They decide which browser extension
to recommend (below). Read-only, best-effort, and quiet — never surface the commands:

| | OS | Default browser |
|---|---|---|
| **macOS** | `sw_vers -productName -productVersion` (or `uname -s` → `Darwin`) | the `https` handler in LaunchServices: `defaults read com.apple.LaunchServices/com.apple.launchservices.secure` → the `LSHandlerRoleAll` next to `LSHandlerURLScheme = https` (e.g. `com.google.chrome`); fall back to what's in `/Applications` |
| **Windows** | `ver` | `reg query "HKCU\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice" /v ProgId` |
| **Linux** | `uname -a` | `xdg-settings get default-web-browser` |

If there's **no execution surface**, a command fails, or the result is ambiguous, **ask once** (same
rule as the host above) — never guess, and never claim a browser you didn't verify.

## How each capability maps
- **Memory** — identical everywhere: local `memory/` files you read and write (see
  `brain/schemas/memory-file.md`, `brain/schemas/capture-rules.md`). No host downgrades this.
- **Boot** — **`AGENTS.md` is the entry point** (a thin dev-vs-use router), read directly by Codex (in the
  ChatGPT desktop app) / other AGENTS.md-aware tools, and by **Claude Code** via a one-line `@AGENTS.md`
  import in `CLAUDE.md`.
  It routes to **`CHIEFOFSTAFF.md`** (the persona + boot protocol — the source of truth for *using* Chief of Staff)
  and runs its boot protocol.
- **Connectors** — see `brain/integrations/connectors.md`: **Claude Connectors** on Claude Code;
  **ChatGPT Plugins** (install from the Plugins tab — no MCP setup) on Codex. Consume them
  capability-first and **degrade gracefully** when one isn't present.
- **Connector/plugin discovery** — the shared, host-neutral contract lives in
  `brain/integrations/connectors.md`; read it first. Don't assume Codex's plugin-control tools
  exist in Claude, or that Claude's `/mcp` status surface exists in Codex — host logic must not
  leak across hosts:
  - **Claude Code/Desktop:** use **`/mcp`** (or connector status) when tools seem missing —
    distinguish **`connected`**, **`needs-auth`**, **`failed`**, and **`pending`**; retry discovery
    with the **connector name + expected MCP action names**; connector tools may need a **fresh
    session** or delayed exposure; don't tell the principal to **reconnect** unless status
    explicitly shows auth/connection failure; **prefer the connected MCP/connector over browser**
    or computer-use.
  - **Codex:** use **deferred** tool discovery when plugin actions aren't initially
    present; search by the **exact plugin name and canonical action names** (a "**canonical
    action**" is the provider's real action identifier, not a paraphrase); inspect **plugin
    permissions** or connection when installed but actions are missing — an **installed plugin
    skill does not guarantee** its tools have surfaced; **avoid the browser** until plugin discovery
    and status checks are complete; **never infer that a blocked** Google **login** means the Gmail
    or Calendar plugin is **disconnected** — check plugin/connection status explicitly first.
  - **Resuming a flow after discovery.** When discovery confirms a connector that was missing is now
    live — after a fresh session (Claude Code) or once deferred tool discovery resolves (Codex) —
    don't just silently note it worked: resume whatever the principal was mid-flow on that depended on
    it. The clearest case is onboarding's step-2 history bootstrap, held via `current_step` for exactly
    this — see `brain/onboarding/flow.md`.
- **Scheduled briefs** — see `brain/integrations/routines.md`: **Routines** on Claude Code;
  **Scheduled** tasks on Codex. Both must run **locally against this folder** to read
  `memory/`.
- **Browser control** — the **fallback offered when no connector/plugin, MCP/API, or CLI can do the
  job**, and only once discovery has actually concluded **state 6**
  (`brain/integrations/connectors.md`) — an unseen tool, or a status you couldn't check, is
  **inconclusive**, not a cue to open a browser (**prefer the connected MCP/connector over browser**).
  Rails in
  `brain/integrations/browser.md` (never types credentials — co-browse; never sends or submits without
  an explicit OK).
  - **Claude Code:** the **Claude browser extension**, matched to the principal's detected browser
    (above) — Chrome and Chromium browsers (Edge, Brave, Arc) → **Claude for Chrome**
    (**https://claude.ai/chrome**), installed once. On Safari/Firefox, **verify support there** before
    recommending it; if it isn't supported, lean on connectors/CLI or a supported browser.
  - **Codex (ChatGPT desktop):** a **built-in browser** — nothing to install. Open it when it would
    help and work the web page; ChatGPT asks before using a new site, and allowed sites, cookies, and
    history are managed in the app's settings.
  - *Any other host:* its own browser / computer-use surface, if it has one.
- **Commands** — the same set ships twice: as skills at `.agents/skills/*`, which Codex, Cursor,
  Gemini CLI, OpenCode and Copilot read, and as Claude Code slash commands at `.claude/commands/*`.
  Both delegate to the same playbook, so they cannot diverge in behavior. On a host that reads
  neither, the same actions are plain requests ("onboard me", "process these docs", "set up my
  briefs"), which the boot protocol recognizes.
- **Self-update** — where the host can **fetch a file and write into this folder** (Claude Code's
  shell; Codex's code execution), Chief of Staff can update itself in place on the principal's OK
  (`brain/integrations/updates.md`). Where it can't, updates fall back to the manual path (download
  the latest ZIP, replace `brain/`). Either way `memory/` is never touched.
- **Virtual team execution** — a specialist runs by **persona-swap** on every host: Chief of Staff loads the
  specialist's `charter.md` + the shared brain (in code names) + its `memory/` and works as it, then integrates
  (`brain/schemas/team-member.md`, `brain/playbooks/delegate.md`) — and only that: there is no
  host-specific execution path to branch on (`brain/schemas/team-member.md` → "Why there is no
  subagent projection"). **Direct interaction** is
  host-independent too: the principal asks for the specialist and Chief of Staff persona-swaps — a
  specialist is never loaded on its own (`brain/schemas/team-member.md`).

## Verify per host (fast-moving)
On a new host, confirm before relying on it: (a) the agent can **write** `memory/` files; (b) which
**boot file** it auto-loads; (c) **scheduled** briefs run **locally** (see `memory/`); (d) connectors
are available and whether they can **act** vs read-only; (e) whether it can **fetch + write files**
(for self-update, else use the manual path); (f) whether **browser control** exists and how it's
reached (extension vs built-in); (g) whether a **session-title tool** surfaces (it may be deferred) — this one moves fastest, so confirm rather than assume. If any
fails, degrade (build from memory, ask for what's missing) — never block.
