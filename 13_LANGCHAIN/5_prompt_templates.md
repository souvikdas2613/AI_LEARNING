# Prompt templates in LangChain

Note **5** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`4_langchain_vs_langgraph.md`](./4_langchain_vs_langgraph.md) · **Next:** [`6_indexes_loaders_retrievers_vector_stores.md`](./6_indexes_loaders_retrievers_vector_stores.md)

Related: [`user_prompt_system_prompt.md`](../2_USER_PROMPT_SYSTEM_PROMPT/user_prompt_system_prompt.md)

---

## Why prompt templates?

LangChain provides **prompt templates** — strings (or message templates) with **placeholders** filled at runtime.

Benefits:

- **Reuse** the same prompt shape across the app.
- **Parameterize** user inputs, retrieved context, chat history, etc.
- Make **prompt engineering** easier to maintain than scattered f-strings.

---

## Example — `PromptTemplate`

Create a template, declare **input variables**, and format with user data:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["topic", "audience"],
    template=(
        "Write a short paragraph about {topic} "
        "for an audience of {audience}."
    ),
)

prompt = template.format(topic="vector databases", audience="beginners")
print(prompt)
```

Chain the template with a model (conceptually):

```python
# With LCEL (optional): prompt | llm
# Or pass `prompt` into an LLMChain (see 8_chains.md)
```

---

## Chat prompt templates

For chat models, use **message** templates (`ChatPromptTemplate`, `SystemMessagePromptTemplate`, `HumanMessagePromptTemplate`) so **system** and **user** roles stay explicit.
