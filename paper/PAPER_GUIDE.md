# LG-SA Paper — Guide for Adding New Results

How to add a new experiment / new data to `LGSA.tex` without breaking the
conventions the paper already follows. Written with the curriculum redo in
mind, but applies to any new axis (X1–X4, V9–V12, …).

---

## 1. Hard constraints (AAAI-27)

- **7 pages of technical content**, hard limit. Only references and the
  reproducibility checklist get extra pages. The appendix does **not**: at
  submission it must move to the separate Supplementary upload. Everything
  before `\bibliography{bib}` is what counts.
- **Anonymous**: never add names, affiliations, grant numbers, repo URLs, or
  "our previous work" phrasing. Keep `\usepackage[submission]{aaai2027}`.
- **Deadlines**: abstract **2026-07-21**, full paper **2026-07-28**. No
  placeholder abstracts (AAAI deletes them).
- Formatting: don't touch the preamble lines marked `DO NOT CHANGE`; US
  Letter, Type 1 fonts (the template handles this).
- Reproducibility: whatever is claimed in the paper must be reproducible from
  the submitted materials — keep `HP_sweep.yaml` and the eval commands in the
  code supplement in sync with what the paper reports.

## 2. Where numbers come from (provenance rule)

Every number in the paper must trace back to a `res/<GROUP>` folder produced
by the protocol in `src/HyperParameters/HP_sweep.yaml`:

1. The batch design (groups, swept keys, seeds) lives in `HP_sweep.yaml`,
   with a comment block explaining the batch's question.
2. Checkpoints are evaluated with the standard command
   (`uv run eval/run.py --dataset random --FOLDER <GROUP> --dim 100 --DATA
   nazari --OUTER_STEPS 10000 --dtype float16 --no-baseline`) so that all
   configurations share the same fixed 10,000-instance test set.
3. Report the **mean final cost over seeds** from those CSVs. Never mix
   numbers evaluated with different `OUTER_STEPS`, dtype, or test sets in
   one table.

If you redesign a component (e.g. the curriculum), give the new batches new
GROUP names (don't overwrite old `res/` folders) and re-derive the noise
floor for the new batch — do not reuse an old batch's floor.

## 3. The per-experiment skeleton (main text)

One `\subsection` per design axis. Inside it, exactly this structure:

```latex
\subsection{<Axis Name>}

\paragraph{Motivation.}   % why this experiment exists; what question it answers
\paragraph{Candidates.}   % the compared variants, each defined in 1-2 lines.
                          % If a component is complex (like the curriculum),
                          % explain it globally here and push details/figures
                          % to the appendix.
<the results table>       % see table rules below
\paragraph{Results.}      % read the table: effect sizes vs. the batch's noise
                          % floor, seed-paired deltas quoted in prose,
                          % pointer to appendix diagnostics
\paragraph{Conclusion.}   % the adopted setting + the one-sentence takeaway
```

- **At most one plot per experiment in the main text** (zero is fine — most
  axes have none; the tables carry the numbers). Illustrations of methods
  that were *not* adopted go to the appendix (cf. the shared-encoder figure).
- Schematic/explanatory figures (like the curriculum ramp, Fig. 3) count as
  the axis's one figure.

## 4. Table rules (main text)

- Columns: **variant + cost only**. Add a Time (s) column *only* when the
  variant changes deployment compute (operators, feature count, actor size).
  Never for the critic or anything training-only.
- **No `Δ ± std` columns, no seed columns** in the table body. Significance
  lives in the Results prose ("seed-paired $-0.173 \pm 0.059$ against a floor
  of $0.072$") and in the appendix.
- Bold = best / adopted. Reference row first (or marked "(incumbent)").
- Costs with 3 decimals (16.459); times as integers.
- `booktabs` only (`\toprule/\midrule/\bottomrule`), `\small` or
  `\footnotesize` + `\setlength{\tabcolsep}{...}` if width is tight. A row
  must never wrap onto two lines — shorten the label instead
  ("$-$ load ratio, $-$ ranks").
- Caption states: what is reported, over how many seeds, and where the full
  diagnostics are ("Per-seed diagnostics in the appendix."). A `\midrule` may
  separate regimes (e.g. stable vs. broken rewards).
- Don't surface seed-set irregularities (missing/duplicated seeds) in tables;
  report "N runs per arm" and move on.

## 5. Statistical reporting rules

The convention is stated once in *Experimental Setup → Statistical protocol*;
every new experiment must follow it, not restate a different one:

- **3 seeds** for exploratory batches, **5 seeds** for confirmations and
  headline numbers.
- Comparisons are **seed-paired** (same seeds in both arms); quote the mean ±
  std of the per-seed differences and mention sign consistency ("unanimous
  across seeds" / "sign split").
- Significance is judged against the **per-batch noise floor** = pooled
  seed-to-seed std of the *stable* arms of that batch. State the floor in the
  Results paragraph. Below the floor = tie; say "tie", don't spin it.
- If some arms are unstable (sparse rewards, structured inits), exclude them
  from the pooled floor and say so — that is exactly why the convention is
  per-batch.
- For the curriculum specifically: the P0 baseline batch (5 seeds) *is* the
  section's noise floor — introduce it as such when reporting the gate
  (Batch 1 go/no-go) and reuse it through the section.
- Report negative results plainly (the paper already does: rejection
  strategy, shared encoder, terminal reward). A confirmed null with a clean
  floor is a result.

## 6. Figure rules

- PNGs go in `Figures/`, referenced by bare name (`\graphicspath` is set).
  Name them `<axis>_<content>.png` (e.g. `p_cl_gate.png`), lowercase.
- One-column: `width=0.9--0.95\columnwidth`; two-column (`figure*`):
  0.72–0.95`\textwidth`.
- **No near-duplicate plots**: if a ranking bar chart and a per-seed spread
  show the same data, keep the more informative one (usually the per-seed /
  paired-delta view). Before adding a plot, check whether an existing one or
  a table already shows it.
- Delta plots must show the shaded noise-floor band (that convention is
  announced in the Appendix Overview — keep the plotting scripts consistent
  with it).
- No cost-vs-time plots for training-only components (critic, reward, PPO
  knobs): evaluation time is unaffected, a time axis is misleading.

## 7. Appendix rules

The appendix mirrors the main-text order. To add a "Full Results" section
for a new axis:

1. `\section{Appendix: <Axis>, Full Results}` + `\label{app:<slug>}`,
   inserted at the position matching the main-text order.
2. Opening paragraph: what it collects + the **mapping from internal config
   names (plot legends, `HP_sweep.yaml` keys) to paper terminology** (e.g.
   `sig`/`lin` = sigmoid/linear ramp, `MAX_OUTER_STEPS_CL` = warm-up strength
   $\xi_{\mathrm{CL}}$, `MAX_PROB_STEP` = ramp duration $E$,
   `STEEP_SIG` = steepness $\kappa$).
3. One `\paragraph{<Topic>.}` per sub-question, **in the order of the
   main-text narrative**, each with 1–3 sentences saying what the
   table/figure shows and what to conclude — then its floats immediately
   after the paragraph (floats keep source order).
4. Full tables with `± std` and paired-Δ columns belong here, not in the
   main text — but don't duplicate a main-text table verbatim; the appendix
   version must add something (std, deltas, extra arms, per-seed views).
5. Update the **Appendix Overview** section if you add/rename a section.

## 8. Cross-referencing and labels

- Label scheme: `tab:<slug>` / `fig:<slug>` / `app:<slug>`; main-text tables
  get short names (`tab:reward`, `tab:metro`), appendix diagnostics keep the
  batch prefix (`tab:v3arch`, `fig:v5rank`).
- Main text points to appendix material as `Figure~\ref{fig:x} (appendix)`
  or `(Table~\ref{tab:x}, appendix)`.
- Every float must be referenced at least once from prose. When deleting a
  float, grep for its label first.

## 9. Checklist before committing a change

```bash
latexmk -pdf LGSA.tex
grep -E "Warning: (Reference|Citation).*undefined" LGSA.log   # must be empty
grep -E "Overfull \\\\hbox \([1-9][0-9]" LGSA.log             # must be empty (>10pt)
pdfinfo LGSA.pdf | grep Pages
```

- Check the page where **References** starts: the technical content before it
  must trend toward ≤ 7 pages (currently ~8 with sections still TODO — new
  content must be paid for by cuts elsewhere).
- Skim the rendered PDF around every float you touched (row wrapping,
  figure/table order, captions).
- Numbers cross-check: any value quoted in prose must match its table; any
  floor quoted must match the batch it came from.

## 10. Worked example: redoing the curriculum section

When the redesigned curriculum results are in:

1. New GROUP names in `HP_sweep.yaml` (e.g. `Q0_baseline`, `Q1_gate`, …),
   comment block explaining the redesigned mechanism and protocol.
2. Update the *Curriculum Learning* subsection: the mechanism description and
   ramp figure (Fig. 3) if the mechanism changed; then fill the skeleton —
   Motivation (train/test horizon gap) is already written; Candidates =
   schedule shape / strength / ramp / mechanism ablation; **one** results
   table: mean cost per protocol stage with the baseline row first (cost
   only; the gate, the winner, and the 5-seed confirmation); Results prose
   with the P0-derived floor; Conclusion = adopted curriculum + whether the
   ramp (vs. constant warm-up of equal budget) is what matters.
3. Add `Appendix: Curriculum Study, Full Results` (between the search-loop
   components appendix and — later — the final-model material), with the
   name mapping and the per-stage diagnostics; ≤ 1 plot in the main text
   (best candidate: gate + confirmation as one paired-delta plot).
4. Remove the TODO comments in the subsection, update the Appendix Overview
   sentence listing the appendices, run the §9 checklist.
