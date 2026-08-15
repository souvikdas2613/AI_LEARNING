# Agents and Tools

Chapter notes for **Souvik’s** AI learning journey (folder `6_AGENTS_AND_TOOLS`).

Related earlier chapter: [`5_TOOLS_FUNCTIONS/README.md`](../5_TOOLS_FUNCTIONS/README.md) — tools / function calling hands-on.

---

## Tools vs Agents — are they the same?

**No** — related, but **not the same**.

| | **Tool** | **Agent** |
|---|----------|-----------|
| What it is | A **function** the LLM can request (price lookup, weather, email…) | A **system** that uses an LLM to reach a goal |
| Role | The **hands** (actions) | The **whole worker** (brain + hands) |
| Alone? | Just a capability | Brain (LLM) + tools + loop/planning |

**Simple picture:**

```text
Agent
 ├── Brain  → LLM (thinks / plans)
 └── Body   → Tools (do things in the world)
```

- **Tool** = one action (e.g. `get_ticket_price`)  
- **Agent** = the system that decides *when* to use tools and keeps going until the goal is done  

Your FlightAI chatbot with `get_ticket_price` is already a **small agent-like app**: LLM + tool.  
A bigger agent may use many tools, loop, and plan more freely.

---

## Index

| Section | Topic |
|---------|--------|
| — | [Tools vs Agents — are they the same?](#tools-vs-agents--are-they-the-same) |
| 1 | [What is an AI Agent](#1-what-is-an-ai-agent) |
| 2 | [What type of tasks can an Agent do?](#2-what-type-of-tasks-can-an-agent-do) |
| 3 | [Essential LLM Workflow Design Patterns](#3-essential-llm-workflow-design-patterns-for-building-robust-ai-systems) |
| 4 | [Agent Patterns](#4-agent-patterns) |
| 5 | [Agentic AI Frameworks (overview)](#5-agentic-ai-frameworks--overview) |
| 6 | [LLM — Large Language Model](#6-llm--large-language-model) |
| 7 | [Prompting the LLM is important](#7-prompting-the-llm-is-important) |
| 8 | [How are LLMs trained?](#8-how-are-llms-trained) |
| 9 | [How are LLMs used in AI Agents?](#9-how-are-llms-used-in-ai-agents) |
| 10 | [Agentic AI Frameworks (detail)](#10-agentic-ai-frameworks-detail) |
| 11 | [Chat Templates](#11-chat-templates) |
| 12 | [Resources](#12-resources) |
| 13 | [What are Tools?](#13-what-are-tools) |

---

## 1. What is an AI Agent

An AI model capable of **reasoning**, **planning**, and **interacting with its environment**.  
We call it an **Agent** because it has **agency** — the ability to interact with the environment.

An **Agent** is a system that leverages an AI model to interact with its environment in order to achieve a **user-defined objective**.  
It combines reasoning, planning, and the execution of actions (often via **external tools**) to fulfill tasks.

Think of the Agent as having two main parts:

### 1. The Brain (AI Model)

This is where all the thinking happens. The AI model handles reasoning and planning.  
It decides which **Actions** to take based on the situation.

### 2. The Body (Capabilities and Tools)

This part represents everything the Agent is equipped to do.

---

The most common AI model found in Agents is an **LLM** (Large Language Model), which takes **text** as input and outputs **text** as well.

Well-known examples:

- GPT-4 from OpenAI  
- Llama from Meta  
- Gemini from Google  

These models have been trained on a vast amount of text and are able to generalize well.

**LLMs are amazing models, but they can only generate text.**

However, if you ask a well-known chat application like HuggingChat or ChatGPT to generate an image, they can. How is that possible?

The answer is that the developers of HuggingChat, ChatGPT, and similar apps implemented additional functionality (**Tools**) that the LLM can use to create images (and do many other things).

```text
Brain (LLM)  →  thinks / plans / decides
Body (Tools) →  acts on the environment
```

---

## 2. What type of tasks can an Agent do?

An Agent can perform **any task we implement via Tools** to complete Actions.

For example: if I write an Agent to act as my personal assistant (like Siri) on my computer, and I ask it to  
“send an email to my Manager asking to delay today’s meeting”,  
I can give it some code to send emails.

Allowing an agent to interact with its environment enables real-life usage for companies and individuals.

### Example 1: Personal Virtual Assistants

Virtual assistants like **Siri**, **Alexa**, or **Google Assistant** work as agents when they interact on behalf of users using their digital environments.

### Example 2: Customer Service Chatbots

Many companies deploy chatbots as agents that interact with customers in natural language.

These agents can:

- answer questions  
- guide users through troubleshooting steps  
- open issues in internal databases  
- even complete transactions  

---

## 3. Essential LLM Workflow Design Patterns for Building Robust AI Systems

These are more **fixed / structured** workflows (compared to open-ended agents).

In diagrams (mental picture):

- input / output = start and end of the workflow  
- yellow boxes = calls to models / LLMs  
- blue boxes = optional code you wrote  

### Prompt Chaining

The first design pattern is **prompt chaining**.

This pattern involves having an LLM carry out some task, then potentially passing the output to a **second** LLM, then to a **third** LLM, which could be the conclusion.

Example vibe:

1. first LLM picks a sector  
2. second picks a pain point  
3. third picks a solution  

```text
Input → LLM1 → LLM2 → LLM3 → Output
```

### Routing

The second design pattern is **routing**.

An input comes in, and an LLM decides **which of multiple possible models** should carry out the function.

You might have specialist models (LLM 1, 2, 3), each good at different tasks.

The **router’s** job is to classify the task and understand which specialist is best equipped to tackle it.

This allows separation of concerns: different LLMs with different expertise, and one LLM deciding how to route to those experts.

```text
Input → Router LLM → chooses LLM1 / LLM2 / LLM3 → Output
```

### Parallelization

The third design pattern is **parallelization**.

At first glance it might look similar to routing.  
The key difference: **code (not an LLM)** breaks down the task into multiple pieces that run in parallel.

In this pattern, code (for example Python) decides how to coordinate and sends subtasks concurrently to multiple LLMs.  
Then more code aggregates or stitches together the answers.

```text
Input → Code splits → LLM1 + LLM2 + LLM3 (parallel) → Code merges → Output
```

### Orchestrator-Worker

The fourth design pattern is **orchestrator-worker**.

This involves breaking down a difficult task and recombining it.

It may seem similar to parallelization, but the key difference is that an **LLM (not code)** performs the orchestration.

- An LLM breaks down a complex task into smaller steps  
- Other LLMs carry out each expert task  
- Then an LLM synthesizes the results for the output  

This creates a more dynamic system where the orchestrator can choose how to divide the task and how many LLMs get assigned activities.

```text
Input → Orchestrator LLM plans → Worker LLMs → Orchestrator synthesizes → Output
```

### Evaluator-Optimizer

The final workflow pattern (often used by many practitioners) is called **evaluator-optimizer** by Anthropic.  
It is also known as evaluators or validation agents.

This pattern involves:

1. an LLM **generator** that produces a solution  
2. a second LLM **evaluator** that checks the work of the first LLM  

The evaluator is given extra information or context to arm itself for **validation** rather than generation.

Based on its assessment, the evaluator can **accept** or **reject** the work:

- if accepted → output proceeds  
- if rejected → evaluator provides a reason; rejection + reason go back to the generator, which produces another solution  

This creates a **feedback loop**.

```text
Generator → draft
     ↓
Evaluator → accept? → Output
     ↓ reject + reason
Generator again → improved draft ...
```

---

## 4. Agent Patterns

By contrast with workflow patterns, **agent processes are more open-ended**.

They can continue indefinitely, incorporating feedback loops.  
This design allows information to be processed multiple times.

Importantly: there is **no fixed path** through the design pattern.  
Instead, it is fluid and dynamic.

As a result, agent patterns can be much more powerful.  
They can tackle a much greater variety of problems.  
However, this flexibility comes with **less predictability**.

### The agent loop (mental model)

A human can make a request that goes to an LLM.  
The LLM can take actions on the environment and receive information back from it.

This forms a repeating loop:

```text
User request
     ↓
LLM thinks / plans
     ↓
Action on environment (often via Tools)
     ↓
Observation / feedback
     ↓
LLM thinks again ... (loop)
     ↓
LLM chooses to stop → final answer
```

This is an open-ended design pattern — almost a meta-design where the LLM chooses its own approach to solving the problem.

**Key distinction:**

| Workflow patterns | Agent patterns |
|-------------------|----------------|
| More certainty about sequence of steps | Fluid / dynamic path |
| Designed pipeline | LLM decides next step |
| More predictable | More powerful, less predictable |

---

## 5. Agentic AI Frameworks — overview

Landscape you will hear about:

| Approach | Notes |
|----------|--------|
| **No Framework** | Call LLM APIs directly (like your Gradio + tools labs) |
| **MCP** (Model Context Protocol) | Protocol (not a framework) for connecting models ↔ tools/data |
| **OpenAI Agents SDK** | Lightweight, clean, flexible |
| **Crew** | Easy / low-code, often YAML config |
| **LangGraph** | Powerful, heavier, graph of agents/tools |
| **AutoGen** | Microsoft, relatively heavyweight |

(More detail in [10](#10-agentic-ai-frameworks-detail).)

---

## 6. LLM — Large Language Model

An **LLM** is a type of AI model that excels at understanding and generating human language.

They are trained on vast amounts of text data, allowing them to learn patterns, structure, and even nuance in language.  
These models typically consist of many millions (often billions) of parameters.

Most LLMs nowadays are built on the **Transformer** architecture — a deep learning architecture based on the **Attention** algorithm, that gained significant interest since the release of **BERT** from Google in 2018.

### Three types of transformers

#### Encoders

An encoder-based Transformer takes text (or other data) as input and outputs a dense representation (or **embedding**) of that text.

#### Decoders

A decoder-based Transformer focuses on generating new tokens to complete a sequence, **one token at a time**.

#### Seq2Seq (Encoder–Decoder)

A sequence-to-sequence Transformer combines an encoder and a decoder:

1. encoder processes the input sequence into a context representation  
2. decoder generates an output sequence  

---

LLMs are a key component of AI Agents, providing the foundation for understanding and generating human language.

They can:

- interpret user instructions  
- maintain context in conversations  
- define a plan  
- decide which tools to use  

**For now: the LLM is the brain of the Agent.**

### Special tokens

Each LLM has some special tokens specific to the model.  
The LLM uses these tokens to open and close structured components of its generation — for example, to indicate the start or end of a sequence, message, or response.

The most important of those is the **End of sequence token (EOS)**.

### How next-token generation works (high level)

1. Once the input text is tokenized, the model computes a representation of the sequence that captures meaning and position of each token.  
2. This representation goes into the model, which outputs **scores** that rank the likelihood of each token in its vocabulary as being the next one.  
3. Based on these scores, we have multiple strategies to select the next tokens.  
4. The easiest decoding strategy: always take the token with the **maximum score**.

---

## 7. Prompting the LLM is important

Considering that the only job of an LLM is to predict the next token by looking at every input token (and choosing which tokens are “important”), the wording of your input sequence is very important.

The input sequence you provide an LLM is called a **prompt**.

Careful design of the prompt makes it easier to guide the generation of the LLM toward the desired output.

---

## 8. How are LLMs trained?

LLMs are trained on large datasets of text, where they learn to predict the next word in a sequence through a **self-supervised** or **masked language modeling** objective.

From this unsupervised learning, the model learns the structure of the language and underlying patterns in text, allowing the model to generalize to unseen data.

---

## 9. How are LLMs used in AI Agents?

LLMs are a key component of AI Agents, providing the foundation for understanding and generating human language.

They can:

- interpret user instructions  
- maintain context in conversations  
- define a plan  
- decide which tools to use  

**What you need to understand now:** the LLM is the **brain** of the Agent.

---

## 10. Agentic AI Frameworks (detail)

These frameworks are designed to provide **glue code** or **abstraction layers** that simplify interactions with LLMs.

They offer elegant structures for building agentic solutions, allowing developers to concentrate on the business problems they aim to solve.

There are numerous Agentic AI frameworks available, with new ones emerging frequently — making it challenging to keep up.  
This section orients you in the landscape.

### Using No Framework

Choosing not to use any AI framework means connecting directly to LLMs through their APIs (as in your earlier labs).

This approach orchestrates interactions among LLMs without additional abstraction layers.

A blog post titled **“Building Effective Agents”** makes a compelling case for often using **no framework** and connecting directly to LLMs:

- APIs are relatively simple  
- you see exactly what is happening under the hood  
- you keep detailed control over prompts  

Your FlightAI tool chatbot (`5_TOOLS_FUNCTIONS`) is this style: OpenAI API + your Python tools + Gradio.

### Model Context Protocol (MCP)

Alongside the no-framework approach, there is the **Model Context Protocol (MCP)**, developed by Anthropic (who advocate for no frameworks).

MCP is **not a framework** but an **open-source protocol** that enables models to connect to data sources and tools in an agreed and established manner.

This protocol allows elegant stitching together of models and their providers without as much custom glue code — as long as the protocol is followed.

### OpenAI Agents SDK

OpenAI Agents SDK is a lightweight, simple, clean, and flexible framework.

It is relatively new (APIs can change), but remains a strong, practical option for building agents.

### Crew

Crew has been around longer and is also easy to use and lightweight.

It offers a **low-code** approach, allowing users to assemble agents primarily through configuration (such as YAML files).

Somewhat heavier than OpenAI Agents SDK, but still accessible.

### High-level complexity frameworks

At the top level of complexity:

- **LangGraph** (from the LangChain creators)  
- **AutoGen** (Microsoft)  

These are relatively heavyweight and have a steeper learning curve (especially LangGraph).

With increased complexity comes greater power.  
LangGraph enables building computational graphs composed of agents and their tools — sophisticated systems, but you commit to that ecosystem’s terminology and abstractions.

```text
Simpler control ←――――――――――――――――――――→ More abstraction / power

No framework  →  MCP  →  OpenAI Agents SDK / Crew  →  LangGraph / AutoGen
```

---

## 11. Chat Templates

Chat templates are essential for structuring conversations between language models and users.  
They guide how message exchanges are formatted into a **single prompt**.

### Base Models vs Instruct Models

| Type | Meaning |
|------|---------|
| **Base Model** | Trained on raw text to predict the next token |
| **Instruct Model** | Fine-tuned to follow instructions and engage in conversations |

Example vibe:

- `SmolLM2-135M` → base model  
- `SmolLM2-135M-Instruct` → instruction-tuned variant  

To make a Base Model behave more like an instruct model, we format prompts in a consistent way the model understands.  
That is where **chat templates** come in.

Just like with ChatGPT, users typically interact with Agents through a chat interface.  
So we need to understand how LLMs manage chats (system / user / assistant message roles, templates, special tokens).

---

## 12. Resources

**Resources** are a method to enhance the capabilities of your agents, enabling them to solve problems more effectively.

Alongside **tools**, resources allow you to equip agents with additional **context and information** to improve their expertise.

Essentially, resources involve providing the language model with relevant data related to the question by including it in the prompt.

### Simple example

If you are prompting an LM to answer questions about a company (e.g. an airline customer support agent), you can include ticket-price information in the prompt.

When the LM answers, it can refer to that information.

### More advanced: retrieve only what is needed

Instead of stuffing *all* data into the prompt, smarter methods select only the ticket prices (or docs) relevant to the specific question.

Such retrieval can even use other language models to help choose the best context.

This approach falls under **Retrieval-Augmented Generation (RAG)** — retrieving relevant context to improve generation quality.

| Concept | Plain meaning |
|---------|----------------|
| **Tool** | Let the model **act** (call a function) |
| **Resource / RAG context** | Give the model **extra knowledge** in the prompt |

---

## 13. What are Tools?

Tools are central to enabling language models to perform actions autonomously.

By giving an LM the ability to use tools at its discretion, you provide it with a form of **autonomy**.  
That means the LM can carry out different actions such as querying a database or sending messages to other LLMs.

Tools allow frontier models to connect with **external functions**, providing functionality beyond the model itself.

In this context, tools mean: giving LLMs access to external functions so they can:

- extend knowledge with richer replies  
- carry out advanced actions in your application  
- enhance abilities (for example, a calculator)  

### One crucial idea

A key part of AI Agents is their ability to take actions.  
This happens through **Tools**.

A Tool is a **function given to the LLM**.  
This function should fulfill a clear objective.

A good tool should **complement** the power of an LLM (do what the LLM is weak at: exact math, live data, private DB, etc.).

### A Tool should contain

- a textual **description** of what the function does  
- a **Callable** (something to perform an action)  
- **Arguments** with typings  
- (optional) **Outputs** with typings  

### Critical reminder (same as chapter 5)

LLMs can only receive text inputs and generate text outputs.  
They have **no way to call tools on their own**.

When we talk about providing tools to an Agent, we mean:

1. teaching the LLM about the existence of these tools  
2. instructing it to generate text-based invocations when needed  

Example:

- provide a weather tool  
- ask about weather in Paris  
- LLM recognizes it should use the weather tool  
- instead of fetching weather itself, it generates a tool-call style request (conceptually: `call weather_tool('Paris')`)  
- the **Agent / your code** executes the tool and gets real weather data  

From the user’s perspective, it looks like the LLM used the tool.  
In reality, the Agent handled execution in the background.

### Simple calculator tool example (idea)

Python-style tool:

```python
def calculator(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b
```

Text description for the LLM:

```text
Tool Name: calculator
Description: Multiply two integers.
Arguments: a: int, b: int
Outputs: int
```

That textual description is what we want the LLM to know about the tool:

- descriptive name: `calculator`  
- longer description (docstring): Multiply two integers  
- inputs and types: two ints  
- output type: int  

(In frameworks, a decorator may mark the function as a tool. In your OpenAI lab, you used a JSON schema + `tools=` instead.)

### The tool loop (again)

When the LLM receives a user prompt, it can respond in two ways:

1. directly with a normal text response  
2. by requesting to run a tool with specific inputs before generating a final response  

You:

1. execute the requested tool  
2. provide the output back to the LLM  
3. let the LLM generate a richer response  

In essence:

> LLM: “I need you to call this tool with these inputs.”  
> You: run it and return the result.  
> LLM: continue with better context.

### Practical mechanism (JSON / structured tool calls)

In practice, tool calling involves sending a prompt to an LLM (such as GPT-4) along with available tools (SQL, calculator, device controllers, etc.).

The LM may respond requesting one of those tools.

Key mechanism:

- the prompt / API lists available actions  
- the model responds in a structured way (often JSON / tool_calls) indicating which tool and arguments  
- your code detects this, executes the tool, and sends results back in a follow-up call  

Process summary:

1. Prompt the LM with available tools  
2. LM responds specifying the desired action (structured)  
3. Your code executes the corresponding tool  
4. Results go back to the LM for further processing / final answer  

This is exactly what you practiced in [`5_TOOLS_FUNCTIONS/tool_functions_1.py`](../5_TOOLS_FUNCTIONS/tool_functions_1.py) with FlightAI ticket prices.

---

## How this chapter connects to **Souvik’s** journey

| Earlier | Now |
|---------|-----|
| Call an LLM | LLM is the **brain** of an Agent |
| Gradio chatbot + history | Agent-style conversation loop |
| Tools / function calling (ch.5) | Body of the Agent — actions on the environment |
| Fixed scripts | Workflow patterns + open-ended agent patterns |
| Direct OpenAI API | Also: frameworks (SDK, Crew, LangGraph, AutoGen) + MCP |

---

## One-line takeaways

- **Agent** = brain (LLM) + body (tools/capabilities) working toward a goal in an environment.  
- **Workflows** are structured; **agents** are more open-ended loops.  
- **Tools** let the model request actions; **your code** executes them.  
- **Resources / RAG** give extra knowledge in the prompt; tools let the model act.
