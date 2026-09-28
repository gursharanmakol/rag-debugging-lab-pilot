# Hints

Open one hint at a time, and try it before you open the next.

<details>
<summary><strong>Hint 1</strong></summary>

What changed around the time the problem started? Read `CHANGES.md`, then look at the history of the code with `git log -p -- src/` (press `q` to leave the log). Compare what the change was meant to exclude with what it actually excludes.

</details>

<details>
<summary><strong>Hint 2</strong></summary>

Run `inspect` on a failing question. The expected document is a top candidate, but it is not in the final results. Run it again with `--verbose`, then read `corpus/METADATA.md`.

</details>

<details>
<summary><strong>Hint 3</strong></summary>

Look at `is_eligible()` in `src/eligibility.py`. Does its idea of "current" match the metadata contract? Which status values should a customer be able to see?

</details>

Still stuck after all three? The full reference answer is in `solution/SOLUTION.md`.
