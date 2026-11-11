# Fanfik — English-to-Russian literary translation

Fanfik is an experimental, human-directed approach to producing natural Russian literary translations. Its structured prompts are designed to help preserve the original author's meaning, voice, style, pacing, and emotional restraint, with optional contextual analysis and conservative editorial review. People remain responsible for the translation and every editorial decision; this methodology is not claimed to be scientifically superior to other approaches.

**New to Fanfik? Start with the [Getting Started guide](docs/GETTING_STARTED.md).**

## The workflow

**Analyze → Translate → Review**

- **Analyze (optional):** identify relevant context, relationships, ambiguity, and stylistic considerations from the source.
- **Translate:** produce natural Russian while preserving the author's intent and source structure.
- **Review (optional):** identify source-grounded errors and propose conservative corrections.

These stages are coordinated manually. You decide whether to analyze or review, and your judgment remains authoritative throughout.

## Try a short passage

Open [`prompts/translate.md`](prompts/translate.md), copy its instructions into a chat with an AI assistant, and replace `{{SOURCE_TEXT}}` with a passage. For example:

> When the lantern went out, Mira kept walking. “I can still hear the river,” she said.

The passage above is a fictional example, not a quality test or a verified translation result. The prompt asks the assistant to return only the Russian translation.

## Who might use Fanfik

Fanfiction readers, amateur literary translators, people exploring AI-assisted fiction translation, and technical readers interested in structured translation workflows. No programming knowledge is needed to use the prompts.

## Translation principles

The English source is authoritative. Aim for natural Russian while preserving meaning, uncertainty, ambiguity, subtext, voice, register, pacing, paragraph structure, and emotional restraint. Do not add details or explain what the source leaves implicit. Review changes against the source, make only justified corrections, and leave uncertain choices for human judgment.

## Requirements and EPUB export

Using the prompts requires a chat-based language model or assistant; provider workflows are described in the [Getting Started guide](docs/GETTING_STARTED.md). EPUB export and tests require Python 3.10 or newer. The builder uses only Python's standard library. No operating-system-specific support has been verified.

To assemble non-empty UTF-8 Markdown chapter files into an EPUB, pass them in reading order:

```sh
python3 scripts/markdown_to_epub.py -o book.epub \
  --title "Example Book" --author "A. Writer" ch01.md ch02.md
```

This command uses the existing builder; the title, author, and chapter names are examples to replace with your own. See [EPUB integration notes](docs/INTEGRATION.md) for supported Markdown and details.

## Available, experimental, and not implemented

- **Verified:** the EPUB builder's tests cover synthetic Markdown files, basic EPUB structure, chapter order, some formatting, and a missing-file error.
- **Experimental and untested as complete workflows:** using the prompts in Codex, ChatGPT, Claude, or another chat interface; carrying continuity notes between chapters; and assessing translation quality with the rubric. These are manual workflows, not tested provider integrations or guarantees of quality.
- **Not implemented:** automatic translation or review, persistent story memory, automatic acceptance, whole-book processing, or cross-provider compatibility.

The EPUB builder is a formatter, not a translator or EPUB quality checker. Prompts cannot guarantee correctness, and model self-review is not independent bilingual validation. Prior project trials did not establish a general quality advantage for added context or adaptive editing.

This public repository does not include copyrighted source texts, translations, or private project records. Keep such material out of public repositories, and check a provider's terms and privacy controls before sharing text with an online service. See [Getting Started](docs/GETTING_STARTED.md) for more guidance.

## Project files

- [`prompts/`](prompts/translate.md): contextual analysis, translation, and conservative review prompts.
- [`evaluation/rubric.md`](evaluation/rubric.md): blind assessment form separating source-grounded defects from reader ratings.
- [`scripts/markdown_to_epub.py`](scripts/markdown_to_epub.py): Markdown-to-EPUB builder.
- [`CURRENT.md`](CURRENT.md), [`ROADMAP.md`](ROADMAP.md), and [`BACKLOG.md`](BACKLOG.md): status, established direction, and deferred research.
