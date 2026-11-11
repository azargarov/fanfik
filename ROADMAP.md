# Roadmap

## Prototype status

The instruction-led whole-book workflow is implemented for ordinary text-based EPUBs. Codex prepares and checks the source, processes chapters sequentially through analysis, translation, editorial review, and rubric-based assessment, records resumable progress, updates optional Dynamic Context after acceptance, and assembles a Russian EPUB from accepted chapters.

The repository includes an EPUB-to-Markdown importer, Markdown-to-EPUB 3 builder, stage prompts, a literary assessment rubric, and focused synthetic-input tests. Prototype validation exercised the chapter workflow and EPUB conversion/assembly; automated utility tests cover ZIP/package handling, extraction order and formatting, refusal to overwrite, and output EPUB structure. These checks do not establish translation quality or broad reliability across books and models. Full-book quality has not received independent bilingual validation.

## Known limitations

- Import is limited to ordinary unencrypted EPUB 2/3 text. PDF, OCR, DRM, images, and complex or styling-dependent layouts are unsupported; chapter boundaries may need careful manual identification.
- EPUB import produces one combined Markdown file and a manifest, not automatically separated story chapters. Codex prepares and verifies chapter files.
- Codex coordinates the workflow through instructions and prompts; there is no standalone translation program or automatic literary-quality guarantee.
- Single-candidate model assessment is self-assessment, not blind or independent validation. The rubric's blind procedure is intended for controlled candidate comparison.
- Dynamic Context is experimental. Its effect on continuity or translation quality has not been established.
- The EPUB builder supports a limited Markdown subset and validates structure only.

## Possible future improvements

Deferred questions and ideas are in [BACKLOG.md](BACKLOG.md). Possible work includes independent bilingual assessment, checking where compact continuity notes help, and addressing demonstrated extraction or formatting gaps. These are research directions, not proven quality improvements or active commitments. Keep the project model-independent and avoid adding orchestration or infrastructure without a demonstrated need.
