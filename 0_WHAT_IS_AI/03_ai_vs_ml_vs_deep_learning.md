# 1.3 Artificial Intelligence vs Machine Learning vs Deep Learning

## The grocery store story

Imagine you work in the produce department. There are dozens of products and little time to sort them by hand.

How could **AI**, **Machine Learning**, and **Deep Learning** each help?

This analogy is used across the next few notes:

| Approach | Produce department idea | Details |
|----------|-------------------------|---------|
| **AI** (rules / classical) | If-else on labels | [04_artificial_intelligence.md](04_artificial_intelligence.md) |
| **Machine Learning** | Learn from many examples | [05_machine_learning.md](05_machine_learning.md) |
| **Deep Learning** | Learn from images; features automatic | [06_deep_learning.md](06_deep_learning.md) |

---

## How they nest

```text
┌─────────────────────────────────────────┐
│         Artificial Intelligence         │
│  ┌───────────────────────────────────┐  │
│  │        Machine Learning           │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │       Deep Learning         │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

- **AI** — the broad discipline (like physics is a discipline of science)
- **ML** — a subfield of AI: learn a model from data
- **Deep Learning** — a subfield of ML: multi-layer neural networks that learn features themselves

---

## One-line contrast

| Term | One line |
|------|----------|
| AI | Make machines do tasks that usually need human intelligence |
| ML | Train a model on data so it can predict on new data |
| Deep Learning | ML with deep neural nets; less hand-crafted feature engineering |

Read the next three files for the full produce-aisle walkthrough.
