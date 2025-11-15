# How Regional Stereotypes Are Narrated

This repository contains code, example data, and writing/slides for the AEJMC 2024 project **“How regional stereotypes are narrated”** (submission \#4288).  
The project uses a **Latent Dirichlet Allocation (LDA)** topic model to explore how **regional stereotypes** are constructed and circulated in a corpus of online comments.

The focus is not only on what regions are mentioned, but **how** they are narrated: which traits, emotions, and narrative templates are repeatedly attached to different places.

---

## 1. Project overview

### Research questions

- How are different regions described and evaluated in online comments?
- What **stereotypical narratives** (e.g., “hard-working but backward”, “rich but arrogant”) emerge across regions?
- How do these narratives cluster into **recurring topics** and **discursive patterns** that go beyond individual comments?

### Approach

1. **Collect comment-level text** from online platforms where regions are routinely discussed.
2. **Pre-process** the text (cleaning, tokenization, stopword removal, basic normalization).
3. Build a **document–term matrix** and fit an **LDA topic model** to uncover:
   - dominant themes in regional talk,
   - characteristic words and phrases associated with each topic.
4. **Interpret and label** topics as **regional stereotypes** (e.g., “backward countryside”, “corrupt local officials”, “vibrant coastal cities”).
5. Use representative comments and topic distributions to discuss how regional stereotypes are **narrated, stabilized, and contested**.

The repository is intended primarily as **supplementary material** for the IAMCR 2024 presentation and as a **lightweight reproducibility package** for the modeling workflow.

---

## 2. Repository structure

At the top level, the repository contains three main folders plus the paper and slides:

```text
IAMCR2024/
├── LDAFramework/                  # LDA-related framework and HTML reports (topic inspection, summaries)
├── OriginalComments/              # Original or pre-processed comment files used as model input
├── Programming/                   # Python scripts / notebooks for cleaning text and running LDA
├── How regional stereotypes are narrated #4288.docx   # manuscript / extended abstract (Word)
├── How regional stereotypes are narrated #4288.pdf    # manuscript / extended abstract (PDF)
└── Presentation.pdf               # IAMCR 2024 presentation slides
