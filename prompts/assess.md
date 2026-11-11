# Chapter translation assessment prompt

Assess one reviewed Russian chapter against its frozen English source using `evaluation/rubric.md`. Follow that file's definitions and scales; do not duplicate or replace its criteria.

This is the ordinary single-candidate workflow. Identify the candidate and evaluator, and state plainly whether the same model produced or reviewed the translation. Do not claim blindness, independence, or external validation. The blind procedure in the rubric remains for future model-comparison experiments; do not reveal or infer candidate identities in those experiments before ratings are recorded.

## Fidelity findings

Compare the complete source and C1. Record each supported addition, omission, meaning shift/factual change, or structural distortion separately from literary ratings. For each finding provide:

- source paragraph and exact or locatable source span;
- exact or locatable Russian span;
- defect type, concrete evidence and effect;
- severity: minor, material, or critical.

Use only source evidence. Do not count stylistic preferences as fidelity defects. Do not collapse multiple defect types into one finding. If there are no supported defects, say so without claiming general correctness.

## Literary quality

Complete every rating dimension in the rubric from 1 (poor) to 5 (strong), with concrete examples for notable judgments. Keep these reader ratings distinct from the defect log. A strong literary score cannot cancel a fidelity defect, and ratings do not prove fidelity or independent quality.

## Required outcome

List uncertainties, limits, and any finding requiring human judgment. Explicitly identify every material or critical fidelity defect. Recommend corrections only when source-supported. Do not declare the chapter accepted while a material or critical defect is unresolved.

When a material or critical defect is corrected, update C1 with the minimal justified change and reassess that passage and its context against the English source. Append the corrected span, reason, and reassessment result to the assessment record; retain the original finding and initial ratings. Do not report a clean reassessment unless the new comparison supports it. Preserve minor findings and unresolved issues in the record.

Save the concise assessment record beside the chapter's C0 draft, using a separate file such as `ch001.assessment.md`; do not put assessment notes in the translation file. Include: identification; fidelity defect log; rubric ratings and evidence; material/critical correction and reassessment entries (or “None”); unresolved findings; and acceptance status (accepted only if assessment is complete and no material or critical fidelity defect remains unresolved).

## Frozen English source

{{SOURCE_TEXT}}

## Reviewed Russian chapter (C1)

{{TRANSLATION}}
