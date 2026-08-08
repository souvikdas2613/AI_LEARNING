# 18. AI vs ML vs DL

A side-by-side comparison of **Artificial Intelligence**, **Machine Learning**, and **Deep Learning**.

Quick nesting reminder:

```text
AI  ⊃  ML  ⊃  Deep Learning
```

For the grocery-store story version, see also [03_ai_vs_ml_vs_deep_learning.md](03_ai_vs_ml_vs_deep_learning.md).

---

## 18.1 Artificial Intelligence

| Aspect | AI |
|--------|-----|
| **Goal** | Simulate human intelligence to perform tasks and make decisions |
| **Data** | May or may not need large datasets; can use predefined rules |
| **How it works** | Can be **rule-based**, with human programming and intervention |
| **Scope** | Simple to complex tasks, across many domains |
| **Algorithms** | Simple or complex, depending on the application |
| **Training cost** | Rule-based systems may need **less** training time and resources |
| **Interpretability** | Often more interpretable when based on explicit human rules |
| **Examples** | Virtual assistants, recommendation systems, and more |

**In one line:** AI is the broad field — systems that act intelligently, including rules, search, ML, and DL.

---

## 18.2 Machine Learning

| Aspect | Machine Learning |
|--------|------------------|
| **Goal** | Subset of AI that uses algorithms to **learn patterns from data** |
| **Data** | Heavily relies on **labeled data** for training and predictions (especially supervised ML) |
| **How it works** | Automates learning from data; **less** hand-written rules for every case |
| **Scope** | Data-driven tasks: classification, regression, and similar |
| **Algorithms** | Decision trees, SVMs, random forests, and many others |
| **Training cost** | Varies with algorithm complexity and dataset size |
| **Interpretability** | Can be interpretable or opaque, depending on the algorithm |
| **Examples** | Image recognition, spam filtering, and other data tasks |

**In one line:** ML trains a model on data so it can predict on new data — without coding every rule by hand.

---

## 18.3 Deep Learning

| Aspect | Deep Learning |
|--------|---------------|
| **Goal** | Subset of ML that uses **artificial neural networks** for complex tasks |
| **Data** | Needs **extensive** labeled data; shines with **big** datasets |
| **How it works** | **Automates feature extraction** — less manual feature engineering |
| **Scope** | Complex tasks: image recognition, NLP, and more |
| **Algorithms / models** | Deep neural networks with many hidden layers |
| **Training cost** | Needs **substantial** compute and time |
| **Interpretability** | Often **less** interpretable (complex architectures) |
| **Examples** | Autonomous vehicles, speech recognition, advanced AI apps |

**In one line:** Deep learning is ML with deep nets that learn features themselves — powerful, data-hungry, and often less transparent.

---

## Comparison at a glance

| | **AI** | **ML** | **Deep Learning** |
|--|--------|--------|-------------------|
| **Relationship** | Broadest field | Subset of AI | Subset of ML |
| **Rules vs data** | Rules *or* data | Learns from data | Learns from data (often lots) |
| **Feature engineering** | Hand rules / varies | Often manual features | Features learned automatically |
| **Data need** | Optional for rule systems | Usually significant | Typically very large |
| **Compute** | Can be light (rules) | Medium–high | Often very high |
| **Interpretability** | Often clearer (rules) | Mixed | Often harder |
| **Typical strengths** | Wide toolkit | Structured prediction tasks | Vision, speech, language, complex patterns |

---

## Key takeaway

- **AI** = the umbrella (rules, agents, ML, DL, …)  
- **ML** = learn patterns from data to make predictions  
- **DL** = neural-net ML that learns features and scales with big data and compute  

Use AI when the problem fits rules or a mix of techniques; use ML when you have labeled (or structured) data; use deep learning when the task is complex and you have enough data and compute.
