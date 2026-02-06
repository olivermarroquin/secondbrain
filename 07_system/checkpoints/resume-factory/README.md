# Project Enhancements, Ideas & Backlog System

- The right place for **requirement backlog** & desired functionality
    
    ### 📁 Canonical location
    
    ```
    ~/secondbrain/07_system/backlog/
    ```
    
    This is **intentionally outside**:
    
    - `01_projects/` (active work)
    - `07_system/checkpoints/` (truth & history)
    
    Because backlog ≠ truth, and backlog ≠ work.
    
    ---
    
    ## Recommended structure (simple, future-proof)
    
    ```
    07_system/backlog/
    ├── README.md
    ├──resume-factory/
    │   ├── ideas.md
    │   ├── requirements.md
    │   ├── ai-vision.md
    │   └── deferred.md
    ├── ai-cli/
    │   ├── ideas.md
    │   ├── agents.md
    │   └── automation.md
    └──global/
        ├── principles.md
        └── non-goals.md
    ```
    
    You do **not** need all of this immediately — but this layout prevents chaos later.
    
    ---
    
    ## What each file is for (tight definitions)
    
    ### `ideas.md`
    
    **Raw thoughts. No filtering.**
    
    - “I want AI to…”
    - “Maybe we could…”
    - “What if the CLI agent…”
    
    Rules:
    
    - No commitment
    - No priority
    - No guarantee it’ll happen
    
    This is your **parking lot**.
    
    ---
    
    ### `requirements.md`
    
    **Promoted ideas that survived thinking.**
    
    - Clear statements of intent
    - Still not implemented
    - May conflict with other requirements
    
    Example:
    
    ```markdown
    - Resume-factory must support AI-assisted refactors with full repo context- CLI agents must never modify files without a verification step
    ```
    
    ---
    
    ### `ai-vision.md`
    
    **Your long-term direction for AI usage.**
    
    This is where things like:
    
    - “AI should be involved as much as possible”
    - “Agents should collaborate”
    - “Claude orchestrates, OpenAI reviews, Gemini sanity-checks”
    
    live **without forcing implementation today**.
    
    This file is *aspirational*, not binding.
    
    ---
    
    ### `deferred.md`
    
    **Explicitly NOT doing now.**
    
    This is incredibly important.
    
    Example:
    
    ```markdown
    - Fully autonomous resume generation (too risky)- Auto-apply to jobs (legal + ethical concerns)
    ```
    
    This prevents re-arguing every month.
    
    ---
    
    ## How backlog interacts with the rest of the system
    
    ### 🔒 What backlog does NOT do
    
    - It does NOT affect CURRENT.md
    - It does NOT affect checkpoints
    - It does NOT drive immediate changes
    - It does NOT get read by default by CLI agents
    
    ### ✅ What backlog DOES do
    
    - Preserves ideas without pressure
    - Gives future-you context
    - Allows deliberate promotion of features
    
    ---
    
    ## The promotion rule (critical)
    
    An idea moves through **four stages**:
    
    ```
    ideas.md
      ↓ (you choose)
    requirements.md
      ↓ (you commit to building) CURRENT.md (as a planned capability)
      ↓ (after implementation)
    checkpoints (as a completed change)
    ```
    
    Nothing skips stages.
    
    ---
    
    ## Where “AI should be involved as much as possible” belongs
    
    👉 **`07_system/backlog/ai-cli/ai-vision.md`**
    
    That’s the right place for:
    
    - heavy AI involvement
    - multi-agent orchestration
    - future automation
    - “endgame” thinking
    
    Not in CURRENT.md. Not in checkpoints.
    
    ---
    
    ## Minimal setup you should do now (5 minutes)
    
    Just create:
    
    ```
    07_system/backlog/
    ├── README.md
    └── resume-factory/
        └── ideas.md
    ```
    
    You can expand later.