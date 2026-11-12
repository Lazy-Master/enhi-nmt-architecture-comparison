import json
from pathlib import Path

TEX = Path(r"C:\Users\anish\Downloads\EnHi_NMT_Report_and_PPT\template\main.tex")
s = TEX.read_text(encoding="utf-8")


def sub(old, new, label):
    global s
    assert old in s, f"anchor missing: {label}"
    assert new not in s, f"already patched: {label}"
    s = s.replace(old, new, 1)
    print(f"  ok  {label}")


# ------------------------------------------------------------------ splits
sub(
    r"""\begin{tabular}{@{}lrrr@{}}
\toprule
Split & Sentences & Mean tokens (EN) & Mean tokens (HI) \\
\midrule
Train & 100,000 & -- & -- \\
Validation & 3,000 & -- & -- \\
Test & 3,000 & -- & -- \\
\bottomrule
\end{tabular}""",
    r"""\begin{tabular}{@{}lrrr@{}}
\toprule
Split & Raw pairs & After cleaning & Used in this study \\
\midrule
Train      & 1,652,981 & 1,377,338 & 99,561 \\
Validation &       520 &       520 &  3,000 \\
Test       &     2,507 &     2,505 &  2,505 \\
\bottomrule
\end{tabular}

\vspace{2pt}
{\footnotesize Train retains 83.3\,\% after de-duplication and length-ratio filtering.
The training budget of 99,561 is 100,000 subsampled pairs minus 439 dropped as
over-length after subword encoding. Validation is the 520 official sentences plus
2,480 held out from train; the official test set is 2,505 after cleaning.}""",
    "tab:splits",
)

# ------------------------------------------------------------------ models
sub(
    r"""Embedding / $d_{model}$ & 300 & 300 & 512 \\
Hidden / layers & 512 / 2 & 512 / 2 (bi) & 4+4 layers, 8 heads \\
Parameters & $\approx$5.9 M & $\approx$13.6 M & -- M \\""",
    r"""Embedding / $d_{model}$ & 300 & 300 & 512 \\
Hidden / layers & 512 / 1 & 512 / 1 (bi) & 4+4 layers, 8 heads \\
FFN / attention dim & --- & 512 & 2,048 \\
Dropout & 0.3 & 0.3 & 0.1 \\
Parameters & 43.15 M & 94.80 M & 62.23 M \\""",
    "tab:models",
)

# ------------------------------------------------------------------ unk
sub(
    r"""\begin{tabular}{@{}lrr@{}}
\toprule
 & Token-level \texttt{<unk>} & Sentences with \texttt{<unk>} \\
\midrule
Word-level (Hindi) & -- \% & -- \% \\
SentencePiece (Hindi) & -- \% & -- \% \\
\bottomrule
\end{tabular}""",
    r"""\begin{tabular}{@{}lrr@{}}
\toprule
Tokenisation & Hindi vocabulary & Token-level \texttt{<unk>} \\
\midrule
Word-level (min.\ freq.\ 2) & 43,774 & 8.85\,\% \\
SentencePiece Unigram       & 32,000 & 0.001\,\% \\
\bottomrule
\end{tabular}

\vspace{2pt}
{\footnotesize Measured on the 2,505-sentence test set. Under subword tokenisation
0.0\,\% of sentences contain any \texttt{<unk>} at all. The English side drops from
11.97\,\% word-level OOV to 0.000\,\%.}""",
    "tab:unk",
)

# ------------------------------------------------------------------ main results
sub(
    r"""Vanilla LSTM & -- & -- & -- & -- & -- & -- \\
+ Bahdanau & -- & -- & -- & -- & -- & -- \\
Transformer & -- & -- & -- & -- & -- & -- \\""",
    r"""Vanilla LSTM & 1.334 & 14.796 & 100.814 & 1.524 & 13.649 & --- \\
+ Bahdanau   & \textbf{2.665} & \textbf{18.560} & \textbf{98.656} & \textbf{3.307} & \textbf{17.929} & --- \\
Transformer & 0.427 & 7.911 & 213.607 & 0.941 & 9.094 & --- \\""",
    "tab:main",
)

# ------------------------------------------------------------------ errors
old_err = s[s.index(r"\caption{Representative translation errors.}"):]
end = old_err.index(r"\end{table}") + len(r"\end{table}")
old_block = old_err[:end]

new_block = r"""\caption{Representative translation errors.}
\label{tab:errors}
\begin{tabular}{@{}p{4.2cm}p{1.9cm}p{5.2cm}p{2.2cm}@{}}
\toprule
Source (EN) & Model & Hypothesis (glossed) & Failure class \\
\midrule
A black box in your car? & Vanilla &
  Fluent Hindi about ``one's own child''; no content from the source &
  Semantic drift \\[4pt]
Australian woman appeals Thai jail time & Vanilla &
  \textit{samay samay samay} (``time'', repeated three times) &
  Repetition loop \\[4pt]
An Obama voter's cry of despair & Bahdanau &
  A single stray word, then the sentence is abandoned &
  Truncation \\[4pt]
The usually dull arena of highway planning\ldots & Transformer &
  \textit{bahut se bahut se bahut se\ldots} (``many'', repeated) &
  Repetition loop \\[4pt]
Libertarians have joined environmental groups\ldots & Bahdanau &
  Starts with a stray ``3.'' and drifts into an invented clause &
  Hallucinated content \\
\bottomrule
\end{tabular}

\vspace{2pt}
{\footnotesize Hypotheses are glossed in roman script because the class file is built
for pdf\LaTeX{} and carries no Devanagari font. To typeset the original Hindi output,
switch the build to Xe\LaTeX{}, add \texttt{\textbackslash usepackage\{fontspec\}} and
a Devanagari face such as Noto Sans Devanagari, and replace the glosses with the raw
hypotheses from \texttt{results.json}.}"""

s = s.replace(old_block, new_block, 1)
print("  ok  tab:errors")

TEX.write_text(s, encoding="utf-8")
print("\nmain.tex tables filled")
