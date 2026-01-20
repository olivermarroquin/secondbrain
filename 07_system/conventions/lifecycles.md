# Lifecycle Rules (LOCKED)

Stages and destinations:
1) INBOX      -> 00_inbox/ (transient, TTL 7 days)
2) PROJECT    -> 01_projects/ (active, resumable work)
3) KNOWLEDGE  -> 02_knowledge/ (distilled canon; strict gate)
4) ASSET      -> 03_assets/ (media, templates, reference files)
5) OUTPUT     -> 05_outputs/ (AI-generated artifacts)
6) ARCHIVE    -> 06_archive/ (immutable cold storage)

Move rules:
- Anything in 00_inbox older than 7 days must be moved or sent to 06_archive/unsorted/
- Recordings: 00_inbox/recordings -> 05_outputs/transcripts + 05_outputs/summaries -> optional 02_knowledge distillation
- Resume templates: 03_assets/templates/resumes
- Resume outputs: 05_outputs/resumes/<company>/<role>/<YYYY-MM-DD>/
- Nothing enters 02_knowledge unless it is cleaned, titled, source-referenced, and not raw
- Archive is immutable: copy out, never editin place
