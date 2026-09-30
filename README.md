# TechNova RAG Lab: The Missing Policies

## What you'll practice

In this exercise, you'll practice diagnosing a RAG retrieval failure in an existing application. You'll use evaluation results and debugging evidence to find where the failure happens, make a targeted fix, and verify that your change actually solves the problem.

## The system

TechNova's support assistant searches the company's help-center documents before it answers a customer. This repository is a small, working version of that search. It has 15 help-center documents, a set of evaluation questions with known correct answers, and a command-line tool for measuring and inspecting the search.

If you'd like to understand how the search works before you start, open the background sections below the ticket. They take about five minutes to read.

## Your ticket

> **TechNova support search: policy questions stopped working**
>
> TechNova's support assistant searches help-center documents before answering customers. Yesterday the team shipped a change so customer searches use only current policies, not old versions (see `CHANGES.md`).
>
> This morning, support reported that several policy questions no longer find the right document.
>
> Your task:
> 1. Reproduce the problem.
> 2. Use the evaluation output to work out what is happening.
> 3. Make the smallest appropriate code change.
> 4. Rerun the evaluation and show that your change fixed it.
> 5. Add one evaluation question that would have caught this before it shipped.
>
> Do not change the existing evaluation questions or expected answers to make them pass.

## Background (optional)

<details>
<summary><strong>How this system works</strong></summary>

The search has two sides. One side prepares the documents. The other side answers a question.

**Preparing the documents**

Each help-center document is a short Markdown file in `corpus/`. It has two parts.

- The text, which is a title and a body.
- A block of metadata at the top of the file. Metadata is information about the document rather than its content, such as its ID, its type, and its dates.

The documents are short, so each one is kept whole instead of being split into smaller chunks. The title and body are turned into an embedding. The metadata is not part of the embedding. It stays attached to the document so the application can use it later.

**What an embedding is**

A computer can't compare the meaning of two pieces of text directly. An embedding model turns text into a list of numbers, called a vector, so that texts with related meaning end up with similar vectors. The documents and the customer's question go through the same model, so their vectors can be compared.

This approach is called embedding-based semantic search, or dense retrieval. It matches meaning rather than exact words, so a question about "headphones" can find a page that talks about "headsets."

**Answering a question**

```
Customer question
      |
      v
Embed the question with the same model
      |
      v
Compare it with every document's embedding
      |
      v
Rank the documents by similarity
      |
      v
Apply the customer eligibility rule
      |
      v
Return the top 3 results
```

**Why there is an eligibility step**

Similarity answers one question, which documents are related to what the customer asked. It doesn't answer a second question, which documents this customer is allowed to receive. A closely related document might be out of date, not yet approved, or meant only for staff. Production search systems therefore often apply a separate rule that decides which of the ranked documents can be shown. That rule works from information about each document, not from its text.

</details>

<details>
<summary><strong>Why the lab is built this way</strong></summary>

- **A small local embedding model.** The lab uses Model2Vec with the `potion-base-8M` model. It runs on a laptop with no API key, no paid service, no PyTorch, and no network connection during normal use. The model files are included in the repository.
- **Questions are embedded when you run a command.** Nothing is precomputed or hard-coded, so any question you add is actually searched.
- **Normalized vectors and a dot product.** Every vector is scaled to length 1, so the dot product between two vectors is equivalent to cosine similarity. It is simple, and it gives the same scores on every run.
- **No chunking.** The documents are small. Splitting them would add another way for search to go wrong, and that isn't what this lab is about.
- **No vector database and no framework.** Fifteen documents fit in memory. A database, or a framework such as LangChain or LlamaIndex, would hide the steps you need to see.
- **Two evaluation checks.** Retrieval asks whether each question's expected document appears in the top 3 results. Eligibility asks whether any document that should not be customer-visible can be returned by search.
- **Top 3.** This is the cutoff for this lab's evaluation, not a rule for every RAG system.

</details>

<details>
<summary><strong>What the commands show</strong></summary>

- `check` confirms that Python, the documents, the evaluation questions, and the embedding model are all ready. Run it first.
- `evaluate` runs every evaluation question through the customer search and reports both checks. It lists every question as PASS or FAIL, with the documents that came back. `--verbose` adds detail when the eligibility check fails.
- `inspect Q01` looks at one question in detail. It shows the documents ranked by similarity and, separately, the final results a customer would receive. `--verbose` adds the eligibility decision for each ranked document.
- `corpus` lists every document with a few of its metadata fields.
- `search "your question"` runs any question you type through the customer search.

</details>

## Setup

### What you'll need

- **Git** to clone the lab repository.
- **uv** to run the lab. It installs the required Python version for you.
- **A terminal** to run the lab commands. On Windows, PowerShell is fine. On macOS, use Terminal. You can also use the terminal built into VS Code or another editor.
- **Any code editor** you like to read and change the code.

### How you'll work

Run the lab commands in the terminal to reproduce the problem and investigate what is happening. Open the project in your code editor, make the code change you think is needed, then run the commands again to verify your fix.

You won't need a debugger.

### 1. Check your setup

```bash
git --version
uv --version
```

If both commands print a version, continue to step 2. If either command is not found, open the install steps below. You do not need to install Python yourself. uv installs Python 3.12 the first time you run the lab.

<details>
<summary>Need to install Git or uv?</summary>

Git: https://git-scm.com/downloads

uv for Windows PowerShell:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

uv for macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal after installing uv. Then run the version checks again.

</details>

### 2. Get the lab and check it

```bash
git clone https://github.com/gursharanmakol/rag-debugging-lab-pilot.git
cd rag-debugging-lab-pilot
uv run python lab.py check
```

The first run may take a few minutes while uv prepares Python and the dependencies. You're ready when the last line starts with `Ready.`

If `check` still does not pass after about 15 minutes, stop trying to fix setup. Copy the full terminal output and paste it into the study form. That still counts as a completed session.

### 3. Evaluate, then inspect

```bash
uv run python lab.py evaluate
uv run python lab.py inspect Q01
```

`evaluate` shows which evaluation questions fail. `inspect` shows what happened for one question. The full command list is in the next section.

## Commands

```
uv run python lab.py check
uv run python lab.py evaluate
uv run python lab.py evaluate --verbose
uv run python lab.py inspect Q01
uv run python lab.py inspect Q01 --verbose
uv run python lab.py corpus
uv run python lab.py search "Can I pay with PayPal?"
```

## If you get stuck

Open `HINTS.md` and read one hint at a time. Each hint narrows the search a little more.

`solution/SOLUTION.md` has the full reference answer and explains what the lab teaches. Open it when you've finished, or when the hints aren't enough.

## After you finish

<details>
<summary><strong>Reflection questions</strong></summary>

1. Why did the right policy disappear from the results?
2. Why would a better embedding model not have fixed this?
3. What measurement showed your change worked, and what would have shown it was wrong?

Compare your answers with "Check your reasoning" in `solution/SOLUTION.md`.

</details>
