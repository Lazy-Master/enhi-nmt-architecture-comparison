# Master Plan — Dissertation Stage-I Report + Review Presentation

**Project:** English → Hindi Neural Machine Translation: A Comparative Study of Three
Sequence-to-Sequence Architectures
**Student:** Anish Date · M.Tech II (AI & DS)
**Template:** VPKBIET `vpcoe.cls` (copied to `template/`)
**Report target:** ~30 printed pages (≈15 sheets double-sided), 6 numbered chapters
**PPT target:** 16 slides, 15 min + 5 min questions

**Governing rule:** every page carries a figure, a table, or a number. No page of pure prose.

All numbers come from `01_CANONICAL_NUMBERS.md`. Nothing else is a valid source.

---

# PART A — THE REPORT

## A1. How the college template is shrunk

The template ships 11 chapters. A Stage-I review is marked on *work done and results*, not
on software-engineering ceremony. Six of the eleven chapters carry no marks here.

| Template chapter | Decision | Why |
|---|---|---|
| Literature Survey | **Cut** | Longest chapter in the template, zero marks at Stage-I. Related work compresses to one paragraph in §1.1. |
| Proposed Systems Architecture | **Merge into Methodology** | A whole chapter for one block diagram wastes 4–5 pages. |
| Requirement Specification (HW/SW/perf/quality/security/other) | **Cut** | Boilerplate. Becomes a 6-line environment table in §3.7. |
| Dissertation Planning / Estimates / Team Structure | **Cut** | Solo project; effort estimates would be invented. |
| Dissertation Schedule / Breakdown | **Cut** | One sentence in §3.4 ("developed over two stages"). |
| Dissertation Design (UML, DFD, ER, test cases) | **Cut** | This is an experimental research report, not a software product. UML of a notebook is noise. |
| Proposed GUI / Working Modules | **Cut** | There is no GUI. Notebook output *is* the interface; screenshots belong in Results. |
| Tools Used (appendix) | **Fold into §3.7** | One table row. |
| Plagiarism Report / Base Paper / Papers Published | **Keep only if the guide demands** | Ask. If not required, dropping saves 3–4 pages. |

**11 chapters → 6 chapters + references.**

## A2. Page budget

| Part | Content | Pages |
|---|---|---|
| Front matter | Title, certificate, acknowledgement, abstract, contents, list of figures/tables, abbreviations | 6 |
| **Ch. 1** | Introduction | 3 |
| **Ch. 2** | Objectives and Scope | 2 |
| **Ch. 3** | Methodology | 8 |
| **Ch. 4** | Results and Discussion | 8 |
| **Ch. 5** | Conclusion and Future Scope | 3 |
| References | 13 IEEE entries | 1 |
| Appendix (optional) | Notebook link, tool versions, hyper-parameter dump | 1 |
| **Total** | | **~32 (≈30 without appendix)** |

If the guide wants exactly 30: drop §4.8 to two paragraphs and cut the appendix.

## A3. Front matter (6 pp)

1. **Title page** — template block, title as above.
2. **Certificate** — template block; guide / HoD / Principal names.
3. **Acknowledgement** — 120 words maximum.
4. **Abstract** — 250–300 words. One paragraph each: problem → data & method → headline
   numbers → conclusion. *Write this last.*
5. **Table of contents** — `\makecontents`.
6. **List of figures / list of tables**, abbreviations (NMT, BLEU, chrF++, TER, OOV, AMP,
   SP, LR, ppl, T4).

## A4. Chapter-by-chapter

### Ch. 1 — Introduction (3 pp)

| § | Content | Length | Carries |
|---|---|---|---|
| 1.1 | **Context.** En→Hi as an under-resourced pair; NMT replaced SMT; the practitioner's three choices — architecture, tokeniser, budget. One paragraph of related work citing [1][2][3][4]. | ¾ p | — |
| 1.2 | **Problem statement.** Under a *fixed* data/compute budget, how much does architecture alone buy? Hindi morphology breaks word-level vocabularies (8.85 % `<unk>`), so naive comparisons confound tokenisation with architecture. | ¾ p | 8.85 % |
| 1.3 | **Motivation.** Published comparisons usually change the recipe as well as the model. A controlled comparison is defensible at 100 K pairs on one GPU. | ½ p | — |
| 1.4 | **Contributions** — three bullets: (i) one shared pipeline for three architectures; (ii) the tokenisation effect *measured* (8.85 % → 0.001 %), not assumed; (iii) full results under greedy **and** beam with BLEU / chrF++ / TER. | ½ p | 0.001 % |
| 1.5 | **Report organisation** — four lines. | ¼ p | — |

**Fig. 1.1** — one-panel block diagram of the shared pipeline (data → tokeniser → 3 models → decode → metrics). This single drawing replaces the entire "Proposed Architecture" chapter.

---

### Ch. 2 — Objectives and Scope (2 pp)

| § | Content |
|---|---|
| 2.1 | **Objectives O1–O5:** (O1) build a reproducible En→Hi pipeline on the IITB corpus; (O2) quantify word-level OOV against subword `<unk>`; (O3) train vanilla LSTM, Bahdanau attention and Transformer under one recipe; (O4) compare on BLEU / chrF++ / TER under greedy and beam; (O5) analyse where each fails — length buckets, attention alignment, error classes. |
| 2.2 | **Scope.** In: En→Hi, one direction, 100 K pairs, 32 K SentencePiece, one seed, no pretrained weights. Out: multilingual, pivoting, domain adaptation, deployment. |
| 2.3 | **Constraints.** One Kaggle T4 ×2 session (15.6 GB), 12-epoch cap, single seed, from-scratch training. |

**Table 2.1** — objective → how measured → where reported. Maps every objective to a
results table so the examiner can tick them off. Half a page, high value.

---

### Ch. 3 — Methodology (8 pp) ← the core chapter

| § | Content | Pages | Carries |
|---|---|---|---|
| 3.1 | **Dataset.** IITB En–Hi; 1,652,981 / 520 / 2,507 raw; cleaning rules; 83.3 % retained; subsample to 99,561 / 3,000 / 2,505. | 1.5 | Table 3.1, 3.2 |
| 3.2 | **Tokenisation.** Word-level baseline (49,955 EN / 43,774 HI, OOV 11.97 % / 8.85 %) vs SentencePiece Unigram 32 K; why subword; how `<unk>` was measured. | 1.5 | Table 3.3 |
| 3.3 | **Architectures.** 3.3.1 vanilla LSTM enc–dec; 3.3.2 Bahdanau additive attention; 3.3.3 Transformer (4+4, 8 heads, d=512, FFN 2048). Same `encode`/`decode_step` interface for all three. | 2 | Fig. 3.2 |
| 3.4 | **Training protocol.** Adam, clip 1.0, plateau LR (RNNs) / Noam (Transformer), label smoothing 0.1 (Transformer only), AMP, early stopping, per-epoch checkpointing. Include the **Noam scaling argument** here or defer to §4.7 — recommend deferring. | 1 | Table 3.4 |
| 3.5 | **Decoding.** Greedy + beam k=5, α=0.7; why beam needs its own eval subset. | 0.5 | — |
| 3.6 | **Evaluation.** BLEU (`intl`), chrF++, TER; 2,505 greedy / 1,000 beam; why chrF++ is the metric to trust for Hindi. | 0.75 | — |
| 3.7 | **Environment.** PyTorch 2.x, CUDA, Kaggle T4 ×2, 15.6 GB; version table; seed control; resumability from checkpoints. | 0.75 | Table 3.5 |

**Figures:** Fig. 3.1 sentence-length distribution; Fig. 3.2 three architectures side by
side (one drawing, three columns — cheaper than three diagrams).
**Tables:** 3.1 splits · 3.2 cleaning rules · 3.3 tokeniser comparison · 3.4 hyper-parameters
· 3.5 parameter counts (**43.15 M / 94.80 M / 62.23 M**).

---

### Ch. 4 — Results and Discussion (8 pp)

| § | Content | Pages | Carries |
|---|---|---|---|
| 4.1 | **Tokenisation result.** 8.85 % → 0.001 % `<unk>`. Strongest single result — put it first. | 1 | Table 4.1 |
| 4.2 | **Training behaviour.** Loss curves, best epoch per model, wall-clock per epoch, over/under-fitting. | 1.5 | Fig. 4.1, Table 4.2 |
| 4.3 | **Headline comparison.** 3 models × BLEU/chrF++/TER × greedy/beam. | 1.5 | Table 4.3, Fig. 4.2 |
| 4.4 | **Effect of beam search.** ΔBLEU per model; note that beam *lowers* chrF++ for both RNNs. | 1 | Table 4.4 |
| 4.5 | **Length-bucket analysis.** chrF++ by source length. Report honestly that all three improve with length. | 1 | Fig. 4.3, Table 4.5 |
| 4.6 | **Attention alignment.** Bahdanau heatmap; 3 sentences, 3 observations. | 1 | Fig. 4.4 |
| 4.7 | **Transformer stability study.** The lr ablation: peak 6.99e-4 → 3.84e-4 turned a degenerate model (chrF++ 3.49, repetition collapse) into a working one (chrF++ 7.91). Explain the batch-size-vs-Noam-peak argument. | 1 | Table 4.6 |
| 4.8 | **Discussion.** Answer the research question: architecture buys **10.65 chrF++ points** at this budget, at 2.2× the parameters and 2.4× the training time of the cheapest model. | 1 | — |

**Figures:** 4.1 loss curves · 4.2 BLEU/chrF++ bars · 4.3 chrF++ vs length · 4.4 attention heatmap.
**Tables:** 4.1 `<unk>` rates · 4.2 best epoch/val/time · 4.3 headline results · 4.4 beam Δ
· 4.5 length buckets · 4.6 LR ablation.

> **Framing decision for §4.7:** presenting the Transformer instability as a *finding*
> rather than an embarrassment is both honest and stronger. The report shows a
> diagnosis (Noam peak assumes ~25 k tokens/batch; this run has ~4 k), a fix, and a
> quantified before/after. That is exactly what a research review rewards.

---

### Ch. 5 — Conclusion and Future Scope (3 pp)

| § | Content |
|---|---|
| 5.1 | **Conclusion** — one paragraph per objective O1…O5, each with its number. No new claims. |
| 5.2 | **Limitations** — single seed (no error bars); 100 K pairs; validation really only 520 official sentences; no pretrained baseline; one direction; BLEU on 2,505 sentences has a ±0.5–1.0 noise band. |
| 5.3 | **Future scope** — 3-seed sweep for error bars; COMET; pretrained comparison (`opus-mt-en-hi`, NLLB [13]); BPE vs Unigram vs word ablation; scaling curve 10 K → 400 K; the multi-agent long-document extension that motivates the dissertation. |

Half a page of §5.2 should be a table (limitation → effect → fix) — reads faster than prose.

---

### References (1 p, IEEE)

The 13 entries are already written into `template/main.tex`. Citation map:
[1][2][3][4] → §3.3 · [5][6] → §3.2 · [7] → §3.1 · [8][9][10] → §3.6 · [11] → §4.8
· [12] → §3.7 · [13] → §5.3.

---

## A5. Figure and table inventory

| ID | Content | Source |
|---|---|---|
| Fig 1.1 | Shared pipeline block diagram | draw (TikZ or draw.io) |
| Fig 3.1 | Sentence-length distribution | `figures/01_length_distribution.png` |
| Fig 3.2 | Three architectures, side by side | draw |
| Fig 4.1 | Training curves (loss, val, lr) | `figures/02_training_curves.png` |
| Fig 4.2 | BLEU / chrF++ bars | `figures/05_results_summary.png` |
| Fig 4.3 | chrF++ vs source length | `figures/03_chrf_by_length.png` |
| Fig 4.4 | Bahdanau attention heatmap | `figures/04_attention_heatmap.png` |
| Table 2.1 | Objective → measure → report | write |
| Table 3.1 | Dataset splits | numbers §1 |
| Table 3.2 | Cleaning rules + retention | numbers §1 |
| Table 3.3 | Word vs subword tokeniser | numbers §2 |
| Table 3.4 | Hyper-parameters | numbers §3 |
| Table 3.5 | Environment / versions | numbers §9 |
| Table 4.1 | `<unk>` rates | numbers §2 |
| Table 4.2 | Best epoch / val / time | numbers §3 |
| Table 4.3 | **Headline results** | numbers §4 |
| Table 4.4 | Beam-search Δ | numbers §4 |
| Table 4.5 | Length buckets | numbers §5 |
| Table 4.6 | LR ablation v4 vs v5 | numbers §8 |

Five of the seven figures already exist as PNGs from the run. Only Fig 1.1 and Fig 3.2
need drawing.

## A6. Writing order (fastest route to a printable draft)

1. **§3.4–3.7** — protocol, decoding, metrics, environment. Mechanical. Copy values from
   `01_CANONICAL_NUMBERS.md`. ~2 h.
2. **§3.1–3.3** — dataset, tokenisation, models. ~2 h.
3. **§4.1–4.7** — results. Tables and figures come straight from the run; prose is
   caption-level plus one interpretive sentence each. ~3 h.
4. **§1 and §2** — write *after* the results so the framing matches the numbers. ~1.5 h.
5. **§5**, then the **Abstract** last. ~1 h.
6. References — already in `main.tex`; renumber if the guide wants alphabetical.

## A7. Traps to avoid

- **Describe the method, not the notebook.** Cell numbers and `PRESET` variables belong in
  the appendix, never in Chapter 3.
- **Every number in the prose must also appear in a table.** Otherwise the examiner
  cannot verify it.
- **Declare the single seed in Limitations before the examiner raises it.**
- **Never claim a 0.3-point BLEU gap as a win** — the noise band on 2,505 sentences is
  ±0.5–1.0. Rank by chrF++ and treat BLEU as secondary.
- **Do not claim the Transformer is competitive.** It trails by 10.65 chrF++ points. Frame
  it as a data-hunger result with a documented instability and fix.
- **Disclose that the Transformer LR was tuned after observing divergence** — that is a
  hyper-parameter search on the validation set, and honesty here protects the result.

---

# PART B — THE PRESENTATION

16 slides, 15 minutes → **~50 seconds per slide**. Rule: no slide has more than 40 words
of body text; every slide has one visual.

| # | Slide | Content | Visual |
|---|---|---|---|
| 1 | **Title** | Title, name, roll, guide, department, date | College logo |
| 2 | **Agenda** | 5 bullets, 10 words total | — |
| 3 | **Problem** | En→Hi is under-resourced; word-level vocabularies break on Hindi morphology | Big stat: **8.85 % `<unk>`** |
| 4 | **Research question** | "Under a fixed 100 K-pair / single-GPU budget, how much does architecture alone buy?" | One line, huge type |
| 5 | **Objectives O1–O5** | Five one-liners | Numbered column |
| 6 | **Dataset** | IITB En–Hi; 1.65 M → 99,561 train / 3,000 val / 2,505 test | Table 3.1 + length histogram |
| 7 | **Tokenisation** | Word 8.85 % vs subword **0.001 %** `<unk>` | Table 4.1, arrow graphic |
| 8 | **Three architectures** | Vanilla / Bahdanau / Transformer, same interface | Fig 3.2 (three columns) |
| 9 | **Training protocol** | One recipe; LR schedules differ by design | Table 3.4 |
| 10 | **Headline results** | The main table — 3 models × 3 metrics × 2 decoders | Table 4.3 (colour the winner) |
| 11 | **Beam vs greedy** | Beam helps BLEU, slightly hurts chrF++ for RNNs | Table 4.4 |
| 12 | **Length analysis** | All three improve with length — contradicts the textbook expectation | Fig 4.3 |
| 13 | **Attention alignment** | Bahdanau heatmap, near-monotone diagonal | Fig 4.4 |
| 14 | **Transformer instability** | lr 6.99e-4 → 3.84e-4: chrF++ 3.49 → 7.91, collapse → working | Table 4.6, before/after |
| 15 | **Conclusions + limitations** | 3 conclusions with numbers; 3 limitations | Two columns |
| 16 | **Future scope / Thank you** | 4 bullets + questions | — |

## B1. Slides that will win or lose the review

- **Slide 14 is your best slide.** A model that collapsed, a diagnosis, a fix, a quantified
  before/after — that is research. Do not bury it.
- **Slide 3 and 7 carry the same number.** Open with the problem (8.85 % `<unk>`) and close
  the loop on slide 7 (0.001 %). That symmetry is what an examiner remembers.
- **Slide 10 must be readable from the back of the room.** Six columns of numbers is a
  lot — use 20 pt minimum, bold the winning cell, grey out the rest.
- **Slide 15 must admit the single seed.** Say it before they ask.

## B2. Likely questions and the answers

| Question | Answer |
|---|---|
| "Why is BLEU so low?" | 100 K pairs, 12 epochs, from scratch, no pretrained weights. chrF++ 18.56 is the meaningful figure. |
| "Why does the Transformer lose?" | Data hunger plus a Noam peak tuned for 6× larger batches. Documented in §4.7 with a quantified fix. |
| "Why only one seed?" | Compute budget. Error bars are the first item in future scope. |
| "How is this different from published IITB results?" | They train on the full 1.65 M with pretrained embeddings and far more epochs. This is a *controlled* comparison, not a SOTA attempt. |
| "Why is validation only 520 sentences?" | That is the corpus's official split; the preset borrows 2,480 from train to reach 3,000. Disclosed in Limitations. |

## B3. Production notes

- Build in PowerPoint (`.pptx`), 16:9, 28 pt body minimum, 40 pt titles.
- One idea per slide; if a slide needs two sentences of explanation, split it.
- Figures: export the run PNGs at 200 dpi; do not upscale the 128-px thumbnails.
- Rehearse to 14 minutes, not 15 — leave buffer for a slow projector.

---

## Deliverables checklist

- [ ] `report/main.tex` compiled to a 30-page PDF with the college class
- [ ] All 7 figures present and referenced
- [ ] All 18 tables present and referenced
- [ ] Every number traceable to `01_CANONICAL_NUMBERS.md`
- [ ] 16-slide `.pptx`
- [ ] Rehearsed once end-to-end
