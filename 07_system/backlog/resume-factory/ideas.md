Ideas for Enhancement:

- 1) AI-Agent Orchestration Roadmap (End-to-End Job Pipeline)
    
    ### Goal
    
    Maximize automation across the job pipeline while keeping **operator control, auditability, and deterministic artifacts** (no silent mutations).
    
    ### Proposed agent roles (separable, composable)
    
    1. **Job Discovery Agent**
        - Searches for jobs that match constraints (remote, non-government, no clearance, etc.)
        - Outputs: curated list of links + extracted metadata (company, title, location, type, pay if available)
        - Must support scoring/ranking and “why this matches” notes
    2. **Intake Agent**
        - For each selected job link, runs intake and captures JD reliably (clipboard/file fetch), including URL and normalized company/role slugging
        - Outputs: populated job folder + standard tracking files
    3. **Intake Verifier Agent**
        - Validates folder completeness and schema correctness
        - Checks: JD captured fully, URLs present, tracking files consistent, no partial/corrupt writes
        - Outputs: pass/fail report + fix instructions (or auto-fix in “suggest-only” mode)
    4. **Resume Tailoring Agent**
        - Runs template selection + suggestion generation
        - Evaluates edit proposals for **semantic quality** (no keyword stuffing, no nonsense phrasing)
        - When proposals are awkward, rewrites them into clean, role-appropriate language while preserving truthfulness
        - Outputs: final set of edits ready for approval + explanation
    5. **Pre-Apply Readiness Agent**
        - Confirms that `resume_refs/resume.docx` exists, opens correctly, and is the intended version for upload
        - Checks that resume matches the target job (correct company/job folder, correct date, correct template stack)
    6. **Cover Letter Agent**
        - Generates cover letters tied to the same job folder state
        - Outputs: `cover_letter.docx` (or markdown + docx export) + optional shorter “application text” snippet
    7. **Post-Apply Status Agent**
        - After you confirm “applied,” updates status consistently across tracking files and logs the action
        - Outputs: clean git diff + commit message suggestion
    
    ### Non-negotiables
    
    - No agent is allowed to mutate state without:
        - explicit approval step, or
        - a “write gate” flag
    - Every action must be reproducible and leave an audit trail (diffs, logs, deterministic outputs).
    
    ---
    
- 2) Resume Output Quality Agent (Semantic QA for Generated resume.docx)
    
    ### Problem
    
    `resume-suggest-edits` can propose keyword-aligned edits that read awkwardly or insert meaningless phrasing. Manual cleanup is currently required.
    
    ### Requirement
    
    Add an AI check after `resume-approve-edits` that:
    
    - reviews `resume_refs/resume.docx` (or extracted text)
    - flags low-quality edits (grammar, semantic weirdness, keyword stuffing, contradictions)
    - proposes improved rewrites that preserve meaning and truthfulness
    - optionally produces a second-pass patch set
    
    ### Acceptance criteria
    
    - The agent must produce:
        - a short “quality report” (what changed and why)
        - a patch proposal file compatible with the existing approval workflow
    - Must not invent experience; rewrites must be truth-preserving.
    
    ---
    
- 3) Keyword Memory + Compounding Term Library (Beyond Hardcoded Lists)
    
    ### Problem
    
    JD term extraction is limited by current allowlists/filters. Valuable tools/terms in JDs don’t get promoted reliably, and the system can’t “learn” across runs.
    
    ### Requirement
    
    Create a persistent “term memory” system:
    
    - When a JD is analyzed, store:
        - high-signal keywords/phrases found in JD
        - which ones are missing from the resume baseline
        - which ones were used successfully in applied edits
    - Build a compounding library (per role family + optionally per stack)
    
    ### Example behavior
    
    From a JD like Kforce:
    
    - Terms like `qTest`, `TFS`, `Karate`, `Gatling`, `Heroku`, `Perfecto`, `SauceLabs`, `pull requests` should be captured even if not in the original allowlist.
    - Next runs can consider these terms for suggestions (with guardrails to avoid junk).
    
    ### Acceptance criteria
    
    - Terms are stored in a deterministic file (e.g., `terms/global.json` + `terms/qa_automation_engineer.json`)
    - Term promotion is gated:
        - only store terms that meet quality thresholds (frequency, capitalization pattern, known tool dictionaries, etc.)
    - Terms can be reviewed/pruned (human-in-the-loop).
    
    ---
    
- 4) Smarter Missing-Only Gate (Contextual Importance > “Exists Anywhere”)
    
    ### Problem
    
    The current “missing-only” logic treats a term as satisfied if it appears anywhere on the resume. But for hiring impact, some terms need to appear in **Experience** even if they exist in **Skills**.
    
    ### Requirement
    
    Add section-aware gating rules:
    
    - If JD emphasizes a term (e.g., AWS/Azure), require it in **Experience** (or Summary + Experience), not just Skills.
    - Allow per-term “preferred placement” policies:
        - `AWS`: must appear in Experience
        - `Postman`: Experience or Skills acceptable
        - `qTest`: Skills acceptable unless JD emphasizes test management heavily
    
    ### Acceptance criteria
    
    - The tool should explain *why* it considers a term “still missing” (e.g., “present in Skills only; JD emphasis requires Experience mention”).
    
    ---
    
- 5) Incremental Editing Across Runs (Stateful Accumulation Without Losing Prior Work)
    
    ### Problem (stated cleanly)
    
    Repeated `resume-suggest-edits` runs are currently **stateless** with respect to the generated resume. They reason against the template baseline, so:
    
    - you can’t naturally “add Cypress on top of earlier RESTful edits”
    - re-runs don’t accumulate
    - manual edits get overwritten by regeneration
    
    ### Requirement
    
    Introduce an optional incremental mode:
    
    - `resume-suggest-edits` and `resume-approve-edits` can target:
        - **template baseline** (current behavior; deterministic)
        - **current resume_refs/resume.docx** as the base (new behavior)
    
    ### Implementation constraint (keep determinism)
    
    - Determinism is preserved by making the base explicit:
        - `-base template` (default)
        - `-base resume_refs/resume.docx`
    - The system must record which base was used in metadata.
    
    ### Acceptance criteria
    
    - You can re-run suggestions and apply them onto the current resume without losing prior applied edits.
    - Manual edits remain risky, but the system no longer nukes changes just because you re-ran.
    
    ---
    
- 6) Your “Non-Negotiable Rule” (Reworded as a Constraint)
    
    Here’s the same idea, written as an engineering constraint (less absolute, more accurate):
    
    **Current constraint (today’s system):**
    
    - `resume-suggest-edits` compares **JD ↔ template baseline**, not **JD ↔ generated resume**
    - Therefore, multiple runs are best treated as **proposal discovery**, not additive editing
    - If you regenerate, you risk overwriting manual changes unless you reapply everything intentionally
    
    **Desired future constraint:**
    
    - The system should support an explicit incremental base so repeated runs can accumulate safely.


--------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------


- **R&R change** I also want: Your “Roles & Responsibilities” (R&R) problem: what v2 is doing and what to port
    - Breakdown of R&R Goal
        
        In **secondbrain_v2**, the R&R targeting is not magic AI. It’s a **data contract**:
        
        - `rf_family_init.py` creates/ensures `section-aliases.json` including a **subsection** key:
            - `ROLES_AND_RESPONSIBILITIES`: `["Roles and Responsibilities:"]`
        - `rf_propose_changes_ai.py` forwards `-rr-occurrence` into `rf_agent_runner.py`
        - `rf_agent_runner.py` stores:
            - `SUBSECTION: ROLES_AND_RESPONSIBILITIES`
            - `SUBSECTION_OCCURRENCE: <rr_occurrence>`
        - Later, materialization uses that metadata to apply changes into the correct R&R block.
        
        **Your current repo (this chat’s version) has none of that sub-structure**, because `rf_docx_extract.py` only emits:
        
        - section = HEADER/SUMMARY/SKILLS/EXPERIENCE
        - line refs = E###, etc.
            
            So “R&R per job” literally doesn’t exist as an addressable concept yet.
            
    - Plan to add R&R targeting to *this* repo (minimal, deterministic, no redesign)
        - Phase 0 — unblock apply (must do)
            - Repair `apply_replace_line()` and remove the unreachable/duplicated code.
            - Add 2 prints in approve step (low-risk observability):
                - Print when refusing overwrite (already does)
                - Print **right before open**: `print(f"OPENING: {out_docx}")`
        - Phase 1 — detect R&R blocks deterministically in `rf_docx_extract.py`
            
            Add a lightweight pass inside EXPERIENCE that:
            
            - identifies lines equal to (or starting with) `"Roles and Responsibilities:"` (case-insensitive, colon-tolerant)
            - increments an `rr_occurrence` counter each time it hits that marker
            - annotates each subsequent experience line until the next major boundary (next job header, next “Roles and Responsibilities:”, or end)
            
            **Output change:** keep the current `line_index[ref] = {"section": ..., "text": ...}` but extend it with optional keys (safe; validator won’t care):
            
            - `line_index[ref]["subsection"] = "ROLES_AND_RESPONSIBILITIES"` (only when inside)
            - `line_index[ref]["subsection_occurrence"] = rr_occurrence`
            - optionally `line_index[ref]["job_occurrence"] = k` (if you add a job-header heuristic later)
        - Phase 2 — expose it during suggest + diff
            - In `resume-suggest-edits`, when you print proposals, show:
                - `E044 (RR#2)` or `E044 (RR#2, JOB#1)` if available
            - In `rf_print_diff.py`, print those optional tags when present.
        - Phase 3 — make OpenAI proposals aware of R&R (without changing approval mechanics)
            
            Update the OpenAI prompt to **prefer** anchoring to R&R lines when a term is “experience-y” (process, tools used in delivery) vs SKILLS lines for tool lists.
            
            You do **not** need `--rr-occurrence` as a CLI arg yet. You can start by just **reporting** RR occurrence and letting the model anchor via `before_ref`. That gets you 80% of what you want with minimal new surface area.
            
        - Phase 4 — optional parity with v2 (`-rr-occurrence`)
            
            If you want the v2 UX (“work only in R&R block #2”):
            
            - Add `-rr-occurrence N` to `resume-suggest-edits`
            - Deterministically filter eligible `before_ref` lines to only those where `subsection_occurrence == N`
            - Print “Working in RR occurrence N” at runtime
            
            ---
            
    - The CLI “ai” command prompt you asked for
        
        Use this to make your CLI AI explicitly explain and map v2 → current:
        
        ```bash
        ai "In /Users/olivermarroquin/secondbrain_v2, explain exactly how Roles and Responsibilities targeting works. Read these files:
        - 01_projects/resume-factory/scripts/rf_family_init.py
        - 01_projects/resume-factory/scripts/rf_propose_changes_ai.py
        - 01_projects/resume-factory/scripts/rf_agent_runner.py
        Tell me:
        1) What data structure defines the R&R subsection and how it’s recognized (aliases/subsection keys).
        2) How --rr-occurrence flows through the pipeline and where it’s stored in the proposal/patch artifacts.
        3) The minimal changes needed to add equivalent R&R occurrence labeling to /Users/olivermarroquin/secondbrain (current repo), specifically in rf_docx_extract.py and resume-suggest-edits output."
        ```
        
        That prompt is “tight”: it forces file-based grounding, asks for the flow, then asks for a port plan.
        
    - **Insight from OpenAI in my CLI**
        
        ```bash
        Absolutely. Based on your directory structure and the three files you listed, I'll detail each point as requested—focused on how Roles and Responsibilities (R&R) targeting is implemented.
        
        ---
        
        ## 1) **Data Structure Defining the R&R Subsection**
        
        ### Recognizing the R&R Subsection:
        #### Where to Look:
        - `rf_family_init.py` (contains family/subsection definitions)
        - (Possibly used/parsed also by `rf_agent_runner.py`, depending on pipeline init logic)
        
        #### How is R&R Defined and Recognized?
        Search for **subsections**, **aliases**, or section keys in `rf_family_init.py`. Typically, roles and responsibilities in resumes are extracted as a **subsection** with a particular key/label and possibly **multiple aliases**.
        
        ##### Example from `rf_family_init.py`:
        
        ```python
        # Hypothetical structure:
        SECTION_ALIASES = {
            "roles_and_responsibilities": [
                "Roles & Responsibilities", "Responsibilities", "Key Responsibilities", "Role", "Duties"
            ],
            ...
        }
        ```
        
        Or, perhaps as part of a subsections dict/list:
        ```python
        FAMILY_SUBSECTIONS = [
            {"key": "roles_and_responsibilities", "aliases": ["Roles & Responsibilities", "Responsibilities", ...]},
            ...
        ]
        ```
        - **Key:** Internal identifier like `roles_and_responsibilities`
        - **Aliases:** Human-resume-section labels you're likely to find, which are recognized as referring to the same subsection
        
        **Conclusion:**  
        **R&R** is defined via a **key** (like `roles_and_responsibilities`) and a list of **string aliases**.  
        Parsing code (in extractors) checks for these aliases to assign content to that subsection internally.
        
        ---
        
        ## 2) **How --rr-occurrence Flows Through the Pipeline**
        
        ### Command-line Control
        - The `--rr-occurrence` command-line argument is added (likely to `rf_propose_changes_ai.py` or agent runner/CLI).
        
        #### Pipeline Flow:
        1. **CLI/Argument Parsing:**  
           - When called with `--rr-occurrence`, an integer or list value is passed (maybe for which RESPONSIBILITY instance to operate on).
        2. **Passing Through Modules:**  
           - Argument is accepted by the top-level script (`rf_propose_changes_ai.py`)
           - Passed down to processing (job/proposal builder, usually in `rf_agent_runner.py`)
           - Code ensures extraction, targeting, or AI suggestions happen on:
             - Only the targeted R&R occurrence (e.g., 2nd one)
             - Or labels proposal with which occurrence it pertains to
        
        #### Where is it Stored?
        - In the **proposal artifact** or **patch** dictionary—probably as a field like `"rr_occurrence"`.
        - Often attached to a section/subsection change dict, e.g.:
          ```json
          {
            "section": "roles_and_responsibilities",
            "occurrence": 2,
            "change_type": ...,
            ...
          }
          ```
          or:
          ```json
          {
            "subsection_key": "roles_and_responsibilities",
            "occurrence_idx": 1,
            ...changes...
          }
          ```
        
        **Summary:**  
        - `--rr-occurrence` is parsed from CLI.
        - It controls which occurrence (out of several, e.g., for jobs with multiple responsibility bullets) is targeted by proposals.
        - The target index is stored in the proposal/patch artifact (under a key like `"rr_occurrence"`, `"occurrence"`, or similar).
        
        ---
        
        ## 3) **How to Port This Functionality to /secondbrain (rf_docx_extract.py and resume-suggest-edits output)**
        
        ### *Goal:*  
        If `/secondbrain` currently extracts sections/subsections but **does not number or label occurrences within "Roles and Responsibilities"**, you want minimal changes for occurrence labeling.
        
        #### **rf_docx_extract.py**
        **Current:**  
        - Collects R&R subsection text by matching headings with aliases.
        
        **Minimal Addition:**
        - Instead of one blob, **store a list of occurrences** (e.g. each bullet or paragraph within R&R).
        - When emitting finds, include the **index** (occurrence) next to the text.
        - E.g., for each R&R bullet found:
          ```python
          {
            "section": "roles_and_responsibilities",
            "occurrence": i,      # 1-based or 0-based, pick and be consistent
            "text": bullet_text,
            ...
          }
          ```
        
        - If downstream code expects one R&R blob, make a compatibility function that concatenates them if needed.
        
        #### **resume-suggest-edits Output**
        **Current:**  
        - Proposals reference only the section (`roles_and_responsibilities`) but not which occurrence is targeted.
        
        **Minimal Addition:**
        - When generating a suggestion (edit, rewrite, etc.) on an R&R item, add an `"occurrence"` field in the proposal dict/output, e.g.:
          ```json
          {
            "section": "roles_and_responsibilities",
            "occurrence": 2,   # The one being edited
            "suggested_change": ...,
            ...
          }
          ```
        
        - When displaying, note the occurrence:  
          "Suggest changing Roles and Responsibilities (occurrence 2)..."
        
        ---
        
        ## **Summary Table**
        
        | Component                    | How it's handled in resume-factory        | Minimal change needed in secondbrain             |
        |------------------------------|-------------------------------------------|-------------------------------------------------|
        | **Subsection Recognition**   | Aliases in a list/dictionary              | Ensure R&R aliases recognized; no change if so   |
        | **Occurrence Labeling**      | Targeted by CLI arg/counter               | Output bullets as list w/ occurrence indexes     |
        | **Proposal Artifacts**       | Patch includes an occurrence field        | Add `"occurrence"` field to R&R changes         |
        | **Edit/Suggestion Output**   | Suggest/patches indicate occurrence       | Tag proposals w/ occurrence; update displays     |
        
        ---
        
        ## **References to Files in /resume-factory**
        
        ### rf_family_init.py
        - Defines R&R via string aliases (see above patterns).
        
        ### rf_propose_changes_ai.py
        - Parses `--rr-occurrence` from CLI.
        - Passes along to proposal-generation logic.
        
        ### rf_agent_runner.py
        - Receives occurrence param, targets changes/patches to selected R&R occurrence.
        - Stores occurrence index in the generated patch/proposal.
        
        ---
        
        ## **Concrete Steps for Minimal Port to secondbrain**
        1. **rf_docx_extract.py:**  
           - When extracting R&R, output a **list** of items, and for each one, add an `"occurrence"` integer (zero- or one-based; be consistent).
        
        2. **resume-suggest-edits:**  
           - In generated proposals or diffs for R&R, include an `"occurrence"` key.  
           - When generating output (print, json, patch), make occurrence visible.
        
        ---
        
        ## **Sample Patch**
        
        **Before (rf_docx_extract.py):**
        ```python
        roles_and_resp = get_section_text("roles_and_responsibilities", ...)
        yield {"section": "roles_and_responsibilities", "text": roles_and_resp}
        ```
        
        **After:**
        ```python
        bullets = extract_rr_bullets("roles_and_responsibilities", ...)  # returns list of strings
        for i, bullet in enumerate(bullets):
            yield {"section": "roles_and_responsibilities", "occurrence": i, "text": bullet}
        ```
        Or, if you don't want to break compatibility:
        ```python
        yield {"section": "roles_and_responsibilities", "text": bullets, "occurrences": len(bullets)}
        ```
        
        **Before (resume-suggest-edits output):**
        ```json
        {
          "section": "roles_and_responsibilities",
          "suggested_change": "...",
          ...
        }
        ```
        **After:**
        ```json
        {
          "section": "roles_and_responsibilities",
          "occurrence": 2,
          "suggested_change": "...",
          ...
        }
        ```
        
        ---
        
        ## **Summary**
        - **R&R** is aliased by a known key and list of string patterns.
        - **Occurrence targeting** flows in via a CLI arg, used at section extraction, proposal, and in patch; proposals store the occurrence index.
        - **Minimal changes:** In `/secondbrain`, enumerate R&R bullets in extract; tag each with occurrence; pass/print this in resume-suggest-edits output.
        
        **If you can show samples from your current extraction and proposal code in `/secondbrain`, I can provide exact patch blocks for you to copy-paste.**
        ```
        
    - Roles & Responsibilities (R&R) occurrence labeling in v1
        
        You already showed how v2 handles it with `section-aliases.json` and `SUBSECTION_OCCURRENCE`.
        
        In v1, we’ll implement a lightweight version:
        
        - Update `rf_docx_extract.py` to detect “Roles and Responsibilities:” headings inside EXPERIENCE
        - Count occurrences per job block
        - Add that metadata to `line_index` (e.g., `job_occurrence`, `rr_occurrence`)
        - Print it during `resume-suggest-edits --diff` so you can see “this edit is in Job #2, R&R #1”
        
        But we do this **after** term filtering + prompt tightening, otherwise you’ll just get better-labeled garbage.