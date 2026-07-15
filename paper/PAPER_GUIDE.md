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

## 3. Main-text ablation: one summary subsection

The whole ablation study (§5.1) is a **single `\subsection`** —
`Design Choices` (or `Ablation Summary`) — budgeted at **~1.25 pages**. There
is **no `\subsection` per axis** and **no per-axis
Motivation/Candidates/Results/Conclusion skeleton in the main text**; that
skeleton now lives once per axis in the **appendix** (§7). The main text states
*which* setting was adopted on each axis and *why*, backed by one summary
table, and defers all evidence (candidate lists, per-seed diagnostics, full
tables, plots) to the appendix.

### 3.1 Structure

```latex
\subsection{Design Choices}   % or "Ablation Summary"

% Opening: state the design space and validation protocol ONCE, in symbols
% (coordinate descent over an ordered axis tuple; per-batch noise floor;
%  seed counts). Do NOT restate the protocol per axis.

<master summary table>        % one row per design axis; see 3.1 + §4

\paragraph{Search operators.}      % operator + feasibility: adopted + 1 takeaway
\paragraph{Node representation.}   % feature set + conditional pair descriptors
\paragraph{Policy and learning.}   % architecture + reward + optimization budget
\paragraph{Annealing search.}      % schedule + Metropolis + initialization
\paragraph{Curriculum.}            % adopted curriculum + whether the ramp matters

% optional: 1-2 headline result tables for the highest-leverage axes only
% (operator x feasibility; final feature set). Every other axis -> appendix.
```

- **One `\paragraph{}` per thematic group, not per axis:** 2–4 sentences each,
  giving the adopted setting, the seed-paired effect size against the batch's
  noise floor, and a pointer to the appendix
  (`Table~\ref{...} / Fig.~\ref{...} (appendix)`). The grouping above is the
  default; move an axis only if it genuinely doesn't fit.
- **Master summary table (required):** one row per design axis. Columns —
  *Axis*, *Adopted setting*, *\# cand.*, *Effect vs.\ floor* (signed
  seed-paired $\Delta$ + a significance mark, or "tie"), *Appendix*. This one
  object shows every decision at a glance and replaces the nine per-axis body
  tables. See §4 for its exact form.
- **Headline tables (0–2):** full result tables only for the highest-leverage
  axes (operator $\times$ feasibility; final feature set). A non-headline
  axis's table lives *only* in the appendix — never duplicate it in the body.
- **At most one figure in the entire ablation subsection** (the curriculum
  ramp schematic, Fig. 3, is the natural candidate). Everything else — including
  any illustration of a method that was *not* adopted (e.g. the shared-encoder
  figure) — goes to the appendix.

### 3.2 Define every object before you use it

The main text must read as a mathematical argument, not a lab log. A symbol or
term must be defined *before* it appears in any claim — preferably once, in
*Experimental Setup*, then reused verbatim (same symbol in body and appendix):

- **Design space** as an ordered tuple of axes
  $\mathcal{A} = (a_1,\dots,a_K)$, each axis $a_k$ ranging over a finite
  candidate set $\mathcal{C}_k$. Coordinate descent = fixing $a_{<k}$ at their
  winners while sweeping $\mathcal{C}_k$.
- **Objective**: final tour cost $c(\cdot)$ (state the cost convention, cf.
  `eval/costs.py`), reported as the seed-mean $\bar c$.
- **Seed-paired delta**
  $\Delta_k = \bar c(\text{variant}) - \bar c(\text{incumbent})$ over shared
  seeds, and the **per-batch noise floor** $\sigma_{\mathrm{floor}}$ (pooled
  seed-to-seed std of the stable arms). Define "significant" once as
  $|\Delta| > \sigma_{\mathrm{floor}}$ and cite that inequality thereafter.
- Every axis-specific object (feature groups, operators, reward function,
  temperature schedule, warm-up strength $\xi_{\mathrm{CL}}$, ramp duration
  $E$, …) is defined at first mention, with its symbol.

No undefined acronyms, no "we tuned $X$" without stating what $X$ ranges over.
Prefer "$\Delta = -0.173 \pm 0.059$ against $\sigma_{\mathrm{floor}} = 0.072$"
to "clearly better".

## 4. Table rules (main text)

Two kinds of table live in the body: the **master summary table** (exactly one,
§3.1) and **headline tables** (0–2, §3.1). Everything else is appendix (§7).

**Master summary table** — one row per design axis:

- Columns: *Axis*, *Adopted setting*, *\# cand.*, *Effect vs.\ floor*,
  *Appendix*. The effect column is a compact **signed seed-paired $\Delta$ + a
  significance mark** (e.g. `-0.173**`, or `tie` when
  $|\Delta| \le \sigma_{\mathrm{floor}}$) — this is the one place a $\Delta$
  appears in the body, and it is a single number, not a `Δ ± std` column.
- Define the significance marks in the caption
  ("`**` $= |\Delta| > 2\sigma_{\mathrm{floor}}$", etc.) and state the floor(s)
  the effects are measured against, plus the per-axis appendix labels.
- Bold the adopted setting. Rows follow the coordinate-descent order (= the
  paragraph order in §3.1).

**Headline tables** (highest-leverage axes only):

- Columns: **variant + cost only**. Add a Time (s) column *only* when the
  variant changes deployment compute (operators, feature count, actor size).
  Never for the critic or anything training-only.
- **No `Δ ± std` columns, no seed columns** in the body. Significance lives in
  the Results prose ("seed-paired $-0.173 \pm 0.059$ against a floor of
  $0.072$") and in the appendix.
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

1. `\appsection{<Axis>, Full Results}` + `\label{app:<slug>}` on the next
   line, inserted at the position matching the main-text order. Do **not**
   use a plain `\section{Appendix: ...}`: AAAI headings are unnumbered
   (`secnumdepth 0`), so `\ref{app:...}` would render empty. `\appsection`
   (defined in the preamble) steps a manual letter counter, so headings read
   "Appendix B: ..." and `\ref` resolves to the letter — and all letters
   shift automatically when a new appendix is inserted.
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
2. Update the **`Curriculum.` paragraph** of the single `Design Choices`
   subsection (§3.1) — not a subsection of its own. State the adopted
   curriculum, the seed-paired effect vs.\ the P0-derived floor, and whether
   the ramp (vs. a constant warm-up of equal budget) is what matters; end with
   a pointer to the appendix. Add its row to the master summary table (axis =
   curriculum; adopted setting; \# candidates across the protocol; effect vs.
   floor; appendix label). The curriculum ramp schematic (Fig. 3) may be the
   subsection's single figure if the mechanism changed.
3. Put **all** stage-by-stage evidence in `Appendix: Curriculum Study, Full
   Results` (between the search-loop components appendix and — later — the
   final-model material): the name mapping, the P0 baseline as the section
   floor, the go/no-go gate, schedule shape / strength / ramp duration /
   steepness sweeps, the mechanism ablation, the random-depth study, and the
   5-seed confirmation — full tables with `± std` and paired-Δ columns. The
   whole ablation subsection carries at most one plot total (§3.1); the
   curriculum's diagnostics plots live here.
4. Remove the TODO comments in the subsection, update the Appendix Overview
   sentence listing the appendices, run the §9 checklist.
