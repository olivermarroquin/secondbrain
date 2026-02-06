Below the Post-Run Synthesis is a End-to-End flow of how Resume-factory currently works

- Post-run Synthesis of today’s Resume Factory executions (From Chat That helped Me Execute this Day)
    - SECTION 1 — What Was Executed
        
        ### End-to-end workflows actually run
        
        You executed **real, production** runs of the job pipeline with these phases exercised in practice:
        
        1. **Intake (create job app folder + tracking + JD capture)**
            - Created job folders under `01_projects/jobs/qa_automation_engineer/<company>/<date_role>/`
            - Captured JDs (stdin paste and later file/pipe workaround)
            - Wrote tracking artifacts (`application-record.json`, `job-meta.json`, `status-history.md`)
            - Committed/pushed intake artifacts
        2. **Resume generation (template selection → edit proposals → apply edits → produce resume.docx)**
            - Auto-selected templates per job (multiple templates used across jobs)
            - Ran `resume-suggest-edits` with gate/missing-only logic
            - Applied edits with `resume-approve-edits` to produce `resume_refs/resume.docx`
            - Opened generated resumes (LibreOffice), and in some cases **manually edited** post-generation
        3. **Application batch flow (open URLs → apply in browser → mark applied in repo)**
            - Used batch queue generation (`jobs-apply-batch`) to open URLs and write `/tmp/applied-YYYY-MM-DD-batchN.txt`
            - Marked applied using both:
                - `jobs-mark-applied-last` (queue-driven; supports `-push`)
                - `jobs-batch-mark-applied` (path-file driven; does **not** support `-push`)
            - Verified state via `jobs-list-unapplied`
        4. **Session hygiene**
            - `session-start` / `session-close`
            - Post-run commits and pushes to keep repo clean
        
        ### Commands / scripts exercised
        
        **Core resume-factory / jobs pipeline commands used for real:**
        
        - `job-intake-one`
        - `job-intake-commit`
        - `jobs-list-unapplied`
        - `resume-select`
        - `resume-preview`
        - `resume-suggest-edits`
        - `resume-approve-edits`
        - `jobs-apply-batch`
        - `jobs-queue-show`
        - `jobs-mark-applied-last`
        - `jobs-batch-mark-applied`
        - `session-start`, `session-close`
        
        ### System surfaces actually tested
        
        - **STDIN ingestion path** (and its failure modes)
        - **JD term extraction + gating** (including “missing-only” logic)
        - **Template scoring + selection**
        - **Proposal generation + safety drops**
        - **Edit application mechanics** (REPLACE_LINE, REPLACE_PHRASE)
        - **Queue file semantics** for applied batches (creation, reuse, selection)
        - **Tracking file coherence** across `application-record.json` vs `job-meta.json` vs `status-history.md`
        - **LibreOffice interaction artifacts** (lock files, saving behavior)
        
        ---
        
    - SECTION 2 — Current Condition of Resume Factory
        
        ### Worked reliably
        
        - **Job folder scaffolding**: intake creates the right structure consistently.
        - **Commit/push discipline**: the workflow supported frequent commits without fighting Git.
        - **Template selection**: generally reasonable matches when JD terms overlapped expected stacks. (but needs some work still)
        - **Proposal application**: when proposals were produced, `resume-approve-edits` applied them deterministically and reported success/failure clearly.
        - **Applied-state reporting**: `jobs-list-unapplied` reliably reflected the *repo state* (once the metadata was corrected).
        
        ### Worked but felt fragile / awkward
        
        - **STDIN paste into `job-intake-one`**: paste sometimes “froze” mid-text and prevented additional typing, forcing aborts and rework.
        - **Batch application UX**: the relationship between:
            - queue files (`/tmp/applied-*`)
            - “batch number” vs “count”
            - `jobs-mark-applied-last` vs `jobs-batch-mark-applied`
                
                created cognitive load and misfires.
                
        - **Repeated runs of `resume-suggest-edits`**: output quality and gating logic produced surprising behavior (edits disappear/reappear between runs depending on what the system believes is “missing”).
        
        ### Required manual intervention
        
        - **LibreOffice manual edits** to finalize resumes (post `resume-approve-edits`).
        - **Handling LibreOffice lock files**:
            - lock files were tracked at one point → had to remove from index + add ignore rule.
        - **Correcting incorrect applied states**:
            - manual JSON edits were needed initially
            - later corrected properly once `job-meta.json` was identified as the driver for `jobs-list-unapplied`.
        - **Workarounds for stdin paste failures**:
            - writing JD to `/tmp/*.txt` and piping into intake. Using -- source clipboard also worked well for this issue.
        
        ### System surprises (good/bad)
        
        **Good surprises**
        
        - The “missing-only gate” behavior prevented a lot of unnecessary edits once terms were “present”. Even though some random unnecessary words would still pass through
        - Safety drops avoided obvious destructive edits (headers, role lines, headings) and duplicates.
        
        **Bad surprises**
        
        - Marking “applied” is not a single source of truth: **job-meta status** and **application-record status** can diverge and the system will behave based on whichever a command uses.
        - Batch queue numbering drifted (`batch1`, `batch2`, `batch3`…) and accidentally targeting the wrong job became easy.
        - Some JD term extraction produced low-signal or wrong terms (e.g., “az/mst”, “and/or”, “c2h”, “database/sql”), leading to awkward resume edits.
        - Missing-only gate:  Would have liked to see a lot more words in there that didn’t make it through even though the resume didn’t mention them example “qTest”, not in resume but still didn’t make it to the list of jd terms in any list.
        
        ---
        
    - SECTION 3 — Key Learnings From the Runs
        
        ### Expected vs actual behavior mismatches
        
        - **“Applied” state is not unified**:
            - You updated `application-record.json` to `not_applied` and saw *no change* because `jobs-list-unapplied` was driven by `job-meta.json.status`.
            - Real fix required updating **both** or making commands reference a single canonical source.
        - **Repeated `resume-suggest-edits` isn’t additive** in the way an operator expects:
            - Each run generates a new `edit-proposals.json`, and depending on gating logic, previously proposed edits may not reappear even if you want to “merge” them into a better combined edit.
        - **`resume-approve-edits` writes a fresh resume.docx**:
            - Operationally, it behaves like “generate from template + apply selected proposals”, not “patch the current resume.docx”, which clashes with manual-edit workflows.
        
        ### Highest friction / cognitive load steps
        
        - **Paste-to-stdin capture**: unpredictable terminal behavior forced resets and alternate methods.
        - **Batch apply flow**: knowing which command opens which URL, and why it opened the “wrong one”, required reasoning about queue files and selection logic rather than intent.
        - **State reconciliation**: knowing which file(s) determine applied/not_applied required investigation (job-meta vs application-record vs status-history).
        
        ### Missing guardrails / validations
        
        - No “single command” to **revert applied → not_applied** safely across all tracking files (you had to do it manually).
        - No validation that `job-meta.json.status` matches `application-record.json.current_status` (drift happened).
        - No batch tooling that forces an explicit target selection (by index or app path) before opening URLs.
        
        ### Operator discipline > tooling
        
        - Correct results depended on you:
            - clearing stale `/tmp/applied-*` queues
            - committing/pushing at the right points
            - manually fixing metadata drift
            - avoiding editing the generated resume in ways that conflict with re-generation
        - The system is usable now, but it demands high attention because **mistakes look like “the tool is wrong” when it’s really “the state is ambiguous.”**
        
        Another friction area was that there was still so much manual work done by me in the entire process. It takes a lot longer and results (suggestions) aren’t as great or worth it. Higher level automations (possibly using agents) would help immensely.
        
        ---
        
    - SECTION 4 — Limitations Discovered
        
        ### Structural limitations
        
        - **Multiple sources of truth for status** (`job-meta.json`, `application-record.json`, `status-history.md`) without enforced coherence.
        - **Resume generation baseline is the template**, not the last generated resume; this prevents iterative “patching” without losing prior manual edits.
        
        ### Workflow limitations
        
        - Batch flow is **queue-file centric**; operator intent is “open job X”, but tooling is “open the next N not_applied jobs”, which is error-prone when the list order isn’t the mental model.
        - Re-running suggestions to “get more keywords” is constrained by gating logic and unsafe-drop logic; it’s not designed for “progressive refinement”.
        
        ### CLI UX limitations
        
        - `jobs-open` doesn’t exist; opening a specific job requires calling batch tools or manually opening URLs.
        - Inconsistent flags across commands (`-push` exists in one place but not another) created confusion mid-run.
        - Stdin capture has a failure mode that feels like the CLI “hangs” with no actionable guidance.
        
        ### Automation limits / scaling risk
        
        If you tried to run 20 jobs today with the current setup:
        
        - Status drift would compound quickly.
        - Queue confusion would cause mis-targeted applications.
        - JD term extraction noise would amplify low-quality edits, creating more manual cleanup.
        - Re-running suggestions would waste time because it’s not reliably incremental.
        
        ---
        
    - SECTION 5 — Recommended Enhancements
        
        ### P0 — Must-fix before running 20 jobs
        
        1. **Unify status source of truth**
            - Problem: status drift between `job-meta.json` and `application-record.json` breaks trust in `jobs-list-unapplied`.
            - Applies to: tracking schema + all `jobs-*` commands that read/write status.
            - Change size: **medium** (schema decision + update readers/writers + migration script).
            - Concrete: pick canonical status (likely `job-meta.json.status`), and have other files derived or auto-updated.
        2. **Add a safe “revert applied” command**
            - Problem: manual JSON edits are risky and incomplete; you already hit this.
            - Applies to: new CLI command (e.g., `jobs-status-set --app ... --status not_applied --note ...`) or `jobs-mark-not-applied`.
            - Change size: **small/medium**.
            - Concrete: update `job-meta.json`, `application-record.json`, append to `status-history.md`, clear `date_applied`.
        3. **Batch selection must be explicit**
            - Problem: “batch auto” opened the wrong job because selection was list-driven.
            - Applies to: `jobs-apply-batch` UX.
            - Change size: **medium**.
            - Concrete: allow `jobs-apply-open --app <path>` and/or `jobs-apply-batch --pick <index|company>` that prints the candidate list and requires confirmation.
        4. **Fix stdin ingestion reliability**
            - Problem: terminal paste freezing forced workarounds.
            - Applies to: `job-intake-one` stdin reader or terminal handling instructions.
            - Change size: **small** if solved by code (read loop), **small** if solved by documented recommended path (clipboard/file).
            - Concrete: support `-source clipboard` (pbpaste) and `-source file:/path` as first-class paths; recommend against interactive paste.
        
        ### P1 — High-leverage quality / reliability improvements
        
        1. **Make resume generation incremental-aware**
            - Problem: re-running `resume-approve-edits` regenerates from template; manual edits get overridden.
            - Applies to: `resume-approve-edits`.
            - Change size: **structural adjustment**.
            - Concrete options (not a redesign):
                - add `-base resume_refs/resume.docx` to apply proposals onto the current generated resume
                - or persist “applied proposals” and reapply cumulatively when regenerating
        2. **Improve JD term extraction quality**
            - Problem: noisy terms (“and/or”, “az/mst”, “c2h”, “database/sql”) degrade proposal quality.
            - Applies to: `rf_jd_terms.py`.
            - Change size: **small/medium**.
            - Concrete: hard filters for timezones/locations conjunctions, normalize “C2H” to “contract-to-hire” (or drop), split/normalize “database/sql” into `sql`, and add a “low-signal term” suppress list.
        3. **Proposal quality controls**
            - Problem: awkward phrasing (“integrating C2H methodologies”) and forced keyword insertion.
            - Applies to: proposal generator prompting rules + validator.
            - Change size: **medium**.
            - Concrete: add rules: “never invent process terms; prefer natural phrasing; avoid location/timezone terms; don’t add meaningless ‘methodologies’”.
        4. **Command flag consistency**
            - Problem: `-push` exists in one status command but not another, causing errors and mid-run confusion.
            - Applies to: `jobs-mark-applied-last`, `jobs-batch-mark-applied`.
            - Change size: **small**.
            - Concrete: standardize: either both support `-push`, or neither and the workflow always ends with `git push`.
        5. **Queue file ergonomics**
            - Problem: multiple `/tmp/applied-*batchN.txt` accumulates; wrong queue used.
            - Applies to: `jobs-apply-batch` and queue tools.
            - Change size: **small**.
            - Concrete: write queue files to a deterministic path per date+batch, and add `jobs-queue-ls --date` / `jobs-queue-pick`.
        
        ### P2 — Can wait, but we can do soon
        
        1. **Auto-detect LibreOffice lock files and prevent tracking**
            - Problem: lock artifacts contaminated repo once.
            - Applies to: repo hygiene tooling.
            - Change size: **small** (pre-commit hook or `session-close` check).
            - Concrete: add a `session-close` warning if `.~lock.*#` exists anywhere.
        2. **Add a “jobs-open-url” convenience command**
            - Problem: operator wants “open this job now” without batch semantics.
            - Applies to: jobs CLI.
            - Change size: **small**.
            - Concrete: `jobs-open --app <path>` that reads `jd/job-post-url.txt` and opens it.
        
        ---
        
    - SECTION 6 — How AI-in-CLI Will Improve This System
        
        ### Continuous codebase access improves fix quality
        
        Today’s failures were **stateful, multi-file, and workflow-dependent**. AI with repo access can:
        
        - trace which commands read which files (e.g., why `jobs-list-unapplied` ignored `application-record.json`)
        - find inconsistent flag behavior across commands quickly
        - implement changes consistently across all entrypoints without missing one path
        
        ### Why AI-assisted step-by-step changes are safer than manual edits
        
        You already experienced that “fixing it manually” led to partial correction until you discovered the real driver file. AI-in-CLI can:
        
        - add validations that prevent partial edits from being accepted
        - run local checks after each patch (unit-ish checks + end-to-end dry runs)
        - enforce deterministic diffs and reduce accidental drift
        
        ### Problem categories AI is especially suited to (based on today)
        
        - **Edge case hunting**: stdin paste freeze, queue-file mismatch, status drift
        - **Consistency enforcement**: unify flags, unify status handling
        - **Refactor-with-constraints**: incremental resume base support without redesign
        - **Invariant checks**: “these three tracking files must agree” assertions
        - **Prompt/schema tightening**: stop low-quality keyword stuffing and banned-term injection
        
        ---
        
    - SECTION 7 — Where AI Should Focus First (Top 5)
        1. **Status source-of-truth + drift prevention**
            - Targets: `jobs-list-unapplied`, `jobs-mark-applied-last`, `jobs-batch-mark-applied`, tracking writers
            - Goal: single canonical status + automatic coherence updates
        2. **Add `jobs-status-set` (or `jobs-mark-not-applied`)**
            - Targets: new command + shared status mutation utility
            - Goal: safe reversible status transitions with consistent history logging
        3. **`jobs-apply-batch` selection + queue UX**
            - Targets: batch selection logic, queue file naming, `jobs-queue-show`/`jobs-queue-*`
            - Goal: prevent wrong-job opens and make intent-driven targeting trivial
        4. **STDIN ingestion + alternative sources for intake**
            - Targets: `job-intake-one` input reader + add first-class `clipboard` / `file` sources
            - Goal: eliminate terminal paste freeze class entirely
        5. **JD term extraction + proposal quality controls**
            - Targets: `rf_jd_terms.py`, proposal schema/prompt rules, unsafe-drop reasons
            - Goal: stop garbage terms and awkward edits; improve “keyword alignment” without degrading language quality


--------------------------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------------------------------------


- Golden Run Checklist (Job #1-6 end-to-end, insightful “golden run”)
    <aside>
    🎙️
    
    **Hard rule:** After *every step*, you paste the terminal output in Chat before we proceed.
    
    - **Mode 1:** Golden run **(recommended for Job #1)**
        
        1 job fully end-to-end:
        
        - intake → resume → apply → mark applied → close
        
        ✅ **Best practice for accuracy + sanity:**
        
        **Intake → build resume for 1 job → apply that job → mark applied** (repeat)
        
    - **Mode 2:** Batch **(jobs 2–20)**
        
        Do it in chunks (5–10 at a time):
        
        - intake chunk → build resumes chunk → apply-batch chunk → prune → mark applied
        
        This prevents tab explosion and keeps marking accurate.
        
        ✅ **Best practice for throughput (batch):**
        
        **Intake a bunch → build resumes for a batch → then `jobs-apply-batch 25` to apply → prune → mark applied**
        
    - 🚫 **Worst practice:**
        
        Intake → `jobs-apply-batch 25` → 25 tabs open → then *try* to build 25 resumes while those tabs sit there.
        
        You’ll lose track, and you’ll mis-mark applied. Period.
        
    </aside>
    
    - Step 0 — Pre-flight (repo + tools + git)
        
        ```bash
        cd ~/secondbrain
        pwd
        which session-start session-close job-intake-one jobs-list-unapplied jobs-apply-batch jobs-mark-applied-last resume-select resume-preview resume-suggest-edits resume-approve-edits
        git status -sb
        
        --------------------------------------------------------------------------------------------------------------
        # OR for second runs:
        # to check what is currently pending to be applied to
        jobs-list-unapplied --date "$(date +%F)"
        
        #it may say something like this (meaning you are in the clear)
        olivermarroquin@Olivers-MacBook-Pro secondbrain % jobs-list-unapplied --date "$(date +%F)"
        
          #  COMPANY               ROLE                                 FOUND       URL
        --------------------------------------------------------------------------------------------------------------
        
        Total not_applied (date_found=2026-02-05): 0
        ```
        
        **Success looks like**
        
        - `pwd` shows `.../secondbrain`
        - `which` returns paths (not “not found”)
        - `git status -sb` is clean or only shows changes you explicitly expect
        
        ⬅️ Paste the output.
        
        ---
        
    - Step 1 — Start session (loads state context) - **Need to re-run this every time you run session-close**
        
        ```bash
        session-start
        ```
        
        **Success looks like**
        
        - It prints git context + your state context without errors (Example Below)
            
            ```java
            olivermarroquin@Olivers-MacBook-Pro secondbrain % session-start
            
            == Repo ==
            /Users/olivermarroquin/secondbrain
            
            == Fetch ==
            Enter passphrase for key '/Users/olivermarroquin/.ssh/id_ed25519_github': 
            
            == Status ==
            ## main...origin/main
            
            == Recent history ==
            * 2fe625e (HEAD -> main, origin/main) chore(code): reorganize automation projects and add language frameworks
            * ed277ff reset(jobs): remove practice job data before first production run
            * fc5f3d9 Refactor Playwright automation structure and remove legacy artifacts
            * 9629348 Ignore target and remove build artifacts
            * bf9f77a Ignore Maven target directories
            * c765677 Add gitignore
            * 513ecc7 Ignore AI refactor and Maven target artifacts
            * 35bd659 Remove AI refactor artifacts from CBAPS_DAWMS
            * d35a817 Refactor CBAPS_DAWMS scaffold: split cbaps and dawms packages
            * bc04315 Add patch extractor for Claude-generated new-file diffs
            
            == Global STATUS.md (top) ==
            # STATUS (Global)
            
            Active project path: 01_projects/resume-factory
            
            ## Active project
            - Name: resume-factory
            - Location: 01_projects/resume-factory
            - Current step: TBD
            
            ## Current focus
            - Automate end-to-end resume tailoring, tracking, and interview prep from job descriptions
            
            ## Git + GitHub
            - Repo: secondbrain
            - GitHub: olivermarroquin/secondbrain
            - Auth: SSH (id_ed25519_github), keychain-backed
            - Default branch: main
            
            ## Working agreements (non-negotiable)
            - Git-first, patch-first
            - No long dirty states
            - RWWLO rule: no work begins until NEXT.md is accurate (updating NEXT is always task #0)
            
            == Global NEXT.md (top) ==
            # NEXT (Global)
            
            ## Task #0 (always allowed)
            - If this file is not accurate, update it first.
            
            ## Routing pointer
            - Active project NEXT: 01_projects/resume-factory/state/NEXT.md
            
            == Project STATUS.md (top) == [01_projects/resume-factory]
            # STATUS (Project)
            
            ## Project Identity
            - Name: Resume Factory
            - Path: 01_projects/resume-factory
            - Type: Continuous / Long-running
            - Primary owner: Oliver
            - Created: 2026-01-20
            
            ## Current State
            - Lifecycle phase: Design / Build / Refactor / Maintenance
            - Current focus:
              - Define AI + Git collaboration workflow (RWWLO)
            - Blocking issues:
              - None
            - Open questions:
              - How granular should patch protocol be for AI edits?
            
            ## Active Context
            - Entry point:
              - state/NEXT.md
            - Current step:
              - Step 3 — Finalize repo collaboration workflow
            - Last completed step:
              - Step 2 — Session rituals + state scaffolding
            - Expected next transition:
              - From “Workflow definition” → “Git muscle memory drills”
            
            ## Working Agreements (Non-negotiable)
            - Work from `state/NEXT.md`, not memory
            - If `NEXT.md` is inaccurate, updating it is task #0
            - Git-first, patch-first workflow
            - No long-lived dirty working trees
            - Commit state changes before ending a session
            
            ## Automation Notes (for AI / CLI)
            - Read order:
              1. state/STATUS.md
              2. state/NEXT.md
              3. git log (last 10)
            - Safe to automate:
              - Editing NEXT.md
              - Appending LOG.md
            - Requires confirmation:
              - Structural refactors
              - Deleting files
              - Rewriting DECISIONS.md
            
            ## Links / Artifacts
            - Repo: olivermarroquin/secondbrain
            - Related docs:
              - 07_system/state/WORKFLOW.md# STATUS (Project)
            
            ## Project
            - Name: (fill)
            - Location: (this folder)
            
            ## Current focus
            - (fill)
            
            ## Working agreements
            - Work from state/NEXT.md, not memory
            - If NEXT is wrong, updating NEXT is task #0
            
            == Project NEXT.md (top) == [01_projects/resume-factory]
            # NEXT (Project)
            
            ## Scope
            - Project: resume-factory
            - Path: 01_projects/resume-factory
            - Applies to: This project only
            
            ## Focus
            Focus: Automate end-to-end resume tailoring, tracking, and interview prep from job descriptions
            
            ## Task #0 — State correction (always allowed)
            - If this file does not accurately represent the next actions, update it before doing any other work.
            - Updating NEXT.md does not require a prior commit.
            
            ## Execution Rules
            - Tasks are executed top-down.
            - Do not skip tasks unless explicitly marked optional.
            - If a task becomes invalid, mark it as [obsolete] and explain why.
            - New tasks are appended (do not insert above in-progress work).
            
            ## Next Actions Queue
            1) (fill)
            Rule: No work begins until NEXT.md is accurate (updating NEXT is task #0).
            
            ```
            
        
        ⬅️ Paste the output.
        
        **Next immediate step:** make `state/NEXT.md` accurate for *this session* (your system says no work begins until it is).
        
        Run:
        
        ```bash
        sed -n '1,120p' 01_projects/resume-factory/state/NEXT.md
        ```
        
        Paste the output.
        
        ```java
        olivermarroquin@Olivers-MacBook-Pro secondbrain % sed -n '1,120p' 01_projects/resume-factory/state/NEXT.md
        # NEXT (Project)
        
        ## Scope
        - Project: resume-factory
        - Path: 01_projects/resume-factory
        - Applies to: This project only
        
        ## Focus
        Focus: Automate end-to-end resume tailoring, tracking, and interview prep from job descriptions
        
        ## Task #0 — State correction (always allowed)
        - If this file does not accurately represent the next actions, update it before doing any other work.
        - Updating NEXT.md does not require a prior commit.
        
        ## Execution Rules
        - Tasks are executed top-down.
        - Do not skip tasks unless explicitly marked optional.
        - If a task becomes invalid, mark it as [obsolete] and explain why.
        - New tasks are appended (do not insert above in-progress work).
        
        ## Next Actions Queue
        1) (fill)%                                               
        ```
        
        Note that “Next Actions Queue” is empty, we changed it to this since the session-start said it should not be empty
        
        ```java
        ## Next Actions Queue (this will be empty later for AI to be able to use it)
        1) Golden run Job #1: run intake → verify → resume-select/preview → suggest edits → approve edits → generate resume.docx
        2) Golden run Job #1: run jobs-apply-batch (dry-run → real) → apply → prune if needed → jobs-mark-applied-last (dry-run → apply/commit/push)
        3) Close session correctly (git clean, session-close)%        
        ```
        
        ---
        
    - Step 2 — Set today boundary var (Optional — Good for batches)
        
        Optional — You do **not** need to set `D` manually for this step.
        
        Why:
        
        - If the command already uses `-date "$(date +%F)"`, that resolves the date inline.
        - Setting `D` is only needed later for **batch apply / filtering**, not for intake.
        
        ```bash
        D=$(date +%F)
        echo "$D"
        ```
        
        **Success looks like**
        
        - Prints today’s date (YYYY-MM-DD)
        
        ⬅️ Paste the output.
        
        ---
        
    - Step 3 — Intake the job (creates job folder + captures JD + commit/push)
        - If using AI Chat to give you the intake command for folder and file designation use this template:
            
            
            ```java
            JOB 2
            <JD text or URL or both>
            
            JOB 3
            <JD text or URL or both>
            
            JOB 4
            <JD text or URL or both>
            
            JOB 5
            <JD text or URL or both>
            
            JOB 6
            <JD text or URL or both>
            ```

            Example for pasting it into a ChatGPT chat for it to give me exact command.
            
            ```java
            JOB 2
            INSPYR Solutions
            Job Details
            Skills
            QUALITY ASSURANCE ENGINEER
            SOFTWARE QUALITY ASSURANCE
            AGILE QA
            QA ENGINEER
            QA
            TOSCA
            TRICENTIS TOSCA
            MANUAL TESTING
            UI TESTING
            API TESTING
            AZURE DEVOPS
            QTEST
            TEST PLANNING
            SQL
            ISTQB
            AUTOMATION
            Summary
            Title: Quality Assurance Engineer
             Location: Remote (EST Hours)  
            Duration: 6 Month Contract to Hire
            Compensation: $40-46/HR Contract, Conversion Target: $100-$115K
            Work Requirements: , Holder
            
            Job Description:
            Job Summary
            We are seeking a Senior Quality Engineer with strong hands-on experience in Tosca automation and manual testing. This role focuses on designing and executing robust test coverage across UI, APIs, and data, while partnering closely with Product Owners and development teams to ensure quality delivery.
            
            Key Responsibilities
            Design, create, execute, and maintain manual and automated test cases aligned to acceptance criteria.
            Develop, enhance, and optimize Tosca automation frameworks and reusable modules.
            Execute functional, regression, API, database, and performance tests.
            Own regression test strategy and coverage for assigned applications.
            Validate backend services, integrations, and complex data flows.
            Manage test planning, execution, and reporting using qTest.
            Log, triage, and validate defects using Azure DevOps.
            Provide test estimates, risk assessments, and quality recommendations.
            Act as a QA point of contact within Agile teams.
            Participate in and contribute to Agile ceremonies.
            Deliver clear test metrics, status reporting, and release readiness assessments.
            
            Required Qualifications
            6–9 years of experience in software quality assurance with strong automation and manual testing focus.
            Strong hands-on expertise with Tricentis Tosca.
            Experience with Azure DevOps and qTest.
            Strong understanding of Agile, SDLC, and QA best practices.
            Solid SQL skills for complex data validation.
            Working knowledge of performance testing execution.
            Strong communication and collaboration skills.
            
            Preferred Qualifications
            Tosca certifications.
            ISTQB certification.
            Extensive experience testing APIs and backend services.
            
            https://www.dice.com/job-detail/9cc26130-6290-4377-9af5-f22f5f7ae48c
            
            JOB 3
            Innominds Software
            Innominds Software
            Skills
            QA Automation
            Java
            API
            Selenium
            Summary
            Role: QA Automation Engineer
            Location: Remote
            Duration: 6 Months C2H
            
            Skill Set:, Java, Automation, Java, Automation, API
            
            Please find below the JD -:
            
            A QA- with minimum 5 years of experience.
            Strong Communication Skills & Team management skills
            Strong experience in working for enterprise clients.
            Understanding of overall Testing process and experience in Agile Methodology
            Very Good knowledge of database/SQL queries
            Knowledge of implementing various testing methodologies, test automation tools
             
            Thanks & Regards,
            
            Jagga Rao
            
            https://www.dice.com/job-detail/e73e4b93-50a2-4ece-b93a-f02211bebede
            
            JOB 4
            Pellera
            Job Details
            Skills
            Artificial Intelligence
            Testing
            Test Suites
            Collaboration
            Reporting
            Mentorship
            Analytical Skill
            Problem Solving
            Conflict Resolution
            Bug Tracking
            JIRA
            Bugzilla
            Programming Languages
            Java
            Python
            C#
            Version Control
            Git
            Quality Assurance
            Orchestration
            Docker
            Kubernetes
            Communication
            Management
            Organizational Skills
            Critical Thinking
            Computer Science
            Software Quality Assurance
            Test Cases
            TestRail
            Zephyr
            API QA
            POSTMAN
            Mobile Testing
            Appium
            Automated Testing
            Selenium
            TestNG
            JUnit
            Continuous Delivery
            Jenkins
            GitLab
            Continuous Integration
            CircleCI
            Security QA
            Summary
            Practice/Department: Artificial Intelligence
            
            Position Title: Senior Quality Assurance Engineer
            
            Job Family: Services
            
            Position Location: Remote
            
            Reports to: Manager
            
            Job Summary:
            
            The Senior Quality Assurance Engineer role designs and develops robust, scalable automated test frameworks and test suites, leading the planning and execution of automated tests, and collaborating with developers and QA engineers to identify and report bugs. The role also includes continuously improving testing strategies, integrating testing into the CI/CD pipeline, analyzing test results, and mentoring junior engineers.
            
            Essential Functions:
            Design and develop robust, scalable, and efficient automated test frameworks and test suites.
            Lead the planning, creation, and execution of automated tests for new features and enhancements.
            Collaborate with software developers and other QA engineers to identify, reproduce, and report bugs and errors.
            Continuously improve automated testing strategies and tools to enhance test efficiency and reliability.
            Integrate automated testing into the CI/CD pipeline to ensure consistent and reliable software delivery.
            Analyze test results, document test reports, and track quality assurance metrics.
            Mentor junior engineers and provide guidance on best practices in automated testing.
            Stay updated with the latest industry trends in test automation and software quality assurance.
            Other duties as assigned.
            
            Required Skills/Abilities/Competencies
            Strong analytical and problem-solving skills.
            Proficiency in bug tracking tools like JIRA or Bugzilla.
            Familiarity with mobile testing tools like Appium or Espresso.
            Proficient in one or more programming languages such as Java, Python, or C#.
            Familiarity with version control systems like Git.
            Strong understanding of software QA methodologies, tools, and processes.
            Knowledge of containerization and orchestration technologies (Docker, Kubernetes) is a plus.
            Excellent verbal and written communication skills.
            Ability to work effectively in a team environment as well as independently.
            Strong time management and organizational skills.
            A proactive approach to tackling challenges and improving processes.
            Ethical and critical thinking.
            
            Education and Experience:
            Bachelor's degree in Computer Science, Engineering, or related field.
            Minimum of 5 years of experience in software quality assurance, with at least 3 years focused on test automation.
            In-depth experience with test case management tools such as TestRail or Zephyr.
            Experience with API testing tools such as Postman or Swagger.
            Familiarity with mobile testing tools like Appium or Espresso.
            Extensive experience with automated testing frameworks and tools like Selenium, TestNG, JUnit, or similar.
            Experience with CI/CD tools such as Jenkins, GitLab CI, or CircleCI.
            Experience with performance and/or security testing is highly desirable.
            
            https://www.dice.com/job-detail/f6e9acea-9139-436b-9822-24e7c293b98f
            
            JOB 5
            Business and Technology Solutions, LLC
            Summary
            Our East Coast based client is seeking a fully remote Consulting QA / Test Engineer with E-commerce platform experience, preferably Magento / Adobe Commerce Cloud. The Consulting QA / Test Engineer will work independently and be responsible for, and not limited to: Manual and Automated testing of E-Commerce features, enhancements, and bug fixes; validating front end functionality across browsers and devices; testing UI behavior / interactions with Alpine.js; validating layouts and styling responsiveness implemented with Tailwind CSS; verifying E-Commerce workflows (catalog browsing, search, cart, checkout, customer accounts, promotions); verifying Admin Workflows (product, pricing, promotions, orders, inventory, customer management, and system configuration); identifying, documenting, and tracking defects with clear reproduction steps, screenshots, and logs; testing API Integrations (REST / SOAP / GraphQL); E-Commerce Storefront workflows (checkout, payment processing, shipping, taxes, etc.); testing integrations with ERP, CRM, WMS, Payment Gateways, and Customer Experience Platforms; executing Performance / Load testing.
            
            To be considered for this project, you must have:
            
            Manual and Automated testing of E-Commerce features, enhancements, and bug fixes; validate front-end functionality across browsers and devices
            Experience with testing API Integrations (REST / SOAP / GraphQL),
            Experience using defect tracking and test management tools such as Jira, TestRail, etc.
            Ability to test UI behavior / interactions with Alpine.js; validate layouts and styling responsiveness implemented with Tailwind CSS; verify E-Commerce workflows (catalog browsing, search, cart, checkout, customer accounts, promotions)
            Experience testing integrations with ERP, CRM, WMS, Payment Gateways, and Customer Experience Platforms
            Working knowledge of GIT and other collaborative development tools
            Ability to effectively write queries in SQL to validate data
            Experience verifying Admin Workflows (product, pricing, promotions, orders, inventory, customer management, and system configuration); identifying, documenting, and tracking defects with clear reproduction steps, screenshots, and logs
            Strong verbal and written communication (focus on documentation) and interpersonal skills, with a proven ability to work effectively with cross functional teams as well as independently as an individual contributor
            Nice to have:
            
            Experience developing QA Plan (Requirements Analysis, Test Planning, Test Case Development, Environment Setup, Test Execution, Test Cycle Closure)
            Experience with Automated testing tools (Cypress, Playwright, Selenium)
            Exposure to Agile / Scrum software development
            Experience with Magento Commerce Cloud
            
            https://www.dice.com/job-detail/2fb74bd7-3d7d-457e-afe6-c74369e12878
            
            JOB 6
            TechTalent Solutions LLC
            Job Details
            Skills
            Oracle ERP
            TOSCA
            Summary
            Job Title: TOSCA Tester /QA automation Lead Oracle Modules
            Location: 100% Remote
            Mode: Fulltime
            
            Must Have: Oracle ERP
            
            Job Description:
            
            We are seeking an experienced TOSCA Automation Lead/ Engineer with strong expertise in Oracle applications to join our QA automation team. The ideal candidate will be responsible for designing, developing, and maintaining automated test solutions using Tricentis TOSCA, ensuring high-quality delivery of Oracle implementations.
            
            Key Responsibilities:
            
            Design, develop, and execute automation test scripts using Tricentis TOSCA
            Collaborate with business analysts, developers, and QA teams to understand requirements
            Maintain and enhance existing automation frameworks
            Perform test data management and test execution reporting
            Identify, log, and track defects using standard defect management tools
            Support CI/CD integration for automated test execution
            Ensure best practices in test automation and QA processes
            Required Skills & Qualifications:
            
            Strong hands-on experience with Tricentis TOSCA
            Experience testing Oracle (ERP,Financials, SCM, HCM, or related modules)
            Solid understanding of QA methodologies and SDLC
            Ability to work independently in a remote environment
            Good communication and documentation skills
            Nice to Have:
            
            TOSCA Certification
            
            https://www.dice.com/job-detail/32b401e0-bf06-4716-943c-8dcd9865445e
            ```
            
        - **ISSUE Fixed** - copy/paste issue happens in the stdin when copying the JD Text **(Alternate fix is to use --source clipboard, it works as well)**
            - **Solution #1**: Create JD file in /tmp and paste there)
                
                Run:
                
                ```bash
                TMP_JD=/tmp/jd-job5.txt
                : >"$TMP_JD"
                open -a TextEdit"$TMP_JD"
                ```
                
                In TextEdit:
                
                1. Paste the **entire JOB 5** JD text (from “Summary …” through the end)
                2. **Save** (Cmd+S)
                3. Close TextEdit
                
                Then run this verification:
                
                ```bash
                wc -l "$TMP_JD"
                tail -n 5 "$TMP_JD"
                ```
                
                **Next immediate step — Job #5 intake from file**
                
                ```java
                cat /tmp/jd-job5.txt | job-intake-one \
                  --family qa_automation_engineer \
                  --company business_and_technology_solutions_llc \
                  --role consulting-qa-test-engineer \
                  --date "$(date +%F)" \
                  --url "https://www.dice.com/job-detail/2fb74bd7-3d7d-457e-afe6-c74369e12878" \
                  --source stdin
                ```
                
            - **Solution #2**: Use —source clipboard
                
                ```java
                job-intake-one \
                  --family qa_automation_engineer \
                  --company techtalent_solutions_llc \
                  --role tosco-tester-qa-automation-lead-oracle-modules \
                  --date "$(date +%F)" \
                  --url "https://www.dice.com/job-detail/32b401e0-bf06-4716-943c-8dcd9865445e" \
                  --source clipboard
                ```
                
                How it looks in Terminal
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % job-intake-one \
                  --family qa_automation_engineer \
                  --company techtalent_solutions_llc \
                  --role tosco-tester-qa-automation-lead-oracle-modules \
                  --date "$(date +%F)" \
                  --url "https://www.dice.com/job-detail/32b401e0-bf06-4716-943c-8dcd9865445e" \
                  --source clipboard
                  
                APP: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules
                SRC: clipboard
                
                JD capture (clipboard): copy full JD in browser (Cmd+C), then press Enter.
                Press Enter to read clipboard: 
                APP : /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules
                OUT : /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules/jd/jd-raw.txt
                CLIP: 33 lines
                
                Preview (first 5):
                Job Details
                Skills
                Oracle ERP
                TOSCA
                Summary
                
                Preview (last 1):
                TOSCA Certification
                
                Type APPLY to write clipboard into jd-raw.txt: APPLY
                
                Wrote:
                      33 /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules/jd/jd-raw.txt
                
                Verify (first 5):
                Job Details
                Skills
                Oracle ERP
                TOSCA
                Summary
                
                Verify (last 1):
                TOSCA CertificationOK
                
                Next:
                  job-intake-commit --app "/Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules"
                
                /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/techtalent_solutions_llc/2026-02-05_tosco-tester-qa-automation-lead-oracle-modules
                ```
                
        - Intake the Job
            
            You will run **one** of these based on your input source:
            
            - **URL scrape** (`--source url`): fastest, may fail on JS pages
            - **Clipboard** (`--source clipboard`): reliable (copy JD → run command)
            - **Stdin** (`--source stdin` OR `job-intake-from-stdin`): paste into terminal, end with Enter then Ctrl+D
            
            ---
            
            - **A) URL scrape (fast path)**
                
                ```bash
                job-intake-one \
                  --company <company_snake_case> \
                  --date "$D" \
                  --role <role-kebab-case> \
                  --url "<job_post_url>" \
                  --source url \
                  --commit --push
                ```
                
            - **B) Clipboard JD (reliable)**
                
                ```bash
                job-intake-one \
                  --company <company_snake_case> \
                  --date "$D" \
                  --role <role-kebab-case> \
                  --url "<job_post_url>" \
                  --source clipboard \
                  --commit --push
                ```
                
            - **C) Paste JD in terminal (stdin)**
                
                ```bash
                job-intake-one \
                  --company <company_snake_case> \
                  --date "$D" \
                  --role <role-kebab-case> \
                  --url "<job_post_url>" \
                  --source stdin \
                  --commit --push
                ```
                
            
            **Success looks like**
            
            - It prints the created **app path**
            - JD ends up in `jd/jd-raw.txt`
            - Commit happens (and push if enabled)
            
            ⬅️ Paste the output (especially the printed app path).
            
            - **Run #1 - Single Job**
                
                ```java
                job-intake-one \
                  --family qa_automation_engineer \
                  --company kforce \
                  --role lead-software-qa-engineer \
                  --date "$(date +%F)" \
                  --url "https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e" \
                  --source stdin
                ```
                
                Paste the JD and hit Enter then Ctrl+D
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % job-intake-one \
                  --family qa_automation_engineer \
                  --company kforce \
                  --role lead-software-qa-engineer \
                  --date "$(date +%F)" \
                  --url "https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e" \
                  --source stdin
                
                APP: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                SRC: stdin
                
                Paste JD now. Finish with Ctrl+D.
                Job Details
                Skills
                FOCUS
                Continuous Delivery
                Innovation
                Mentorship
                JavaScript
                C#
                Java
                TypeScript
                Quality Assurance
                Management
                Acceptance Testing
                Documentation
                Collaboration
                Agile
                Cypress
                Manual Testing
                Automated Testing
                Regression Analysis
                Load Testing
                Testing
                RESTful
                Test Management
                Application Lifecycle Management
                Microsoft TFS
                API QA
                Apache JMeter
                POSTMAN
                Performance Testing
                Cloud Computing
                Amazon Web Services
                Microsoft Azure
                Heroku
                SOA
                Artificial Intelligence
                Messaging
                Summary
                RESPONSIBILITIES:
                Kforce's Phoenix-based client needs to add a Lead Software QA Engineer to their team. This is a fully remote role that can be performed from anywhere in the US (AZ/MST hours required). This is a ten month contract assignment to start.
                
                Duties & Role Description:
                The Quality Assurance Engineer is responsible for ensuring the quality, reliability, and performance of Republic Services' Web, Mobile, and Application portfolios. Operating remotely within the AZ time zone, this ro a strong focus on automated testing within Agile and Continuous Delivery environments.
                
                The Lead Quality Assurance Engineer will architect and implement automation frameworks, develop and maintain automated and manual test plans, and drive innovation in testing strategies. A key part of the role is mentoring Software Test Engineers, reviewing specifications, and shaping test architectures that enhance quality and reduce risk.
                
                Core responsibilities include building and executing automated testing for end-to-end integration across applications, platforms, and devices using JavaScript, C#, Java, TypeScript, and related tools. The Lead Quality Assurance Engineer will evaluate and implement testing tools, manage defects across release cycles, ensure traceability to requirements, and support user acceptance testing. Additional duties include analyzing test metrics, ensuring adherence to documentation standards, and participating in functional, system, regression, and load testing. Collaboration with developers and Agile teams is essential to ensure software meets functional and technical standards.
                
                REQUIREMENTS:
                * Experience with Cypress, AWS, and APIs
                * Experience in both automated and manual testing
                * To be considered for this position, candidates must have experience in a similar role, or they must possess significant knowledge, experience, and abilities to successfully perform the responsibilities listed
                * Relevant education and/or training will be considered a plus
                
                Preferred Qualifications:
                * Experience with automation testing methodologies such as regression, functional, unit, integration, coverage, performance, and load testing
                * Background in testing applications that integrate through RESTful APIs
                * Familiarity with test management tools such as qTest, ALM, or TFS
                * Experience with API testing frameworks (Karate, Gatling, JMeter, Postman)
                * Exposure to load and performance testing
                * Knowledge of cloud platforms including AWS, Azure, Heroku, Perfecto Mobile, or SauceLabs
                * Experience reviewing code through pull requests
                * Understanding of Service-Oriented Architecture (SOA)
                ^D
                Captured 63 lines:
                Job Details
                Skills
                FOCUS
                Continuous Delivery
                Innovation
                ...
                * Understanding of Service-Oriented Architecture (SOA)
                
                Next:
                  job-intake-commit --app "/Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer"
                
                /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                ```
                
        - Commit the Intake
            
            ```java
            job-intake-commit --app "/Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer"
            ```
            
            - **Run #1 - Single Job**
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % job-intake-commit --app "/Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer"
                [main d9f869a] intake: kforce Lead (JD + tracking)
                 5 files changed, 91 insertions(+)
                 create mode 100644 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/jd/jd-raw.txt
                 create mode 100644 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/jd/job-post-url.txt
                 create mode 100644 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/application-record.json
                 create mode 100644 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/job-meta.json
                 create mode 100644 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/status-history.md
                Enter passphrase for key '/Users/olivermarroquin/.ssh/id_ed25519_github': 
                Enumerating objects: 16, done.
                Counting objects: 100% (16/16), done.
                Delta compression using up to 16 threads
                Compressing objects: 100% (12/12), done.
                Writing objects: 100% (14/14), 2.78 KiB | 2.78 MiB/s, done.
                Total 14 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
                remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
                To github.com:olivermarroquin/secondbrain.git
                   2fe625e..d9f869a  main -> main
                ## main...origin/main
                
                ```
                
        
        ---
        
    - Step 4 — Set APP var + verify job folder artifacts exist
        - Set APP var
            
            ```bash
            APP="<PASTE_APP_PATH_HERE>"
            ls -la "$APP"
            find "$APP" -maxdepth 2 -type f | sort
            python3 -m json.tool "$APP/tracking/job-meta.json" >/dev/null && echo "job-meta.json OK"
            python3 -m json.tool "$APP/tracking/application-record.json" >/dev/null && echo "application-record.json OK"
            wc -l "$APP/jd/jd-raw.txt"
            sed -n '1,5p' "$APP/jd/jd-raw.txt"
            ```
            
            **Success looks like**
            
            - Folder contains `jd/`, `tracking/`, `resume_refs/`
            - JSON validates
            - `jd-raw.txt` line count > 0
                
                ⬅️ Paste the output.
                
            - **Run #1 - Single Job**
                
                ```java
                APP="01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer"
                
                ls -la "$APP"
                find "$APP" -maxdepth 2 -type f | sort
                jobs-list-unapplied --date "$(date +%F)"
                ```
                
                What I Got:
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % APP="01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer"
                
                olivermarroquin@Olivers-MacBook-Pro secondbrain % ls -la "$APP"
                
                total 0
                drwxr-xr-x  6 olivermarroquin  staff  192 Feb  5 15:56 .
                drwxr-xr-x  3 olivermarroquin  staff   96 Feb  5 15:56 ..
                drwxr-xr-x  4 olivermarroquin  staff  128 Feb  5 15:56 jd
                drwxr-xr-x  2 olivermarroquin  staff   64 Feb  5 15:56 notes
                drwxr-xr-x  2 olivermarroquin  staff   64 Feb  5 15:56 resume_refs
                drwxr-xr-x  5 olivermarroquin  staff  160 Feb  5 15:56 tracking
                olivermarroquin@Olivers-MacBook-Pro secondbrain % find "$APP" -maxdepth 2 -type f | sort
                
                01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/jd/jd-raw.txt
                01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/jd/job-post-url.txt
                01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/application-record.json
                01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/job-meta.json
                01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/tracking/status-history.md
                olivermarroquin@Olivers-MacBook-Pro secondbrain % jobs-list-unapplied --date "$(date +%F)"
                  #  COMPANY               ROLE                                 FOUND       URL
                --------------------------------------------------------------------------------------------------------------
                  1  kforce                Lead Software Qa Engineer            2026-02-05  https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590…
                
                Total not_applied (date_found=2026-02-05): 1
                
                ```
                
        - Step 4A — Inspect unapplied jobs - Confirm job is in today’s not_applied list (date-scoped)
            
            ```bash
            jobs-list-unapplied --date "$D"
            ```
            
            **What this tells you**
            
            - Jobs found *today* and still `not_applied`
            - This is your **candidate workset**
            
            **If output is empty**, proceed to Step 4B.
            
            ⬅️ Paste output.
            
            ---
            
        - Step 4B — Inspect full unapplied backlog - If Step 4A is empty, check backlog unapplied (no date filter)
            
            ```bash
            jobs-list-unapplied
            ```
            
            **Decision checkpoint**
            
            - If jobs appear here but not in 4A → they’re older
            - Decide intentionally:
                - work backlog now
                - or leave untouched
            
            ⬅️ Paste output.
            
            ---
            
        - **🛑 NEXT STEPS: Resume Factory work happens HERE**
            
            This is where Steps 5–9 run **per job**:
            
            - Step 5 — resume-select
            - Step 6 — resume-preview
            - Step 7 — resume-suggest-edits
            - Step 8 — resume-approve-edits
            - Step 9 — manual review + submission
            
            🚫 **Do not mark applied yet.**
            
        
        ---
        
    - Step 5 — Resume template selection (read-only)
        
        ```bash
        resume-select --app "$APP"
        ```
        
        - **Success looks like**
            - Shows ranked templates + “Best pick” with template id/slug/path
            
            ⬅️ Paste the output.
            
        - **Run #1 - Single Job**
            
            ```java
            olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-select --app "$APP"
            APP: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
            JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05 | status=not_applied
            
            RANK  SCORE  TEMPLATE                          STACK                   WHY
            ------------------------------------------------------------------------------------------------------------------------
               1     42  04_typescript_playwright          typescript/playwright   pref: typescript, javascript | neut: api testing, postman, cypress
               2     30  02_java_playwright_migration      java/playwright         pref: java, framework | neut: api testing, postman
               3     26  03_python_playwright              python/playwright       pref: api testing, requests | neut: postman, aws, azure
               4     20  01_java_selenium                  java/selenium           pref: java | neut: api testing, postman
            
            Best pick:
            - template_id: 04
            - template_slug: 04_typescript_playwright
            - template_path: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
            ```
            
        
        ---
        
    - Step 6 — Resume preview sanity check (read-only)
        
        ```bash
        resume-preview --app "$APP"
        ```
        
        - **Success looks like**
            - Shows selected template info
            - Shows JD quick stats
            - Shows keyword hits
            - Prints heuristic preview sections without crashing
            
            ⬅️ Paste the output.
            
        - **Run #1 - Single Job**
            
            ```java
            olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-preview --app "$APP"
            
            APP: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
            JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05 | status=not_applied
            
            TEMPLATE (auto-selected):
            - template_id: 04
            - template_slug: 04_typescript_playwright
            - template_path: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
            - resume-master.docx: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright/resume-master.docx
            
            JD quick stats:
            - lines: 63
            - first: Job Details
            - last : * Understanding of Service-Oriented Architecture (SOA)
            
            Keyword hits (selected template):
            - preferred (2): typescript, javascript
            - neutral   (3): api testing, postman, cypress
            - anti      (0): -
            
            TEMPLATE PREVIEW: SUMMARY (heuristic)
            Dynamic and results-driven Senior Quality Assurance Engineer / SDET with over 7 years of hands-on experience in manual and
            automation testing for web, API, and mobile applications. Proven expertise in architecting and implementing scalable end-to-end automation frameworks using Playwright with Typescript, reducing test execution time by 70% while improving stability, reliability, and defect detection across critical user workflows.
            Strong background in designing and maintaining TypeScript-based Playwright Test frameworks for UI and API automation, leveraging native Playwright capabilities such as auto-waiting, parallel execution, and cross-browser testing. Experienced in supporting and maintaining legacy Java and Selenium-based backend test suites, while driving modernization efforts through Playwright adoption and shift-left testing strategies.
            Highly skilled in CI/CD integration, cloud-based testing, and test orchestration, delivering maintainable automation solutions using TypeScript, Playwright Test, Node.js, and modern CI tooling. Proficient in integrating automation workflows with Jenkins, GitHub Actions, and AWS, and leveraging tools such as Postman, JMeter, and BrowserStack for comprehensive end-to-end validation, performance testing, and cross-platform coverage.
            Demonstrated expertise in REST API testing, mobile testing with Appium, and database validation across SQL Server, PostgreSQL, and Oracle. A collaborative team player with a proven ability to lead, mentor, and drive QA initiatives in Agile and fast-paced environments, ensuring testing standards, visibility, and continuous quality improvement throughout the SDLC.
            TECHNICAL SKILL:
            Automation Frameworks: Playwright (TypeScript), Playwright Test, Selenium WebDriver, Rest Assured, Cucumber
            Programming Languages: TypeScript, JavaScript, SQL, Java
            ETL & Databases: SQL Server, Oracle, PostgreSQL, MongoDB
            Networking & Protocols: HTTP/HTTPS, REST, JSON, TCP/IP, DNS
            
            TEMPLATE PREVIEW: SKILLS (heuristic)
            (not found by heading heuristic)
            
            TEMPLATE PREVIEW: EXPERIENCE (heuristic)
            Sr. Test Automation Engineer           Food and Drug Administration, MD.                 Jul 2021 -- Present
            Roles and Responsibilities:
            - Architected and implemented a TypeScript-based API automation framework leveraging Playwright’s native request context to validate distributed microservices, achieving 90% API test coverage and ensuring data integrity through real-time validation logic.
            - Developed an end-to-end automation framework using Playwright (TypeScript) for web and mobile workflows, supporting cross-browser and device validation and reducing overall testing time by 70% while improving cross-platform accuracy.
            - Enhanced REST and GraphQL API automation using Playwright and Postman, implementing schema validation, data mocking, and request-level assertions to support IoT microservices testing.
            - Integrated automation workflows with GitHub Actions and Jenkins CI/CD pipelines, enabling automated build verification on every code push.
            - Conducted performance testing with JMeter and Locust to validate scalability and responsiveness under high-load conditions.
            - Performed mobile application testing with Appium across Android and iOS devices to ensure consistent UI behavior and performance.
            - Designed and implemented a Jenkins-based continuous testing pipeline with prioritized and parallel Playwright test execution, reducing deployment validation time from 4 hours to 90 minutes.
            - Leveraged AWS CloudWatch and application logs to monitor distributed test executions, analyze failures, and identify API performance bottlenecks.
            - Created custom reporting solutions integrating TestRail, JIRA, and Slack for real-time insights and proactive issue tracking.
            - Led and mentored a team of 3 junior QA engineers, promoting best practices in TypeScript-based automation, Agile testing, and continuous quality improvement, resulting in a 30% increase in script development efficiency.
            - Conducted database testing by executing complex SQL queries to validate backend data integrity and performance.
            Test Automation Engineer                             Microsoft, WA                                             Dec 2019 -- Jul 2021
            Roles and Responsibilities:
            - Analyzed requirement specifications, developed test plans, test cases, and automation strategies, and defined QA methodologies within an Agile delivery environment.
            - Developed and implemented an end-to-end automation framework using Playwright with TypeScript, automating 200+ functional and integration scenarios to ensure scalable, maintainable coverage across web and API workflows.
            - Designed and implemented data-driven Playwright tests to automate regression validation across 5+ major releases, improving overall automation coverage by 30%.
            
            NOTE:
            - This is READ-ONLY: no files written.
            - If headings aren't detected in your DOCX, we’ll add a template-specific locator map next.
            ```
            
        
        ---
        
    - Step 7 — Generate numbered change proposals (writes proposals JSON)
        - Ask for the suggested Edits
            
            ```bash
            resume-suggest-edits --app "$APP" --diff
            
            #checks to see if the document was created
            ls -l "$APP/resume_refs/edit-proposals.json"
            
            #Checks if it compiles
            python3 -m json.tool "$APP/resume_refs/edit-proposals.json" >/dev/null && echo "edit-proposals.json OK"
            ```
            
            - **Success looks like**
                - Terminal prints numbered proposals with BEFORE/AFTER
                - `edit-proposals.json` exists and validates
                
                ⬅️ Paste the output.
                
            - **Run #1 - Single Job**
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-suggest-edits --app "$APP" --diff
                
                APP: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05
                TEMPLATE (selected): 04 04_typescript_playwright
                TEMPLATE PATH: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
                
                JD TERMS (gate): api, java, agile, typescript, javascript, end-to-end, restful, cypress, postman, jmeter, azure, aws, qa, service-oriented, phoenix-based, az/mst, and/or
                
                JD TERMS (missing-only gate): restful, cypress, service-oriented, phoenix-based, az/mst, and/or
                
                JD TERMS (run gate): restful, cypress, service-oriented, phoenix-based, az/mst, and/or
                
                NOTE: dropped 5 unsafe proposal(s).
                  - [EXPERIENCE] duplicate_jd_term_in_run: Expanded framework capabilities with Playwright-native API testing, validating REST endpoints for data consistency, lat…
                  - [EXPERIENCE] target_is_role_header_line: Sr. Test Automation Engineer           Food and Drug Administration, MD.                 Jul 2021 -- Present
                  - [EXPERIENCE] duplicate_before_ref_in_run: Architected and implemented a TypeScript-based API automation framework leveraging Playwright’s native request context …
                  - [EXPERIENCE] duplicate_before_ref_in_run: Architected and implemented a TypeScript-based API automation framework leveraging Playwright’s native request context …
                  - [EXPERIENCE] duplicate_before_ref_in_run: Conducted performance testing with JMeter and Locust to validate scalability and responsiveness under high-load conditi…
                
                Proposed localized edits (READ-ONLY):
                
                1. [EXPERIENCE] REPLACE_LINE
                   why: JD mentions RESTful; align resume to JD requirement. Enhanced the automation framework by explicitly referencing RESTful services.
                   BEFORE:
                   - Architected and implemented a TypeScript-based API automation framework leveraging Playwright’s native request context to validate distributed microservices, achieving 90% API test coverage and ensuring data integrity through real-time validation logic.
                   AFTER:
                   + Architected and implemented a TypeScript-based API automation framework leveraging Playwright’s native request context, RESTful services, and Postman for validating distributed microservices, achieving 90% API test coverage and ensuring data integrity through real-time validation logic.
                
                2. [EXPERIENCE] REPLACE_LINE
                   why: JD mentions Cypress; align resume to JD requirement. Incorporated Cypress as part of the framework for enhanced automation.
                   BEFORE:
                   - Developed and implemented an end-to-end automation framework using Playwright with TypeScript, automating 200+ functional and integration scenarios to ensure scalable, maintainable coverage across web and API workflows.
                   AFTER:
                   + Developed and implemented an end-to-end automation framework using Playwright with TypeScript, leveraging Cypress to automate 200+ functional and integration scenarios for scalable coverage across web and API workflows.
                
                3. [EXPERIENCE] REPLACE_LINE
                   why: JD mentions load testing; align resume to JD requirement. Specify load testing to meet performance validation.
                   BEFORE:
                   - Conducted performance testing with JMeter and Locust to validate scalability and responsiveness under high-load conditions.
                   AFTER:
                   + Conducted load testing and performance testing using JMeter to validate scalability and responsiveness under high-load conditions.
                
                Wrote proposals: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/edit-proposals.json
                ```
                
        - Re-run later if you want more of the keywords (This funtionality needs fixing to compound edits)
        - If you want to make **No Changes** to the resume or if ‘None’ appear, you can open the job-app url that you want like this
            - The correct command (do this)
                - **For later** (you want to create this)
                    
                    ```bash
                    jobs-open --app 01_projects/jobs/qa_automation_engineer/inspyr_solutions/2026-02-05_quality-assurance-engineer
                    ```
                    
                    ## 🔧 Enhancement we should add later (you were right)
                    
                    You’ve now hit this pain **multiple times**, so it’s real:
                    
                    **Proposed command (future):**
                    
                    ```bash
                    jobs-open --app <path>
                    ```
                    
                    Implementation would literally be:
                    
                    ```bash
                    open "$(cat "$APP/jd/job-post-url.txt")"
                    ```
                    
                    Low effort, high value. We’ll add it to the enhancement list you asked me to remember.
                    
                    That will:
                    
                    - Read **only** this file:
                        
                        ```
                        jd/job-post-url.txt
                        ```
                        
                    - Open **only** the INSPYR Dice URL
                    - Ignore batch order, queues, or other unapplied jobs
                - But **for now,** you can use this:
                    
                    ```java
                    open "$(cat 01_projects/jobs/qa_automation_engineer/inspyr_solutions/2026-02-05_quality-assurance-engineer/jd/job-post-url.txt)"
                    ```
                    
                
                ---
                
            - If you want to verify before opening (optional)
                
                ```bash
                cat 01_projects/jobs/qa_automation_engineer/inspyr_solutions/2026-02-05_quality-assurance-engineer/jd/job-post-url.txt
                ```
                
                You should see:
                
                ```
                https://www.dice.com/job-detail/9cc26130-6290-4377-9af5-f22f5f7ae48c
                ```
                
                If that’s correct, then:
                
                ```bash
                open "$(cat 01_projects/jobs/qa_automation_engineer/inspyr_solutions/2026-02-05_quality-assurance-engineer/jd/job-post-url.txt)"
                ```
                
                ---
                
            - Why batch kept opening the “wrong” job (important)
                - `jobs-apply-batch` **never** means “the job I just worked on”
                - It means: *first N unapplied jobs in sorted order*
                - Resume work does **not** influence apply order
                
                So nothing was broken — you just used the **wrong abstraction** for a targeted apply.
                
                ---
                
            - After you apply in the browser
                
                Then you do **exactly** this:
                
                ```bash
                jobs-mark-applied-last --date "2026-02-05" --apply --commit
                git push
                ```
                
                ---
                
                ### Rule to remember (burn this in)
                
                - **One job → use `jobs-open --app`**
                - **Many jobs → use `jobs-apply-batch`**
        - To add a note in the /tracking/status-history.md file for you to read later:
            
            ```java
            echo "- Applied via Dice on 2026-02-05. Role is Tosca-heavy; resume aligned but low Tosca depth." >> \
            01_projects/jobs/qa_automation_engineer/inspyr_solutions/2026-02-05_quality-assurance-engineer/tracking/status-history.md
            ```
            
        
        ---
        
    - Step 8 — Apply ONLY approved changes (writes final DOCX + applied log)
        - **Option A: apply all proposals**
            
            ```bash
            resume-approve-edits --app "$APP" --force --open
            ```
            
        - **Option B: apply selected proposals only (example IDs)**
            
            ```bash
            resume-approve-edits --app "$APP" --numbers 1 3 5 --force --open
            ```
            
        - Then verify:
            
            ```bash
            #Checks to see if file exists
            ls -l "$APP/resume_refs/resume.docx"
            
            #Checks to see what other files exist in that folder: should see 'edit-proposals.json', 'edits-applied.json', and 'resume.docx'
            ls -l "$APP/resume_refs"
            ```
            
            - **Success looks like**
                - `resume_refs/resume.docx` created
                - `resume_refs/edits-applied.json` created
                - Output shows APPLIED count and FAILED count
                
                ⬅️ Paste the output.
                
                - **Run #1**
                    
                    ```java
                    olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-approve-edits --app "$APP" --force --open
                    APP: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                    JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05 | status=not_applied
                    
                    TEMPLATE:
                    - template_id: 04
                    - template_slug: 04_typescript_playwright
                    - template_path: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
                    - resume-master.docx: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright/resume-master.docx
                    
                    Proposals selected: 3 of 3
                    
                    APPLIED: 3
                    - 1. [EXPERIENCE] REPLACE_LINE
                    - 2. [EXPERIENCE] REPLACE_LINE
                    - 3. [EXPERIENCE] REPLACE_LINE
                    
                    FAILED: 0
                    
                    WROTE: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/resume.docx
                    WROTE: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/edits-applied.json
                    ```
                    
        - 👉🏽 Re-run suggestions to see if anything is still missing (This needs fixing as the suggested edits aren’t compiling, starts from the template level, so other suggested edits are lost)
            
            Run:
            
            ```bash
            resume-suggest-edits --app "$APP" --diff
            ```
            
            Paste the output **only**.
            
            If it returns **0 proposals**, we immediately move to the apply phase.
            
            - **Run #1 - Single Job**
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-suggest-edits --app "$APP" --diff
                
                APP: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05
                TEMPLATE (selected): 04 04_typescript_playwright
                TEMPLATE PATH: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
                
                JD TERMS (gate): api, java, agile, end-to-end, typescript, javascript, cypress, postman, restful, jmeter, azure, aws, qa, service-oriented, phoenix-based, and/or, az/mst
                
                JD TERMS (missing-only gate): cypress, restful, service-oriented, phoenix-based, and/or, az/mst
                
                JD TERMS (run gate): service-oriented, phoenix-based, and/or, az/mst
                
                NOTE: dropped 3 unsafe proposal(s).
                  - [EXPERIENCE] target_is_role_header_line: Sr. Test Automation Engineer           Food and Drug Administration, MD.                 Jul 2021 -- Present
                  - [EXPERIENCE] jd_term_already_present_in_resume: Conducted performance testing with JMeter and Locust to validate scalability and responsiveness under high-load conditi…
                  - [EXPERIENCE] target_is_resume_heading: PROFESSIONAL EXPERIENCE:
                
                Proposed localized edits (READ-ONLY):
                
                1. [EXPERIENCE] REPLACE_LINE
                   why: JD mentions service-oriented; align resume to JD requirement.
                   BEFORE:
                   - Designed and implemented data-driven Playwright tests to automate regression validation across 5+ major releases, improving overall automation coverage by 30%.
                   AFTER:
                   + Designed and implemented data-driven Playwright tests focusing on regression validation and service-oriented architecture across 5+ major releases, improving overall automation coverage by 30%.
                
                2. [EXPERIENCE] REPLACE_LINE
                   why: JD mentions AZ/MST; align resume to JD requirement.
                   BEFORE:
                   - Leveraged Jenkins for continuous integration and Python-based performance testing with Locust, significantly reducing manual regression efforts and improving response-time visibility.
                   AFTER:
                   + Leveraged Jenkins for continuous integration, integrating with Azure for performance testing and reducing manual regression efforts while improving response-time visibility.
                
                Wrote proposals: 01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/edit-proposals.json
                ```
                
        - 👉🏽 Re-apply only the proposals you want (This needs fixing as the suggested edits aren’t compiling, starts from the template level, so other suggested edits are lost)
            
            ```java
            resume-approve-edits --app "$APP" --numbers 1 --force --open
            ```
            
            - **Run #1 - Single Job**
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % resume-approve-edits --app "$APP" --number 1 --force --open
                APP: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                JOB: kforce | Lead Software Qa Engineer | date_found=2026-02-05 | status=not_applied
                
                TEMPLATE:
                - template_id: 04
                - template_slug: 04_typescript_playwright
                - template_path: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright
                - resume-master.docx: /Users/olivermarroquin/secondbrain/03_assets/templates/resumes/qa_automation_engineer/04_typescript_playwright/resume-master.docx
                
                Proposals selected: 1 of 2
                
                APPLIED: 1
                - 1. [EXPERIENCE] REPLACE_LINE
                
                FAILED: 0
                
                WROTE: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/resume.docx
                WROTE: /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer/resume_refs/edits-applied.json
                ```
                
        
        ---
        
    - **Step 9 — 🔄 APPLY TO JOBS**
        - Step 9a — Open jobs into active work queue
            - Open & Apply to All Jobs By Batch Date
                
                ```bash
                jobs-apply-batch --date "$D"
                ```
                
                (omit `--date "$D"` if intentionally working backlog)
                
                **What this does**
                
                - Opens jobs for processing
                - Does **not** mark them applied
                - Creates a working queue
                
                ⬅️ Paste output.
                
            - Open & Apply to 25 Jobs By Batch Date (Open an application batch)
                - Dry-run first
                    
                    ```bash
                    jobs-apply-batch 25 --batch auto --date "$D" --dry-run
                    ```
                    
                    **Success:** it prints the queue file path (e.g. `/tmp/applied-$D-batch1.txt`) and what it WOULD open.
                    
                    **Success looks like:** it prints what it *would* open + queue file path it *would* use (typically `/tmp/applied-$D-batch*.txt`)
                    
                - Real open (writes queue file)
                    
                    ```bash
                    jobs-apply-batch 25 --batch auto --date "$D"
                    ```
                    
                    **Success:** browser opens; queue file is written; command prints the exact queue file path.
                    
                - Show current queue (optional but recommended)
                    
                    Even though `jobs-mark-applied-last` will show the queue, I want this as a standalone sanity check:
                    
                    ```bash
                    jobs-queue-show
                    ```
                    
                - Scenario: If you opened 25 but only applied to 18: prune the queue
                    
                    This is exactly where `jobs-queue-prune` belongs: **after applying, before marking applied**.
                    
                    ```bash
                    jobs-queue-prune
                    ```
                    
                    Then verify the queue is now correct:
                    
                    ```bash
                    jobs-queue-show
                    ```
                    
                    **Success looks like:** queue shows only the applied jobs you actually submitted.
                    
                    > This matches your stated purpose: prune by number without manual file editing, with guardrails.
                    > 
                
                ---
                
                If something goes wrong with the queue:
                
                - Show the queue (MUST pass queue path)
                    
                    We need the exact queue path. Since behavior guarantees it, compute it like this:
                    
                    ```bash
                    Q="/tmp/applied-$D-batch1.txt"
                    ls -l "$Q"
                    jobs-queue-show "$Q"
                    ```
                    
                    ⚠️ If `--batch auto` chose a batch number other than 1, this path will be different. The safe way is: **read it from the output of jobs-apply-batch** and set `Q` to that. (You paste output, I tell you the exact Q.)
                    
                - Prune queue (ONLY if partial applied)
                    
                    ```bash
                    jobs-queue-prune "$Q"
                    jobs-queue-show "$Q"
                    ```
                    
            
            ---
            
        - Step 9b — Inspect the active queue
            - Inspect all jobs in the queue
                
                ```bash
                jobs-queue-show
                ```
                
                **Success looks like**
                
                - You see the jobs you intend to work on
                - Paths match expected job folders
                
                ⬅️ Paste output.
                
    - Step 10 — Mark job “applied” only after you actually submit
        
        Checkpoint supports “batch marking” via queue tooling. For a **single job**, we’ll do this safely:
        
        - Step 10a — DRYRUN mark-applied-last (built-in safety)
            
            This is your “final truth check” before flipping statuses:
            
            ```bash
            jobs-mark-applied-last --date "$D"
            ```
            
            Per help: default behavior is to resolve newest queue, show it, and DRYRUN mark unless `--apply`.
            
            - **Run #1 - Single Job**
                
                ```java
                olivermarroquin@Olivers-MacBook-Pro secondbrain % jobs-mark-applied-last --date "2026-02-05"
                
                Resolved date : 2026-02-05
                Queue file    : /tmp/applied-2026-02-05-batch2.txt
                
                No.  Company              Role                                Found      URL
                ---- -------------------- ----------------------------------- ---------- ----
                1    kforce               Lead Software Qa Engineer           2026-02-05 https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e
                
                Mark applied preview:
                MODE     COUNT  DETAILS
                DRYRUN       1  to-change
                             0  skipped
                
                Will mark APPLIED:
                - kforce | Lead Software Qa Engineer | https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e
                  /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                
                Dry run only. Re-run with --apply to write changes.
                ```
                
        - Step 10b — ACTUAL Mark jobs as “applied”
            - Manual Steps: For Single Job (Optional)
                1. Create a one-line queue file (non-destructive):
                    
                    ```bash
                    Q="/tmp/applied-$D-goldenrun.txt"
                    printf "%s\n" "$APP" > "$Q"
                    ls -l "$Q"
                    cat "$Q"
                    ```
                    
                2. Mark applied (this uses your existing status mechanism; no guessing):
                    
                    ```bash
                    jobs-batch-mark-applied --date "$D" --paths-file "$Q" --apply --commit --message "status: applied ($D) golden run"
                    git push
                    ```
                    
                3. Verify status updated:
                    
                    ```bash
                    python3 -m json.tool "$APP/tracking/job-meta.json" | sed -n '1,80p'
                    jobs-list-unapplied --date "$D"
                    ```
                    
                
                **Success looks like**
                
                - Status flips to applied in tracking JSON
                - Job disappears from “unapplied” list for today
                
                ⬅️ Paste the output.
                
            - Batch-Jobs (Single or multiple)
                - Mark Applied (and optionally commit/push) - can be used for 1 or for multiple jobs
                    - If everything in the queue is truly applied (date specific):
                        
                        ```bash
                        jobs-mark-applied-last --date "$D" --apply --commit --push --message "status: batch -> applied ($D) last"
                        ```
                        
                        OR
                        
                        ```bash
                        jobs-mark-applied-last \
                          --date "$D" \
                          --commit \
                          --message "status: applied ($D)"
                        git push
                        ```
                        
                        **Only valid if**
                        
                        - Every job in the last batch was actually submitted
                        
                        **Success looks like:** it updates job tracking statuses, commits, and pushes.
                        
                    - Mark last opened batch (fast, only if all were applied, including backlog)
                        
                        Mark last queue (best when you applied to all opened)
                        
                        ```java
                        jobs-mark-applied-last
                        jobs-mark-applied-last --apply --commit
                        git push
                        ```
                        
                - Quick Sanity Check: Inspect the queue you’re about to mark applied
                    
                    Use the exact queue file path printed above (example shown):
                    
                    ```bash
                    jobs-queue-show "/tmp/applied-$D-batch1.txt"
                    ```
                    
                    **Success:** it shows the jobs in a readable table; you can sanity-check “did I just open what I intended?”
                    
                - Option B — If you opened 25 but only applied to 18: prune BEFORE marking applied
                    - Step B.1 — First confirm whether `jobs-queue-prune` actually exists
                        
                        Run:
                        
                        ```bash
                        which jobs-queue-prune || echo "NO jobs-queue-prune on PATH"
                        ls -la ~/secondbrain/07_system/bin | grep -n "jobs-queue-prune" || true
                        ```
                        
                        - If it exists → use it (Step 9C.1)
                        - If it doesn’t → fall back to the Q2 applied-only file method (Step 9C.2)
                    - Step B.2 — (If available) Interactive prune (removes the ones you didn’t apply to)
                        
                        **Placement:** right after `jobs-queue-show`, before any marking.
                        
                        Example (you’ll use your tool’s real syntax):
                        
                        ```bash
                        jobs-queue-prune "/tmp/applied-$D-batch1.txt"
                        jobs-queue-show "/tmp/applied-$D-batch1.txt"
                        ```
                        
                        **Success:** queue is rewritten to contain only the applied ones; re-show confirms.
                        
                        > If your `jobs-queue-prune` syntax differs, paste the output of `jobs-queue-prune --help` and I’ll wire it exactly.
                        > 
                    - Step B.3 — (Fallback) Create applied-only queue file (manual but safe)
                        
                        ```bash
                        Q2="/tmp/applied-$D-batch1-applied-only.txt"
                        : >"$Q2"
                        cat >> "$Q2"
                        # paste ONLY applied APP paths, one per line
                        # Ctrl-D
                        wc -l "$Q2"
                        sed -n '1,200p' "$Q2"
                        ```
                        
                    - Mark using your applied-only queue file (when partial applied)
                        
                        ```java
                        jobs-batch-mark-applied --date "$D" --paths-file "$Q2" --apply --commit --message "status: batch -> applied ($D) batch1 applied-only"
                        git push
                        ```
                        
                - Option C — Mark a subset
                    
                    ```bash
                    Q2="/tmp/applied-$D-applied-only.txt"
                    : >"$Q2"
                    ```
                    
                    Add only applied APP paths:
                    
                    ```bash
                    cat >> "$Q2"
                    # paste paths
                    # Ctrl-D
                    ```
                    
                    Verify:
                    
                    ```bash
                    wc -l"$Q2"
                    sed -n'1,200p'"$Q2"
                    ```
                    
                    Mark applied:
                    
                    ```bash
                    jobs-batch-mark-applied \
                      --date "$D" \
                      --paths-file "$Q2" \
                      --apply \
                      --commit \
                      --message "status: batch -> applied ($D)"
                    git push
                    ```
                    
                - Run #1
                    
                    ```java
                    olivermarroquin@Olivers-MacBook-Pro secondbrain % jobs-mark-applied-last --date "2026-02-05" --apply --commit --push --message "status: applied (2026-02-05) kforce Lead Software QA Engineer"
                    
                    Resolved date : 2026-02-05
                    Queue file    : /tmp/applied-2026-02-05-batch2.txt
                    
                    No.  Company              Role                                Found      URL
                    ---- -------------------- ----------------------------------- ---------- ----
                    1    kforce               Lead Software Qa Engineer           2026-02-05 https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e
                    
                    Mark applied preview:
                    MODE     COUNT  DETAILS
                    DRYRUN       1  to-change
                                 0  skipped
                    
                    Will mark APPLIED:
                    - kforce | Lead Software Qa Engineer | https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e
                      /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                    
                    Type APPLY to mark these jobs as applied: APPLY
                    MODE     COUNT  DETAILS
                    APPLY        1  to-change
                                 0  skipped
                    
                    Will mark APPLIED:
                    - kforce | Lead Software Qa Engineer | https://www.dice.com/job-detail/f37066fb-9587-4bbb-b220-590ee268994e
                      /Users/olivermarroquin/secondbrain/01_projects/jobs/qa_automation_engineer/kforce/2026-02-05_lead-software-qa-engineer
                    [main 5e5a9df] status: applied (2026-02-05) kforce Lead Software QA Engineer
                     3 files changed, 13 insertions(+), 4 deletions(-)
                    Enter passphrase for key '/Users/olivermarroquin/.ssh/id_ed25519_github': 
                    Enumerating objects: 21, done.
                    Counting objects: 100% (21/21), done.
                    Delta compression using up to 16 threads
                    Compressing objects: 100% (9/9), done.
                    Writing objects: 100% (11/11), 1.04 KiB | 1.04 MiB/s, done.
                    Total 11 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
                    remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
                    To github.com:olivermarroquin/secondbrain.git
                       8c74b4b..5e5a9df  main -> main
                    
                    ```
                    
        - Step 10c — Post-apply verification (Verify remaining work)
            
            ```bash
            jobs-list-unapplied --date "$D"
            jobs-queue-show
            ```
            
            **Success**
            
            - Applied jobs disappear from unapplied list
            - Queue reflects reality
            
            ⬅️ Paste output.
            
        
        ---
        
    - Step 11 — End-of-session close (protocol boundary)
        
        ```bash
        cd ~/secondbrain
        git status -sb
        session-close
        git status -sb
        ```
        
        **Success looks like**
        
        - After any required commits/pushes, working tree is clean/understood
        
        ⬅️ Paste the output.
        
        - **Run #1 - Single Job**
            
            ```java
            session-close
            
            git add 07_system/state/LOG.md
            git commit -m "chore(session): close golden run job application session"
            git push
            ```
            
            What I Got:
            
            ```java
            olivermarroquin@Olivers-MacBook-Pro secondbrain % session-close
            
            == Session close ==
            
            Appending to 07_system/state/LOG.md ...
            
            Update NEXT.md (task #0 rule) then STATUS.md.
            Opening NEXT.md...
            Opening STATUS.md...
            
            == Git status ==
            ## main...origin/main
             M 07_system/state/LOG.md
            
            Reminder:
            - If ready: git add -p && git commit -m "..." && git push
            - If not ready: write why in NEXT.md before stopping.
            
            olivermarroquin@Olivers-MacBook-Pro secondbrain % git add 07_system/state/LOG.md
            git commit -m "chore(session): close golden run job application session"
            git push
            
            [main f2da617] chore(session): close golden run job application session
             1 file changed, 5 insertions(+)
            Enter passphrase for key '/Users/olivermarroquin/.ssh/id_ed25519_github': 
            Enumerating objects: 9, done.
            Counting objects: 100% (9/9), done.
            Delta compression using up to 16 threads
            Compressing objects: 100% (5/5), done.
            Writing objects: 100% (5/5), 460 bytes | 460.00 KiB/s, done.
            Total 5 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
            remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
            To github.com:olivermarroquin/secondbrain.git
               5e5a9df..f2da617  main -> main
            olivermarroquin@Olivers-MacBook-Pro secondbrain % 
            
            ```
