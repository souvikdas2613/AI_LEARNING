# 1.6 Deep Learning

Deep learning sits inside machine learning. It uses **multi-layer neural networks** that can learn useful representations of data with less hand-crafted feature engineering.

---

## The produce aisle gets harder

The store expands: nectarines and plums (stone fruits), blackberries and cranberries (berries), mangoes and star fruit (tropical). Products also come in different sizes, shapes, and colors.

Hand-written features (“if round and red…”) become painful. **Deep learning** helps by learning features from the data itself.

---

## What makes deep learning different?

Deep learning models reduce the need for manual **feature extraction**.

For sorting fruit, you can train on **dozens (or more) of fruit pictures**. The model processes images through **layers of a neural network**. What counts as a useful feature is learned inside that process, without you defining every visual rule by hand.

---

## Real-world examples

| Example | Type | What it does |
|---------|------|----------------|
| **Amazon Rekognition** | Deep learning (vision) | Analyze images and video at scale |
| **Amazon Q Developer** | Generative AI app | Suggest code from comments and existing code |

---

## Generative vs discriminative models

Deep learning models (and ML models in general) often fall into two types:

### Discriminative models

- Used to **classify** or **predict labels** for data points
- Trained on labeled data
- Learn the relationship between features and labels
- After training: predict the label for new points

**Role:** discriminate between kinds of data (e.g. berry vs tropical).

### Generative models

- Learn a **probability distribution** over data
- Can **generate new data instances** (new content)
- Examples of generative AI: text, images, code suggestions

**Role:** generate new samples that look like they came from the same distribution.

| | Discriminative | Generative |
|--|----------------|------------|
| Main job | Predict / classify | Create new examples |
| Typical output | Label, score, class | Text, image, audio, code, … |

---

## Key takeaway

**Deep learning** = powerful ML with neural nets that learn features automatically — strong for images, speech, language, and generative applications — while still being a way to **calculate predictions** (or generate content) from patterns in data.
