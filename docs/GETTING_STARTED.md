# Getting started

[Project README](../README.md) · [Русский](GETTING_STARTED.ru.md)

Fanfik supports two ways to run the same chapter workflow. **Agent mode is recommended** because a filesystem-capable coding agent can manage files, checkpoints, conversion, and export. In **Chat mode**, you provide the text and manage every file and command yourself.

## Agent mode (recommended)

1. Open this repository in Codex or another coding agent that can read and write project files. Python 3.10+ is required for the included EPUB tools; they use the standard library.
2. Put one ordinary, unencrypted English EPUB in `books/`.
3. Ask the agent:

   > Read and follow `AGENTS.md`. Translate the English EPUB in `books/` into Russian using Fanfik. Save the finished EPUB in `books/`.

The agent follows [AGENTS.md](../AGENTS.md): it prepares and verifies the source, initializes Dynamic Context (unless disabled), and processes every chapter in order through mandatory analysis, fresh C0 translation, editorial review/C1, C1 integrity verification, rubric assessment, required fidelity correction and reassessment, acceptance, and context update. Once all chapters are accepted, it assembles and structurally validates the Russian EPUB. You do not need to request each stage or approve each chapter.

Even when you request the whole book, the agent handles one chapter at a time instead of putting the book into one translation task. This keeps the active material within the model's context window and makes checkpoint-based resuming practical.

### Long books and context windows

A single request can start a full-book translation, but a long book may need several agent sessions. For a long book, ask the agent to work in small batches, for example 3–5 chapters, and stop at a chapter boundary after completing all stages, acceptance, and the Dynamic Context/progress update. The batch size is a starting point: adjust it for chapter length, model context capacity, and the amount of analysis and review material.

For example:

> Following `AGENTS.md`, translate the next 3–5 chapters in reading order. Complete each chapter's full workflow and update the saved progress and Dynamic Context after acceptance. Then stop at the next chapter boundary and report the next unfinished chapter so I can resume in a fresh session.

Start a fresh agent session, open the same project, and ask it to continue from the saved project state. It will inspect the checkpoints and resume at the first unfinished chapter/stage.

Progress and artifacts are saved under `books/`. If interrupted, ask the agent to continue the translation; it inspects the progress record and existing files and resumes at the first incomplete stage. The source EPUB remains unchanged, and `books/` is excluded from Git.

The importer supports ordinary text-based EPUB 2/3 XHTML/HTML. PDF, OCR, DRM, images, and complex layouts are unsupported. The agent checks extraction warnings and chapter text, but model assessment is not independent translation validation. Dynamic Context is experimental and can be disabled by request.

## Chat mode (manual execution)

Use this mode with a conversational LLM that cannot access the repository or run commands. You copy prompt instructions and source text into chat, then manage files and local tools yourself. The LLM does not create files, persist checkpoints, verify your saved files, or assemble the EPUB for you. If you disable Dynamic Context, record that choice in your progress notes and omit context from prompts; keep the other stages.

For a long book, use batches of a few chapters per chat session, save all accepted chapter files plus the updated Dynamic Context and progress notes, then start a fresh chat. Supply the current context and the next unfinished chapter; do not rely on the new chat remembering earlier conversation content.

### Start a chat

Copy the relevant files from `prompts/` and `evaluation/rubric.md` into the conversation when using each stage. Start with:

> I am translating an English EPUB into Russian with Fanfik. I will provide one complete, numbered English chapter at a time and maintain the files and Dynamic Context myself. Follow the supplied Fanfik prompts in order. Do not skip analysis, C0 translation, editorial review, C1 integrity verification, assessment, acceptance, or the post-acceptance context update. Do not use later chapters. Ask if an unresolved issue could materially change facts, events, attribution, or meaning.

### Work through each chapter

1. **Prepare the text and initial context.** Run `python3 scripts/epub_to_markdown.py books/source.epub --output-dir books/import` locally. Inspect the manifest and warnings, determine chapter boundaries, and save complete UTF-8 chapter files in reading order. Create a context note with `Context through: none` and the sections used by [AGENTS.md](../AGENTS.md). For each chapter, number source paragraphs and provide only relevant preceding English context.
2. **Analyze.** Paste `prompts/analyze.md`, the current chapter and relevant prior English context, and the current Dynamic Context. Save the returned analysis yourself.
3. **Create C0.** Paste `prompts/translate.md`, the complete frozen English chapter, and current Dynamic Context. Save only the Russian translation as C0.
4. **Review into C1.** Paste `prompts/review.md` with the complete English chapter and complete C0. Save the complete revised Russian text as C1, plus its change log and unresolved questions.
5. **Verify C1 integrity.** Compare every correction marked applied with C1 at its source location: the replacement must be present, or the log must say why it was rejected or superseded. Compare all of C0 with C1 and document every change. If a correction is missing or an edit is unlogged, have the LLM correct the record/text and repeat the check. Do not proceed until it passes.
6. **Assess and accept.** Paste `prompts/assess.md` and `evaluation/rubric.md` with the complete frozen English chapter and C1. Save the defect log, ratings, uncertainties, and outcome separately from the translation. Correct every material or critical fidelity defect minimally, record the change, and reassess the affected passage against English. Accept only when assessment is complete and no material or critical fidelity defect remains unresolved; preserve minor findings and uncertainty.
7. **Update context after acceptance.** Using the English chapter and accepted decisions, update Dynamic Context with source-grounded facts, interpretations, unresolved questions, character/relationship states, terminology, and voice/style. Set `Context through` to this accepted chapter. Do not add a plot summary or future knowledge. Record the chapter's stage status and file paths in your progress notes.
8. **Continue and export.** Repeat for the next chapter in source order. After every chapter is accepted, save the C1 chapters as UTF-8 Markdown files with headings, then run the existing builder locally, supplying every file in reading order:

       python3 scripts/markdown_to_epub.py \
         --output books/translated.ru.epub \
         --title "Book Title" --author "Author Name" --language ru \
         books/work/reviewed/ch001.c1.md books/work/reviewed/ch002.c1.md

   Choose an unused output path. Validate the resulting EPUB structure as described in [EPUB integration notes](INTEGRATION.md). The structural checks do not assess literary quality.

The agent workflow's full recovery, acceptance, and validation rules are in [AGENTS.md](../AGENTS.md). Extraction and builder details are in [EPUB integration notes](INTEGRATION.md). Keep source books and all generated book material out of version control; text sent to a chat provider is subject to that provider's data-handling terms.
