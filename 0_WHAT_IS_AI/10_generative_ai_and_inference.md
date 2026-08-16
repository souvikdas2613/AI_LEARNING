# 19. Generative AI (GenAI)

Generative AI creates **new content** — conversations, stories, images, videos, music, code, and more — instead of only classifying or scoring existing data.

---

## 19.1 Introduction

### What is generative AI?

**Generative AI** is a type of AI that can create **new, original content** people have not seen before.

Like all AI, it is powered by **machine learning models**. In practice, modern GenAI is powered by **very large models** pretrained on **vast** collections of data.

| Point | Detail |
|-------|--------|
| **Parent field** | GenAI is typically treated as a **subset of deep learning** (artificial neural networks) |
| **Data** | Can use labeled and unlabeled data |
| **Learning styles** | Supervised, unsupervised, and semi-supervised methods |
| **LLMs** | Large Language Models are also a subset of deep learning |

---

### Generative vs discriminative

Most traditional AI systems people meet first are **discriminative**: they **predict** or **classify**.

**Generative** models are different: given a **prompt**, they **generate** new content.

| | Discriminative | Generative |
|--|----------------|------------|
| **Job** | Predict / classify | Create new content |
| **Example** | Tell a bicycle from a truck | Generate a **new** image that looks like a bicycle |
| **Outputs** | Labels, scores, classes | Images, video, music, synthetic data, essays, Q&A, code, … |

**Distinction:** generative AI’s hallmark is producing content that feels **new** and **creative**, at high quality and speed.

Quick mental picture: someone types `"butterflies, flowers, mountains"` into an image generator and gets several new images instantly — that is GenAI in action.

GenAI’s uniqueness, quality, and speed of content creation are why it has drawn global attention — often compared (in impact) to earlier transformative technologies.

---

### What are foundation models?

**Foundation models (FMs)** are advanced AI models trained on **extensive datasets** across domains, often with **unsupervised** or **self-supervised** learning.

That training builds a broad grasp of complex patterns — from natural language to visual content. The word **“foundation”** means they can serve as a **base** for many specialized applications.

Also called:

- Foundation models  
- Sometimes **general-purpose AI (GPAI)** systems  

They can handle a **range of general tasks** (text synthesis, image manipulation, audio generation, and more).

**Notable examples**

| Model | Notes |
|-------|--------|
| **GPT-3 / GPT-4** (OpenAI) | Foundation models behind ChatGPT-style agents |
| **DALL·E 2** | Image generation |
| **BERT** | Bidirectional Encoder Representations from Transformers |

The term **foundation model** was coined by researchers at the **Stanford Center for Research on Foundation Models** and the **Stanford Institute for Human-Centered Artificial Intelligence (HAI)** in a 2021 paper: *“On the Opportunities and Risks of Foundation Models.”*

**Why regulation is hard but important:** apps are often **built on top of** or **fine-tuned from** an FM. Errors or issues at the foundation level can affect **every** downstream application.

**Platforms** that help organizations build, train, and deploy models include Amazon SageMaker, IBM watsonx, Google Cloud Vertex AI, and Microsoft Azure AI.

---

### Foundation models, LLMs, and GenAI together

Generative AI is often powered by **large language models (LLMs)** pretrained on internet-scale data. Those large pretrained models are commonly called **foundation models**.

| Traditional ML | Foundation-model approach |
|----------------|---------------------------|
| Gather labeled data **per task** | Pretrain one large FM once |
| Train **many** separate models | **Adapt the same FM** to many tasks |

**How LLMs generate text:** they predict the **next word (token)** using position and context in the sequence — and use that ability repeatedly to produce new content.

**Business / UX uses of GenAI**

- Chatbots and virtual assistants  
- Intelligent contact centers  
- Personalization  
- Content moderation  
- (and many creative / coding workflows)

---

## 19.2 Inference in AI

### What is inference?

**AI inference** is the process where a **trained** model uses what it learned to analyze **new, unseen** data and make **predictions or decisions**.

It is the **operational phase** of AI — the model in action in the real world — drawing conclusions without needing a fresh labeled example of every desired outcome at runtime.

For generative / LLM systems, inference often means: use a **pretrained** model at runtime to **predict the next token** given the current input (and improve that path with various performance techniques).

---

### Training vs inference

| Phase | What happens |
|-------|----------------|
| **Training** | First phase. Trial-and-error and/or showing examples of desired inputs and outputs. Weights are **learned** and updated. |
| **Inference** | After training. Apply the fixed model to new inputs. Better training / fine-tuning → better inferences (never perfect). |

In decision-making terms: inference is how machines draw conclusions, predict outcomes, and help solve problems once learning is done.

---

### Inference — bullets to remember

**What it is**

- Using the **trained** model to make predictions or generate outputs  
- **No learning** here — weights are **frozen**  
- Like “reading from memory” and applying what it already knows  

**Goal**

- Produce answers, predictions, or text **efficiently**

**Analogy**

- Training = studying for an exam  
- Inference = **taking** the exam — not learning new material, applying what was studied  

**LLM example**

- You ask ChatGPT: *“Write me a poem about the moon.”*  
- The model uses trained knowledge (via next-token prediction) to **generate** text — that generation step is **inference**

---

## Key takeaways

1. **GenAI** creates new content; **discriminative** AI mainly classifies or predicts labels.  
2. Modern GenAI leans on **deep learning**, especially **LLMs** and other **foundation models**.  
3. **Foundation models** are broad pretrained bases you adapt to many apps — powerful, and cascading if wrong.  
4. **Training** teaches the model; **inference** is the model running on new inputs with frozen weights.
