# Fine-Tuning in LLM

Chapter notes (folder `15_MODEL_FINE_TUNING`).

**LLM fine-tuning** is the process of taking pre-trained models and further training them on smaller, specific datasets to refine their capabilities and improve performance in a particular task or domain.

Fine-tuning is about turning general-purpose models into specialized models, bridging the gap between generic pre-trained models and the unique requirements of specific applications and ensuring that the language model aligns closely with human expectations.

---

## RAG vs fine-tuning

Exactly — **for many GenAI applications, RAG is the better solution.** But RAG and fine-tuning solve **different problems**.

The simplest distinction is:

> **RAG changes what the model knows at inference time. Fine-tuning changes how the model behaves.**

### Think of it like this

**RAG:**

```text
Question
   ↓
Retrieve relevant information
   ↓
LLM + information
   ↓
Answer
```

**Fine-tuning:**

```text
Question
   ↓
Fine-tuned LLM
   ↓
Answer
```

### Example: company documentation

Suppose you want an AI assistant that answers questions about Red Hat documentation.

You have:

```text
10,000 documentation pages
```

You **wouldn't normally fine-tune the model on those documents**.

Instead:

```text
User: "How do I configure X?"

        ↓

Vector search
        ↓

Relevant documentation
        ↓

LLM
        ↓
Answer based on documentation
```

That's RAG.

Why? Because documentation changes.

If Red Hat updates a document:

```text
Old documentation ❌
New documentation ✅
```

You update your vector store.

You don't need to retrain the model.

---

## So when does fine-tuning help?

Consider a different problem.

You want the model to **always produce a particular output style**.

For example:

```text
Input:
"Customer says their server is down."

Desired output:

Severity: P1
Category: Infrastructure
Action: Escalate immediately
```

You could give the model thousands of examples:

```text
Input → Desired output
Input → Desired output
Input → Desired output
...
```

Fine-tuning teaches the model the **pattern/behavior**.

RAG isn't really solving that problem.

You don't need to retrieve a document saying:

> "When a customer says X, format your response like Y."

You want the model to **learn the behavior**.

---

### Another example: structured output

Imagine you're building a model that converts messy text into your company's specific schema:

```json
{
  "customer": "...",
  "product": "...",
  "severity": "...",
  "root_cause": "...",
  "action": "..."
}
```

You have 50,000 examples of:

```text
Messy input → Correct JSON
```

Fine-tuning can make the model much better at consistently performing that specialized transformation.

RAG doesn't inherently teach the model that transformation.

---

## The really important distinction

Think about **knowledge vs behavior**:

| Problem                               |       RAG |         Fine-tuning |
| ------------------------------------- | --------: | ------------------: |
| Give model company documents          |         ✅ | Usually unnecessary |
| Frequently changing information       |         ✅ |                   ❌ |
| Private knowledge                     |         ✅ |           Sometimes |
| Teach a specific response style       |   Limited |                   ✅ |
| Consistent output format              |   Limited |                   ✅ |
| Specialized classification            | Sometimes |                   ✅ |
| Teach a recurring transformation      | Sometimes |                   ✅ |
| Reduce huge prompts                   | Sometimes |                   ✅ |
| Make model cheaper/smaller for a task |         ❌ |                   ✅ |
| Give model today's information        |         ✅ |                   ❌ |

### And you can combine them

This is actually very common conceptually:

```text
                 ┌──────────────┐
User question →  │ RAG          │
                 │ current data │
                 └──────┬───────┘
                        ↓
                 Fine-tuned LLM
                        ↓
                Specialized answer
```

So it's not:

**RAG vs fine-tuning**

It's often:

**RAG + fine-tuning**, when both are useful.

---

### One analogy that makes it very easy

Imagine hiring an employee.

**RAG = giving the employee access to your company's knowledge base.**

> "Here are the latest company documents. Look up the information you need."

**Fine-tuning = training the employee how to do their job.**

> "Here are 50,000 examples of how we classify and respond to these situations."

So if the problem is **"the employee doesn't know the latest information"** → RAG.

If the problem is **"the employee knows the information but doesn't perform the task in the way we want"** → fine-tuning.

And if it's both:

> **RAG + fine-tuning.**

That's the fundamental reason fine-tuning still exists even though RAG has become extremely useful.

---

## Practice in this folder

- Notebook: [`simple_finetune.ipynb`](simple_finetune.ipynb) — products → chat messages → JSONL → (optional) OpenAI fine-tune job
- Sample files: [`jsonl_simple/`](jsonl_simple/)

OpenAI is winding down self-serve fine-tuning for many orgs (`403 training_not_available`). The notebook still teaches the **data format**. For real training on a blocked account, use a local/open model (LoRA) or stay with prompts + RAG.
