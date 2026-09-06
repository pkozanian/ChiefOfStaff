---
name: onboarding-step-projects
description: Onboarding step 4 — Projects, OKRs, open decisions, confidentiality, and the team proposal.
type: role
---

# Priorities & projects → `memory/projects/`
*Render the progress bar (`Step 4/6 · Priorities & projects`; personal: `Goals & plans`).* Current
top priorities and active initiatives. **One file per project**: goal/definition of done, owner,
status, key dates. Link to the people involved.

**Checklist:** `projects`, `okrs`, `okr-critique`, `decisions`, `confidentiality`, `team-offer`.

**By mode:** *work-manager* — the **team's** projects + OKRs + the RAPID decisions below. *work-IC* —
**your own** deliverables and goals; OKRs optional (capture them lightly if they have them), and RAPID
only if they actually drive decisions. *personal* — **personal goals & plans** (a move, a trip, a
health goal, a course or side interest); **skip OKRs and RAPID entirely** — capture goals plainly and
any commitments to `memory/commitments.md`. Personal mode also **skips the confidentiality ask below
entirely** — file anything sensitive as normal private memory unless the principal explicitly asks to
code-name it. (Internally these still live in `memory/projects/` — a personal principal is just
never *told* "project"; they're "goals & plans.")

**Recommend an upload here:** a roadmap, planning doc, or OKR sheet is often richer than typing —
*"If you have a roadmap or planning doc, upload it and I'll break out the projects."* Extract each
initiative into its own file, then confirm them with the principal.

**Each of this step's asks is its own turn** — projects, OKRs (with the critique offer), open
decisions, confidentiality and the specialist proposal are separate checklist rows, not one turn's
worth. Never *"three quick ones"*, and never hang one ask off the turn that closes another: the
specialist proposal especially is its own turn, not a rider on the confidentiality wrap-up. Each
reply is material the next question should build on; asked together they get one shrug for all of
them (`flow.md` → "One topic per turn").

**Capture OKRs — and offer a critique.** Ask for the principal's (and their team's) objectives & key
results; record them to `memory/okrs.md`, then **offer to pressure-test them** (are the KRs
measurable outcomes, not activities?) per `brain/playbooks/okrs.md` — offer, don't force. **If they
accept, make the critique count — this is a moment to show chief-of-staff caliber, not run a
checklist.** Find the sharpest issue in *their actual* KRs (never a generic template) — most often a
key result that's an *activity* masquerading as an *outcome* — name it plainly and hand back the
crisp, measurable reframe on the spot, so the goal is visibly better, not just flagged. Stay honest
and constructive: one or two sharp, well-grounded catches beat a nitpicky pass over every line. *"'Ship
the redesign' is an activity — the outcome is 'cut checkout drop-off from 40% to 25%.' Want me to
sharpen the rest the same way?"* (Work mode only — personal mode skips OKRs entirely, per the "By
mode" note above.) **Always ask in work mode** — an IC who doesn't run on OKRs says so in a word;
never decide it for them. `okrs` → `done` (recorded) or `declined` (they don't use them — note it);
`okr-critique` → `done` / `declined`, or `n/a` (note: no OKRs captured).

**Capture open decisions.** Ask what **big decisions** they're weighing right now. **When one
surfaces, react first, log second.** Give one sharp, grounded beat — name the real tradeoff, or ask
the one pointed question that reframes it — before you file it; this is a taste of thinking with
them, not a full brief, so keep it to a single line, and only offer it when it's genuinely useful,
never forced on a trivial item. Then log it to `memory/decisions.md` with **RAPID** roles where
known (leave the decider blank and ask if unclear) — see `brain/playbooks/decisions.md` — and note
you've logged it and can go deeper anytime with the full `brain/playbooks/decision-brief.md`
treatment. Mention you'll track decisions this way going forward. *"The real question isn't build
vs. buy — it's whether you can afford to wait a quarter for either. Want me to work that up
properly later? Logging it for now."* Row `decisions` → `done` (logged, or "nothing big right now"
noted).

**Work-IC: no OKR, no live decision — offer a sounding-board beat anyway.** OKRs are optional for an
IC and RAPID only applies if they actually drive decisions, so a "nothing big right now" answer to
both prompts can leave an IC with no think-with-me moment at all — don't let it. If neither surfaces
anything, offer **one** sharp, grounded observation on their stated deliverables or priorities instead
— a sequencing risk, a week that looks over-committed, a dependency that's about to bite. Same honesty
rail as the reaction above: only offer it if it's genuinely useful given what they've actually said;
skip it gracefully if their answers are too thin for anything specific. Keep it brief, one line. *"Q3
and the migration land the same week on what you've described — worth flagging now, or just noting it
and moving on?"*

**Personal mode: react first, then log — no RAPID needed.** Personal mode skips the OKR critique and
RAPID roles above (per the "By mode" note), which would otherwise leave it without a sounding-board
moment — so give it its own. When a real life decision or goal comes up (a move, a renovation's
timing, a big purchase), give one grounded, warm-voiced take first — name the real tradeoff, or ask
the one pointed question that reframes it — before you log it to `memory/decisions.md` or
`memory/commitments.md`. Same beat as the work-mode reaction above, just without the RAPID apparatus.
*"A kitchen reno right before the baby's due might cost more in stress than money — want to talk
through timing, or just log it as-is?"*

**Ask about confidentiality (work mode only — skip entirely in personal mode, per the "By mode" note
above).** Ask narrowly: whether any project is **unannounced or pre-public** — an acquisition, a
reorg or reduction, an unannounced launch, or a live legal matter. Don't ask whether anything is
"sensitive" in general; most of their work is, and treating it that way buries their own memory
behind code names on day one. For each confidential one, agree on a **non-descriptive code name**,
record the real identity **only** in `memory/confidential/registry.md`, and track the work in
`memory/projects/<codename>.md` (no real name) — then use the code name from then on. When you
create the first confidential project, add the registry's **one** guarded link to `memory/index.md`,
under `## Load on demand` — e.g. `- [Confidential registry](confidential/registry.md) — PRIVATE;
load silently at boot, never quote/echo its contents.` This is the registry's **only** link, ever —
never from a specialist memory file, roster, or charter (`brain/schemas/team-member.md` → "Access control").
See `brain/schemas/confidentiality.md`. Row `confidentiality`.

Keep every identifying detail — the real name, the counterparty, any unmasking specifics — in
`memory/confidential/` **only** (the registry, or a sealed file there). On the de-identified
`memory/projects/<codename>.md`, use the **code name** and **non-identifying stakeholder labels**;
the memory file may **safely link to `memory/confidential/registry.md`** (a path, not a name — no leak),
mirroring how the registry can link back to the code-name memory file. Confidential facts in the onboarding
source note also use the code name only — never the real identity.

**Manual-path synthesis (no step-2 bootstrap ran).** If steps 3 and 4 were captured by hand — no
connector scan behind them — give the principal the same golden moment the bootstrap path gets, just
grounded in what they typed instead of scanned data. **This fires in every mode — work or personal —
not just work mode.** (The "no bootstrap ran" gate above still applies regardless of mode.) **If a
reaction beat already fired earlier this step** — the OKR critique, the open-decisions reaction, the
Work-IC sounding-board fallback, or the personal-mode reaction — **don't repeat the beat you just
gave** (including re-observing a KR the OKR critique already reframed); build on it or fold it in here
rather than re-observing the same answers. Before moving to preferences, offer 2–3 sharp
observations drawn only from what they've actually told you so far — who they lean on most, what
seems to dominate their plate, a rhythm that's already emerged from their answers. Frame it warmly —
*"Here's the shape of your world as you've described it so far:"* **Stay honest, same rail as the
bootstrap synthesis:** every observation must trace to something they actually said; if what they've
shared is too thin for anything specific, skip this gracefully rather than force a generic-sounding
insight.

**Propose a virtual team — grounded, at most one (once, opt-in).** You now know what they're actually
working on, so don't ask them to invent specialists — **propose them from what you just captured**:
their projects, OKRs, mandate, and any gap visible in the step-3 people map (a departed owner, an open
backfill). Name **2–3 candidates, one line each, with the reason attached** so they can judge each one
rather than take it on faith — then make a **single** ask: pick **at most one** to stand up now (the
per-specialist intake runs long); the rest stay a `/team-member-onboard` away. Make that ask in **its
own turn**, and keep it an ask — *"want me to stand up one of them now?"*, never softened to *"just
say so anytime"* on the way out of another row. Frame it to the mode —
*work-manager*: specialists to **augment your team**; *work-IC*: specialist helpers for **your craft**;
*personal*: helpers like a travel planner or a research assistant, grounded in the household and plans
you captured rather than an org.
*"Two that would earn their keep from what you've described: a **reliability engineer** — Meridian is
your top priority and it's at risk on reliability; and a **recruiter** — you're carrying Dana's open
backfill on top of the team. Want me to stand up one of them now? The other's there whenever you
want it."*

**Grounded, or the generic line — same honesty rail as the synthesis above.** Every specialist you
propose must trace to something they actually told you this session. If the context is too thin to
ground one — a sparse onboarding — fall back to the one-line generic offer (*"I can stand up
specialists whenever you want — just say so, or run `/team-member-onboard`"*). The generic line
still counts as the offer: `team-offer` → `done` or `declined`. Never manufacture a rationale to
make the proposal look sharp, and never skip the row.

**On yes**, run `brain/playbooks/team.md` (onboard) for the one they chose — that playbook creates the
specialist's charter, the `memory/team/index.md` roster (first specialist only), and the `memory/index.md` →
roster link, atomically; don't duplicate its steps here. **On no**, move on — it stays available later.
Don't push it: the row is `n/a` (note: team-offer off) if `team-offer: off` is set in
`memory/preferences/briefings.md` or the principal declined a team before. If the OKR critique was
just declined, keep this to its one line — still make it.

**Minimum-viable checkpoint (you're now useful).** It fires at the **end** of this step, never inside
it: every row step 4 owns — `projects`, `okrs`/`okr-critique`, `decisions`, `confidentiality`,
`team-offer` — is resolved first, because the only rows it may defer are `open-preferences`, `rhythms`
and `routines`. **A row you haven't reached yet is not a row you may defer here**, however the session
is going. With step 4 closed out, Chief of Staff already has enough to be genuinely useful — steps 5–6
are the lightest (preferences and routines). So if the principal is out of time or losing steam here,
**it's fine to pause**: tell them
you've got the essentials, leave `onboarding_status: in_progress` with `current_step` set, record the rows that remain
(`open-preferences`, `rhythms`, `routines`) as `deferred` with their agreement — the express path's
rule — and offer to **finish the rest anytime** (they just say so, or run `/onboard` to resume). Don't force the last two
steps in one sitting.

**A checkpoint pause is not Finishing.** Don't render the completion bar and don't set
`onboarding_status: complete` — `complete` supersedes `current_step`, so it doesn't pause onboarding,
it ends it, and nothing resumes. `defaults-menu` is **not** deferrable (`checklist.md` → Deferrable),
so it stays `open` and boot step 2 picks up there. Close with a short "here's what I have so far",
not the full recap.
