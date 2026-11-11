# Getting started with Fanfik

Fanfik is a collection of prompts and a small EPUB builder, not an application with buttons or an automatic translation pipeline. You control what text is shared, provide the prompts to a language model, review its work, and keep the output you choose.

## Before sharing source text

The repository contains no book text. Keep copyrighted or otherwise private source material and translations in a private working location; do not add them to a public GitHub repository. A file being on your own computer does **not** mean its contents stay there when you submit it to an online model.

Before sending text to a provider, check that provider's current terms, privacy controls, and any rules that apply to your source. Share only text you are allowed to share, and consider using the shortest passage that supplies enough context. Do not include personal or confidential information unnecessarily. This guide cannot determine your rights or guarantee a provider's handling of submitted text.

## Choose how to use the prompts

The following are **plausible manual workflows, not provider integrations tested by this project**. The same prompt text is in the repository, but each chat product may handle long inputs, files, and instructions differently. You can copy the relevant prompt from `prompts/` into a chat and replace its placeholder sections with your material.

### Codex

If you use Codex in an environment that can read this repository, ask it to read and follow the relevant prompt file. Provide the source passage and context you intend it to use. For example, you can request scene analysis with `prompts/analyze.md`, then translation with `prompts/translate.md`, or conservative review with `prompts/review.md`.

Tell Codex whether it may create or change files. If you only want suggestions, say to return the result in the conversation and not write source text or translations into the repository. Codex availability and file access depend on how it is set up; this repository does not configure them.

### ChatGPT or Claude in a chat interface

Open the prompt file you need, copy its instructions into a conversation, and replace the placeholder text with the source and any relevant context. You may instead provide the source as an attachment if your interface accepts it, but follow the service's privacy and file-handling rules. Keep the prompt's instructions together with the passage so the model receives the constraints in the same request.

No ChatGPT- or Claude-specific integration, file workflow, or cross-provider equivalence has been tested. Other chat interfaces may work similarly, but their behavior is also unverified.

## A chapter-by-chapter process

Use one chapter or manageable scene at a time. Save the English source privately and keep any notes, draft, and reviewed text in separate files or clearly labeled copies so you can compare them. Fanfik does not create these files or track versions for you.

### 1. Analyze context when useful

For a scene that depends on earlier events, use [`../prompts/analyze.md`](../prompts/analyze.md). Supply the scene and only relevant adjacent or earlier source context. The prompt asks for paragraph-grounded facts, interpretation, and uncertainty. Read the analysis and remove unsupported claims before using it. Skip this step if context notes are not needed.

### 2. Translate

Use [`../prompts/translate.md`](../prompts/translate.md) with the English passage. If you made context notes, include only verified, relevant notes that do not reveal later events. Preserve paragraph breaks when carrying text between stages. The prompt returns Russian text only; it does not provide a change log.

### 3. Review conservatively

Use [`../prompts/review.md`](../prompts/review.md) with the frozen English source and the Russian draft. It asks for a complete proposed C1 text, a concise change log, and unresolved questions. Check every material change against the English. Accept, reject, or revise suggestions yourself; leave uncertain changes flagged. Avoid replacing the previous draft until you have compared and saved the version you want to keep.

### 4. Carry continuity forward

For the next chapter, provide relevant earlier **source** passages or concise notes grounded in them. Label what is explicit, what is interpretation, and what remains uncertain. Keep notes limited to what characters know at that point; do not pass later revelations backward. Reuse character names and established terminology consistently, but verify each choice against the current source. A model may not retain facts between chats, and this project does not provide persistent story memory.

### 5. Keep and export your chosen text

Save source, draft, accepted revision, and notes separately in a private location. The repository's [blind assessment rubric](../evaluation/rubric.md) can help a reviewer record source-grounded defects separately from reader ratings; blind and independent review is a manual process.

For EPUB export, prepare one non-empty UTF-8 Markdown file per approved chapter and pass the filenames in reading order. This is the only executable workflow in this guide. The builder is tested on synthetic examples, not on your book or every EPUB reader. See [integration notes](INTEGRATION.md) for supported Markdown and an example command. Readers who do not want to use Python can keep their text in a word processor; Fanfik does not currently provide a no-code EPUB export route.

## Troubleshooting

- **The model ignores a constraint:** resend the relevant prompt with the source passage, restate the missed rule briefly, and inspect the result against the source. A prompt cannot guarantee compliance.
- **The model invents or resolves something:** compare the claim with the exact source span. Remove unsupported material or record the uncertainty; do not treat a fluent answer as evidence.
- **Continuity drifts between chapters:** provide a short, source-checked recap and terminology list with the next passage. Do not assume the model remembers another chat.
- **The builder says a chapter file does not exist:** check the spelling and location of every filename and run the command from a location where those paths resolve. The builder does not search for or sort chapters.
- **The builder rejects the output path:** use a filename ending in `.epub`, and provide non-empty title and author values.
- **Formatting looks different in a reader:** the builder supports only the Markdown features listed in [integration notes](INTEGRATION.md). Complex Markdown and reader-specific layout are outside its tested scope.

## Status of the guidance

- **Verified:** the repository contains the prompts, rubric, and EPUB script; the script's existing tests pass for synthetic inputs.
- **Plausible but untested:** the manual stages above in Codex, ChatGPT, Claude, or other model interfaces; using notes to improve continuity; and the rubric's effectiveness with particular readers or books.
- **Requires future implementation:** automatic stage orchestration, story memory, automatic quality decisions, direct provider integrations, and no-code EPUB export.
