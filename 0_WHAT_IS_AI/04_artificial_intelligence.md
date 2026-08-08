# 1.4 Artificial Intelligence

Continuing the produce department story from [03_ai_vs_ml_vs_deep_learning.md](03_ai_vs_ml_vs_deep_learning.md).

---

## Sorting with programmed rules

To separate stone fruits, berries, and tropical fruits, you can write **programmed rules** — classic **if-else** logic. The machine reads the label and routes items to the right basket.

Example:

```python
if berries_is_on_label:
    route_items_to_center_basket()
else:
    redirect_item_to_main_basket()
```

Here the “intelligence” is mostly **human-written logic**. The machine follows instructions you defined.

That still counts as AI in a broad sense: a system that acts to achieve a goal (correct sorting) without a human physically doing every step.

---

## AI as a discipline

One way to think about it:

> **AI is a discipline**, like how physics is a discipline of science.

AI is a branch of **computer science** concerned with creating **intelligent agents** — systems that can reason, learn, and act with a degree of autonomy.

Not all AI is machine learning. Rule-based systems, search, planning, and expert systems are also part of the AI family.

---

## Limits of the rule-based approach

Rules work when:

- Labels are reliable
- Categories are few and clear
- You can write and maintain every case

They break down when:

- Products vary in size, shape, color, packaging
- Labels are missing or inconsistent
- The catalog keeps growing

That is where **Machine Learning** becomes useful — next note.

---

## Key takeaway

**AI** is the broad field. A simple AI solution can be hand-coded rules. The next step in the story is teaching the machine from **data** instead of writing every rule yourself.
