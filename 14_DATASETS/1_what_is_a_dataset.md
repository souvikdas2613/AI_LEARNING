# What is a dataset?

Chapter notes (folder `14_DATASETS`).

Make **dataset** simple first, then connect it to **ML/AI, Kaggle, RAG, and your projects**.

---

## 1. What exactly is a dataset?

A **dataset is an organized collection of data that you want to work with.**

The easiest analogy:

> **Dataset = a collection of examples/data that a computer can read and learn from or analyze.**

For example, suppose you want to build a model that predicts house prices.

You collect information about 1,000 houses:

| House |       Area | Bedrooms | Location  |  Price |
| ----- | ---------: | -------: | --------- | -----: |
| 1     | 1200 sq ft |        2 | Bangalore |   ₹80L |
| 2     | 1500 sq ft |        3 | Bangalore | ₹1.1Cr |
| 3     |  900 sq ft |        2 | Mysore    |   ₹55L |
| 4     | 2000 sq ft |        4 | Bangalore | ₹1.6Cr |

**Those 1,000 rows together are your dataset.**

---

## 2. Dataset vs data

This distinction is useful.

### Data

Individual pieces of information:

```text
1500 sq ft
3 bedrooms
Bangalore
₹1.1 crore
```

### Dataset

Those pieces organized into a collection:

```text
Area     Bedrooms     Location     Price
1200     2            Bangalore    80L
1500     3            Bangalore    1.1Cr
900      2            Mysore       55L
...
```

So:

> **Data = individual information**  
> **Dataset = organized collection of data**

---

## 3. What is a row?

Usually, each **row represents one example/record**.

For our housing dataset:

```text
1200 | 2 | Bangalore | ₹80L
```

is **one house**.

Another row:

```text
1500 | 3 | Bangalore | ₹1.1Cr
```

is another house.

So:

> **Row = one example / observation / record**

---

## 4. What is a column?

Each **column represents a characteristic/property** of that example.

```text
Area
Bedrooms
Location
Price
```

These are called **features** or **attributes**.

For example:

```text
Area = 1500
Bedrooms = 3
Location = Bangalore
Price = ₹1.1Cr
```

Here:

* `Area` → feature
* `Bedrooms` → feature
* `Location` → feature
* `Price` → target/output, if we're predicting price

---

## 5. Dataset in Machine Learning

This is where datasets become particularly important.

Suppose you want AI to predict house prices.

You give it many examples:

```text
Area    Bedrooms    Location     Price
1200       2        Bangalore     80L
1500       3        Bangalore     1.1Cr
900        2        Mysore        55L
2000       4        Bangalore     1.6Cr
...
```

The ML algorithm looks at these examples and tries to learn a relationship:

```text
Area + Bedrooms + Location
             ↓
          Price
```

Then you give it a new house:

```text
Area = 1400
Bedrooms = 3
Location = Bangalore
```

The model might predict:

```text
₹95 lakh
```

So the dataset is essentially the **experience/examples from which the model learns**.

---

## 6. Training dataset, validation dataset and test dataset

This is VERY important in ML.

You normally don't give all your data to the model for training.

Suppose you have **10,000 examples**.

You might split them:

```text
10,000 examples
       │
       ├── 8,000 → Training
       │
       ├── 1,000 → Validation
       │
       └── 1,000 → Test
```

### Training dataset

Used to **teach the model**.

```text
Examples → Model learns patterns
```

### Validation dataset

Used while developing/tuning the model.

You ask:

> "Is my model improving, and which settings work better?"

### Test dataset

Used at the end.

You ask:

> "How well does my model perform on data it has never seen?"

This is important because you don't want a model that simply **memorizes** the training data.

---

## 7. Different types of datasets

Datasets don't have to be Excel-like tables.

### Tabular dataset

Like:

```text
Age | Salary | Experience
25  | 8L     | 2 years
30  | 12L    | 5 years
```

Usually CSV, Excel, SQL tables, etc.

---

### Image dataset

Suppose you want to recognize cats and dogs.

```text
image001.jpg → Cat
image002.jpg → Dog
image003.jpg → Cat
```

Thousands of images together form an **image dataset**.

---

### Text dataset

For NLP:

```text
"I loved this movie"       → Positive
"The movie was terrible"   → Negative
"Excellent acting"         → Positive
```

That's a text dataset.

---

### Audio dataset

For speech recognition:

```text
audio001.wav → "Hello"
audio002.wav → "How are you?"
```

---

### Video dataset

For things like:

* action recognition
* autonomous driving
* surveillance research
* gesture recognition

---

## 8. What is a labeled dataset?

This is another important concept.

Suppose you have:

```text
"I love this movie"
```

and someone tells the model:

```text
Positive
```

The **label** is:

```text
Positive
```

So:

```text
Input                  Label
"I love this movie" → Positive
"I hate this movie" → Negative
```

This is a **labeled dataset**.

The model can learn:

```text
Input → Correct answer
```

This is commonly used in **supervised learning**.

---

## 9. What is an unlabeled dataset?

Now imagine you have:

```text
"I love this movie"
"I hate this movie"
"The acting was amazing"
"Terrible story"
```

but nobody tells the model whether they are positive or negative.

That's **unlabeled data**.

The model can potentially discover patterns or structure without explicit labels.

This is associated with **unsupervised/self-supervised approaches**, depending on the task.

---

## 10. What is Kaggle's role?

Now Kaggle makes more sense.

Kaggle provides a huge collection of datasets.

For example:

```text
Kaggle
  ↓
Movie dataset
  ↓
Download CSV
  ↓
Python / Pandas
  ↓
Clean data
  ↓
Build ML/AI project
```

You don't have to collect all the data yourself.

That's why Kaggle is useful for **learning and experimenting**.

---

## 11. Dataset in your RAG learning

This is where it gets interesting for what you've been studying.

Suppose you create a RAG chatbot for **Red Hat documentation**.

Your source documents might be:

```text
OpenShift documentation
Kubernetes documentation
Red Hat documentation
Your own notes
```

You convert them into chunks:

```text
Chunk 1 → OpenShift networking
Chunk 2 → OpenShift storage
Chunk 3 → MachineConfig
Chunk 4 → NodePool
...
```

That collection can itself form a **retrieval/evaluation dataset**.

For example:

| Question                     | Relevant document |
| ---------------------------- | ----------------- |
| What is a NodePool?          | chunk_124         |
| How does MachineConfig work? | chunk_382         |
| What is KServe?              | chunk_521         |

Now you can test your retriever.

Question:

> "What is a NodePool?"

Retriever returns:

```text
1. chunk_124 ✅
2. chunk_500 ❌
3. chunk_521 ❌
4. chunk_300 ❌
5. chunk_382 ❌
```

Then you can calculate:

**Recall@5**

**Precision@5**

**MRR**

That's why datasets matter for **evaluating RAG**, not just training ML models.

Related notes:

* [`7_mrr_mean_reciprocal_rank.md`](../12_RAG_Retrieval_Augmented_Generation/7_mrr_mean_reciprocal_rank.md)
* [`8_recall_precision_at_k.md`](../12_RAG_Retrieval_Augmented_Generation/8_recall_precision_at_k.md)

---

## 12. What is data curation? (theory)

**Data curation** means carefully **selecting, cleaning, organizing, and documenting** data so it is trustworthy and useful for a purpose.

It is **not** the same as merely downloading a dataset.

```text
Collecting data  = getting raw information
Curating data    = making that information good enough to use
```

### Simple definition (interview-ready)

> **Data curation is the process of preparing raw data into a high-quality, organized dataset suitable for analysis, training, testing, or evaluation.**

### Why curation matters

Raw data is often:

* incomplete (missing prices, empty descriptions)
* noisy (boilerplate text, product codes, duplicates)
* inconsistent (different formats, junk values)
* unbalanced (too many cheap items, one category dominating)

If you train or evaluate on messy data, your results can be misleading.

So curation is where a lot of the **real quality** of an ML/AI system is decided — often more than tiny hyperparameter tweaks later.

### What curation usually includes

| Activity | Meaning |
|----------|---------|
| Selecting | Keep only relevant examples |
| Cleaning | Fix/remove bad values, strip noise |
| Filtering | Drop rows that fail quality rules |
| Deduplicating | Remove repeated titles/texts |
| Labeling / structuring | Shape rows into useful fields or prompts |
| Splitting | Make train / validation / test sets |
| Documenting | Know source, rules, and purpose of the dataset |

### Curation is not model training

Important distinction:

| Stage | What happens |
|-------|----------------|
| **Curation** | Prepare examples (clean text, keep good prices, build prompts) |
| **Training** | Update model weights using those examples |

So scripts that load Amazon data, filter prices, scrub text, and build prompts are **curation / data preparation**.  
They become **training** only when a model is actually optimized on that data.

### Example from this folder

```text
Hugging Face Amazon rows          ← raw / collected
        ↓
keep valid prices
scrub noisy text
build Item prompts                ← curated
        ↓
later: train a price model        ← training (separate step)
```

Related practice notes:

* [`2_amazon_appliances_dataset_simple.md`](./2_amazon_appliances_dataset_simple.md)
* [`3_working_with_dataset_and_items.md`](./3_working_with_dataset_and_items.md)

### One-line memory hook

> **Collect → Curate → Train / Evaluate**

Without curation, “more data” can mean “more garbage.”

---

## 13. One important misconception

A dataset does **NOT necessarily mean training data**.

This is important.

A dataset can be used for:

```text
Training
Testing
Validation
Evaluation
Benchmarking
Analysis
Visualization
RAG retrieval evaluation
```

So don't automatically think:

> Dataset = something used to train an AI model.

Instead:

> **Dataset = organized collection of data prepared for some purpose.**

The purpose determines how you use it.

---

## The whole picture

You can think of it like this:

```text
              RAW / COLLECTED DATA
                       │
                       ↓
                  CURATION
              (clean, filter, shape)
                       │
                       ↓
                    DATASET
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Training       Testing       Evaluation
        │              │              │
        ↓              ↓              ↓
    ML model       Performance     Recall@K
    learning       measurement     Precision@K
                                   MRR
```

And in your AI learning:

```text
Kaggle / Hugging Face
  ↓
Raw dataset
  ↓
Curation (Python / Pandas / filters / prompts)
  ↓
Train / val / test (or RAG eval set)
  ↓
ML / embeddings / RAG
  ↓
Recall@K / Precision@K / MRR  (when evaluating retrieval)
```

**The simplest definition to remember for an interview:**

> **A dataset is a structured collection of examples or observations used for analysis, training, testing, or evaluation of a machine-learning/AI system.**

**Curation definition to remember with it:**

> **Data curation is preparing raw data into a clean, organized dataset before you train or evaluate.**
