# 1.5 Machine Learning (ML)

Machine learning is a **subfield of AI**.

---

## Definition

A machine learning **program or system trains a model from input data**. That trained model can make useful **predictions** from **new** (never-before-seen) data drawn from a similar distribution.

In other words: ML gives the computer the ability to learn **without** you writing explicit rules for every case.

---

## Back to the grocery store

To improve sorting, you expose the machine to **more data** — many examples of each fruit type and their characteristics. The more good data you provide, the better the model can get.

By providing data and adjusting parameters, the machine reduces errors through repeated training (guess → check → adjust).

---

## How ML works (features and labels)

ML trains a computer to recognize patterns in **historical data** so it can predict on **new data**.

A training dataset typically has:

| Concept | Meaning |
|---------|---------|
| **Features** | Inputs (measurements, attributes, signals) |
| **Labels** | Desired outputs (the answer you want to predict) |

**Goal:** find a formula / model that maps features → labels.

After training, the algorithm can take new data, recognize patterns, apply the learned mapping, and **predict**.

---

## Two common classes of ML models

| Type | Idea (simple) |
|------|----------------|
| **Supervised** | Learn from labeled examples (features + correct labels) |
| **Unsupervised** | Find structure in data without labels (e.g. clusters) |

(There are other families too — reinforcement learning, etc. — but supervised vs unsupervised is the usual first split.)

---

## Key takeaway

**ML = train on data → predict on new data.** You stop hand-coding every rule and instead learn patterns from examples — as long as you have enough relevant data and a clear prediction target.
