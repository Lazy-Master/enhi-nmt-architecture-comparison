# Canonical numbers — single source of truth

Every number that appears in the report or the PPT must come from this file. If a value
is needed and isn't here, it does not go in the document.

Source: Kaggle run `v5 transformer lr0.55`, 24 Oct 2026, `Ran in 1 hour and 17 minutes`,
GPU T4 x2. Full log: `kaggle_run_v5_final.log` (502 lines).

---

## 1. Dataset — IIT Bombay English–Hindi

Raw split sizes:

| split | pairs |
|---|---|
| train | 1,652,981 |
| validation | 520 |
| test | 2,507 |

Sentence length in **words**:

| | English | Hindi |
|---|---|---|
| mean | 13.1 | 14.1 |
| p50 | 9.0 | 9.0 |
| p90 | 30.0 | 33.0 |
| p95 | 40.0 | 44.0 |
| p99 | 68.0 | 76.0 |
| max | 1,917 | 1,380 |

After cleaning (NFKC, dedup, Devanagari validation, length-ratio filter):

| split | before | after | kept |
|---|---|---|---|
| train | 1,652,981 | 1,377,338 | 83.3 % |
| validation | 520 | 520 | 100.0 % |
| test | 2,507 | 2,505 | 99.9 % |

Length-cut sensitivity (word-level, before subword encoding):

| percentile | cut (words) | pairs kept |
|---|---|---|
| p90 | 32 | 88.7 % |
| p95 | 42 | 94.0 % |
| p97 | 50 | 96.2 % |
| p99 | 72 | 98.7 % |

**Budget actually used (the `balanced` preset):**

| split | pairs | composition |
|---|---|---|
| train | **99,561** | 100,000 subsampled from official train, minus 439 dropped as over-length after subword encoding |
| validation | **3,000** | 520 official + 2,480 held out from train |
| test | **2,505** | official test |

> ⚠️ The validation set is really only 520 official sentences. `val_subset = 3000`
> borrows from train. State this in Limitations.

---

## 2. Tokenisation — the headline result

Word-level baselines (min frequency ≥ 2, fitted on the 100,000 training pairs):

| language | vocabulary | OOV on test |
|---|---|---|
| English | 49,955 | 11.97 % |
| Hindi | 43,774 | **8.85 %** |

Subword (SentencePiece, Unigram, 32,000 pieces per language, pad 0 / unk 1 / bos 2 / eos 3):

| language | vocabulary |
|---|---|
| English | 32,000 |
| Hindi | 32,000 |

**The number to headline:**

| tokenisation | Hindi `<unk>` rate on test |
|---|---|
| word-level | **8.85 %** |
| SentencePiece subword | **0.001 %** |

Reduction ≈ **4 orders of magnitude**. This is the strongest single result in the study
and should open Chapter 4.

---

## 3. Models and training

| model | parameters | best epoch | best val loss | best val ppl | final train loss | train time |
|---|---|---|---|---|---|---|
| Vanilla Seq2Seq | **43.15 M** | 10 | 4.6957 | 109.48 | 3.6672 | 51.2 min |
| Seq2Seq + Bahdanau | **94.80 M** | 6 | 4.3803 | 79.86 | 2.6522 | 120.8 min |
| Transformer | **62.23 M** | 7 | 6.5154 | 675.49 | 6.7155 | 59.0 min |

Stopping behaviour:

| model | epochs run | stopped | note |
|---|---|---|---|
| Vanilla | 12 | ran to cap | patience 3 never triggered; restored epoch 10 |
| Bahdanau | 9 | early stop | restored epoch 6 |
| Transformer | 11 | early stop | restored epoch 7; patience 4 |

Shared recipe: Adam (β = 0.9/0.98, ε = 1e-9), grad-clip 1.0, AMP on,
batch 128, max 128 subword tokens, seed 42, no pretrained weights.

Per-model LR schedule:

| model | scheduler | lr | warmup | label smoothing | patience |
|---|---|---|---|---|---|
| Vanilla | ReduceLROnPlateau | 1e-3 | — | 0.0 | 3 |
| Bahdanau | ReduceLROnPlateau | 1e-3 | — | 0.0 | 3 |
| Transformer | Noam | **0.55** (peak 3.84e-4) | 4,000 steps | 0.1 | **4** |

Architecture hyper-parameters: emb 300, hidden 512 (LSTM, 2 layers, bidirectional encoder),
attn dim 512, d_model 512, 8 heads, 4 enc + 4 dec layers, FFN 2,048, dropout 0.3 (LSTM)
/ 0.1 (Transformer), tied target embedding.

---

## 4. Test-set results

greedy n = 2,505 · beam k = 5, n = 1,000 · length penalty α = 0.7

| model | params (M) | best val | BLEU (greedy) | chrF++ (greedy) | TER (greedy) | BLEU (beam k=5) | chrF++ (beam) |
|---|---|---|---|---|---|---|---|
| Seq2Seq + Bahdanau | 94.80 | 4.3803 | 2.665 | **18.560** | 98.656 | **3.307** | 17.929 |
| Vanilla Seq2Seq | 43.15 | 4.6957 | 1.334 | 14.796 | 100.814 | 1.524 | 13.649 |
| Transformer | 62.23 | 6.5154 | 0.427 | 7.911 | 213.607 | 0.941 | 9.094 |

Best chrF++: Bahdanau 18.56 · Worst: Transformer 7.91 · **Spread 10.65 chrF++ points**

Beam-search gain (ΔBLEU, greedy → beam k=5):

| model | ΔBLEU | ΔchrF++ |
|---|---|---|
| Vanilla | +0.190 | −1.147 |
| Bahdanau | +0.642 | −0.631 |
| Transformer | +0.514 | +1.183 |

> Beam raises BLEU for all three but *lowers* chrF++ for the two RNNs. Worth one
> sentence of discussion — beam optimises sequence likelihood, not character overlap.

---

## 5. chrF++ by source sentence length

| source words | Bahdanau | Transformer | Vanilla |
|---|---|---|---|
| 0–10 | 16.77 | 8.55 | 12.81 |
| 10–20 | 18.54 | 7.71 | 14.14 |
| 20–30 | 18.38 | 8.05 | 14.96 |
| 30–200 | 19.12 | 7.88 | 15.65 |

All three **improve** with length. The fixed-vector degradation predicted in the
introduction is not visible at this data budget.

---

## 6. Output length behaviour

| model | mean hyp words | mean ref words | ratio | empty outputs | max hyp words |
|---|---|---|---|---|---|
| Vanilla Seq2Seq | 22.7 | 22.8 | 0.996 | 0 | 93 |
| Seq2Seq + Bahdanau | 22.9 | 22.8 | 1.007 | 0 | 128 |
| Transformer | 46.8 | 22.8 | **2.058** | 0 | 128 |

A ratio near 1.0 means the model is not systematically over- or under-generating.
The Transformer over-generates by ~2×.

---

## 7. Transformer training curve (v5)

| epoch | train | val | ppl | lr | flag |
|---|---|---|---|---|---|
| 1 | 60.13 | 23.39 | — | 7.47e-05 | *best* |
| 2 | 17.37 | 11.18 | 71,381 | 1.49e-04 | *best* |
| 3 | 9.64 | 7.92 | 2,750 | 2.24e-04 | *best* |
| 4 | 7.73 | 7.19 | 1,327 | 2.99e-04 | *best* |
| 5 | 7.17 | 7.01 | 1,105 | 3.73e-04 | *best* |
| 6 | 6.87 | 6.76 | 861 | 3.56e-04 | *best* |
| 7 | 6.72 | **6.5154** | 675 | 3.30e-04 | *best* |
| 8 | 10.14 | 7.82 | 2,491 | 3.08e-04 | no improve 1/4 |
| 9 | 8.46 | 7.38 | 1,597 | 2.91e-04 | 2/4 |
| 10 | 7.55 | 7.28 | 1,451 | 2.76e-04 | 3/4 |
| 11 | 7.24 | 7.37 | 1,595 | 2.63e-04 | 4/4 → stop |

## 8. Transformer learning-rate ablation (this is a real contribution)

Two runs, identical in everything except the Noam scale:

| | run v4 | run v5 |
|---|---|---|
| Noam scale | 1.0 | **0.55** |
| peak lr | 6.99e-4 | **3.84e-4** |
| patience | 3 | **4** |
| best val loss | 6.9905 | **6.5154** |
| chrF++ (greedy) | 3.494 | **7.911** |
| BLEU (greedy) | 0.056 | **0.427** |
| TER (greedy) | 405.92 | **213.61** |
| output/ref ratio | 3.983 | **2.058** |
| failure mode | repetition collapse (`एक एक एक एक …`) | none |

In v4 train loss went **7.39 (ep 4) → 10.56 (ep 5)** as lr passed 5.8e-4 — divergence
exactly as warmup ended. In v5 the worst epoch was a shallow 6.72 → 10.14 relapse at
ep 8 that recovered.

**Interpretation:** the Vaswani Noam peak assumes ~25 k tokens per batch. Here a batch is
128 sequences × ~30 subwords ≈ 4 k tokens, so gradients are far noisier and the default
peak is too aggressive. This is a genuinely reportable finding, not a footnote.

---

## 9. Environment

| item | value |
|---|---|
| GPU | NVIDIA Tesla T4 ×2, 15.6 GB per device |
| platform | Kaggle Notebooks (batch "Save & Run All (Commit)") |
| framework | PyTorch 2.x, CUDA, AMP |
| tokeniser | SentencePiece (Unigram) |
| metrics | sacrebleu — BLEU `intl`, chrF++, TER |
| wall clock | 1 h 17 min end-to-end (data + train + eval) |
| quota used | ~5 h of a 30 h weekly GPU allowance |

---

## 10. Numbers that must NOT be claimed

- Do **not** claim the Transformer is competitive. It trails Bahdanau by 10.65 chrF++.
- Do **not** claim a statistically significant ranking. One seed, no error bars.
- Do **not** claim the vanilla model degrades with length — the data shows the opposite.
- Do **not** compare to published IITB BLEU figures. Different subset, different split,
  no pretrained weights.
