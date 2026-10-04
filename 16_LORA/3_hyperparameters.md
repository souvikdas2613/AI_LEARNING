# Hyperparameters

Chapter notes (folder `16_LORA`). Related: [`simple_finetune.ipynb`](../15_MODEL_FINE_TUNING/simple_finetune.ipynb) · LoRA-specific knobs (`r`, `lora_alpha`): [`1_what_is_lora.md`](1_what_is_lora.md#hyperparameters-starting-points).

**Hyperparameters** are the settings you choose **before/during training** that control *how a machine-learning model learns*.

Think of them as **training controls**, not knowledge the model learns itself.

---

## Example from your fine-tuning code

```python
hyperparameters={
    "n_epochs": 1,
    "batch_size": 1
}
```

### 1. `n_epochs`

How many times the model goes through the **entire training dataset**.

If you have 1,000 training examples:

```text
1 epoch  → sees all 1,000 once
2 epochs → sees all 1,000 twice
3 epochs → sees all 1,000 three times
```

More epochs can help the model learn the training data better, but too many can cause **overfitting**.

### 2. `batch_size`

How many examples the model processes **together before updating its weights**.

```text
batch_size = 1
→ process 1 example
→ update
→ process next example
→ update
```

With:

```text
batch_size = 32
```

it processes 32 examples, then performs an update.

---

## Other common hyperparameters

| Hyperparameter  | Controls                                                                  |
| --------------- | ------------------------------------------------------------------------- |
| `learning_rate` | How big each learning step is                                             |
| `epochs`        | How many times to see the dataset                                         |
| `batch_size`    | Examples processed per update                                             |
| `weight_decay`  | Regularization / prevents overfitting                                     |
| `dropout`       | Randomly disables neurons during training                                 |
| `temperature`   | Mainly controls randomness during generation, not standard model training |
| `max_depth`     | Tree-model complexity                                                     |
| `n_estimators`  | Number of trees in ensemble models                                        |

For **LoRA / QLoRA** training you will also tune adapter-specific settings (e.g. `r`, `lora_alpha`, target modules) — see the table in [`1_what_is_lora.md`](1_what_is_lora.md#hyperparameters-starting-points).

---

## The key distinction

**Parameters** → learned by the model.

```text
weights
biases
```

**Hyperparameters** → chosen by **you**.

```text
learning_rate = 0.001
epochs = 3
batch_size = 32
```

So in your fine-tuning example:

```text
Training data
      ↓
Model
      ↓
Hyperparameters tell it HOW to learn
      ↓
Updated model parameters
```

That's why they're called **hyper**parameters — they're parameters **about the training process**, rather than the model's learned parameters.
