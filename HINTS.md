# Hints

Open one hint at a time, and try it before you open the next.

<details>
<summary><strong>Hint 1</strong></summary>

Start with one failed question, such as Q01. Run `uv run python lab.py inspect Q01 --verbose` and follow the expected document through the search pipeline. Where does it appear, and where does it disappear?

</details>

<details>
<summary><strong>Hint 2</strong></summary>

Now look at what changed around the time the problem started. Read `CHANGES.md`, then inspect the code history with `git log -p -- src/` (press `q` to leave the log). Compare what the change was intended to do with what the code actually does.

</details>

<details>
<summary><strong>Hint 3</strong></summary>

Look at `src/eligibility.py` and `corpus/METADATA.md`. Compare the eligibility condition in the code with the document states defined for customer-visible content. Does the condition allow every kind of document that should be visible to customers?

</details>

Still stuck after all three? The full reference answer is in `solution/SOLUTION.md`.
