# Hints

Open one hint at a time, and try it before you open the next.

<details>
<summary><strong>Hint 1</strong></summary>

Pick one failing question and run `inspect` on it.
Find the document you expected.
Where does it appear, and where does it stop appearing?

</details>

<details>
<summary><strong>Hint 2</strong></summary>

`inspect --verbose` shows what happened to each document at each step.
If you want more context, `CHANGES.md` and the git history show what changed recently.

</details>

<details>
<summary><strong>Hint 3</strong></summary>

Look at `src/eligibility.py` and `corpus/METADATA.md`. Compare the eligibility condition in the code with the document states defined for customer-visible content. Does the condition allow every kind of document that should be visible to customers?

</details>

Still stuck after all three? The full reference answer is in `solution/SOLUTION.md`.
