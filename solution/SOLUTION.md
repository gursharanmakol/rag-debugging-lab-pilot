# Reference Solution

Read this after you've finished the lab, or when the hints aren't enough.

## What you learned

> Retrieval can fail even when the right document is the most relevant one. In this system, an eligibility filter runs after search and removed the right policy before it reached the results. A filter can do the same thing whether it runs before or after search. Better embeddings would not fix this kind of failure, because the problem was never similarity. The fix has to match what the data actually says, which is why the metadata contract matters.

## The pattern to remember

When a RAG system returns the wrong result, don't start by changing the embedding model, the prompt, or the retrieval settings. Follow the expected evidence through the pipeline instead.

1. Reproduce the failure and measure it.
2. Pick one failing case and follow the document that should have come back.
3. Find the first stage where what you observe differs from what you expected.
4. Make the smallest change to that stage.
5. Measure again, and check that you haven't broken another requirement.

In this lab, the expected document for Q01 moved through the stages like this.

```
Expected document: refund-policy-2026
       |
       v
Similarity ranking    FOUND    (rank 1 of 15)
       |
       v
Eligibility           REMOVED
       |
       v
Final results         MISSING
```

The same pattern works on other failures. Only the stage changes. If the document had been missing from the similarity ranking, you would investigate the embeddings or the document text. If it had reached the final results and the answer was still wrong, you would look further downstream.

## What failed, and which output showed it

`evaluate` reported 5 PASS and 5 FAIL. All five failures were policy questions (Q01 to Q05). The five help-page questions passed.

`inspect Q01 --verbose` showed where the document went.

```
Question   How many days do I have to ask for a refund?
Expected   refund-policy-2026

Top candidates by similarity
rank  id                   score  after eligibility
1     refund-policy-2026   0.747  removed
2     refund-policy-2025   0.718  removed
3     returns-policy-2026  0.593  removed
4     billing-faq          0.581  kept
5     returns-policy-2025  0.486  removed

Final results (top 3 after eligibility)
1  billing-faq
2  account-help
3  payment-methods
```

The right document was the closest match of all fifteen. Search found it, and the eligibility step removed it, along with the other 2026 policy near the top. The help page `billing-faq` was kept. The `corpus` command, or the files themselves, show the difference. Both removed 2026 policies are `published`, and the kept help page is `active`.

## The wrong assumption

`CHANGES.md` says customer search "now treats active documents as eligible." The code does exactly that.

```python
return doc.meta.get("status") == "active"
```

`corpus/METADATA.md` tells a different story. The new content system marks current, approved pages as `published`. The value `active` is a legacy value from before the February 2026 migration, and it means the same as `published`. The 2026 policies came through the new system, so they say `published`, and the rule rejected every one of them. The older help pages still say `active`, so they passed. That is why exactly the five policy questions failed.

## The fix

```python
def is_eligible(doc):
    """Return True if a document may appear in customer search results."""
    return doc.meta.get("status") in {"active", "published"}
```

Any version that lets `published` and `active` through and rejects everything else is a full solution.

After the fix, `evaluate` reports this.

```
Summary
Retrieval    10 PASS / 0 FAIL
Eligibility  PASS  0 ineligible documents are searchable
```

**A follow-on idea.** In a larger system it's often better to normalize legacy values when documents are loaded, turning `active` into `published` once. Code downstream then deals with a single value, and `check` could flag any status the contract doesn't define. It isn't required here.

## Why the tempting fixes are wrong

Two other changes also get retrieval to 10/10.

| Change | Retrieval | Ineligible documents searchable | Result |
|---|---|---|---|
| Starting code, `== "active"` | 5/10 | 0 | Retrieval fails |
| Remove the filter | 10/10 | 4 | FAIL |
| `!= "superseded"` | 10/10 | 1 | FAIL |
| `in {"active", "published"}` | 10/10 | 0 | PASS |

Removing the filter brings back the three 2025 policies and the unapproved warranty draft. Excluding only `superseded` still lets the draft through, and the draft proposes a 2-year warranty that TechNova hasn't approved.

This is the second lesson. A retrieval score can say the system is fixed while a separate requirement says it is still unsafe. Don't prove a fix with only the metric you were trying to improve. Also check what your change could break. That is why this lab reports two checks.

## The model was never the problem

With no filter at all, the same embedding model finds every expected document in the top 3 for all ten questions. Retrieving the right documents was never the issue. A bigger or better embedding model would have produced the same 5/10, because the right document was already at the top of the ranking and was removed afterward.

## The regression question

The ticket asks for one question that would have caught this before it shipped. A good one has a single correct source that is a `published` document, so the broken rule can't return it.

The reference question is in `solution/questions_added.yaml`.

```yaml
- id: Q11
  question: "Is there a restocking fee if I open a speaker and send it back?"
  expected: returns-policy-2026
```

Only the 2026 returns policy answers it, with a 10% fee on opened electronics. With the starting code, `evaluate` shows Q11 failing. With the fix it passes, and the report reads 11/11.

Yours doesn't need to match. Any question whose only correct source is a current policy does the job.

## Why editing the evaluation questions hides the problem

Changing an expected answer to whatever the system now returns makes the score go up, but customers would still get the wrong documents. The evaluation questions describe what should happen. When they fail, the system is what needs to change.

## Check your reasoning

1. **Why did the right policy disappear from the results?** Search ranked it first. The eligibility rule then removed it, because the rule accepted only `active` and current policies are marked `published`.
2. **Why would a better embedding model not have fixed this?** The embedding model had already done its job. The document was lost at the eligibility step, after ranking, and no model changes that decision.
3. **What measurement showed your change worked, and what would have shown it was wrong?** Retrieval 10/10 together with Eligibility PASS. A remaining retrieval failure would show the fix was incomplete. An Eligibility FAIL would show it let the wrong documents through, even at 10/10.

## Where to look next time

Suppose the right document had reached the final results, but the assistant's answer was still wrong. Where would you investigate?

<details>
<summary><strong>One way to think about it</strong></summary>

Keep following the evidence. Check what text was actually passed to the model, and whether the fact the customer needed was in it. If it was, the problem is in how the answer was generated. If it wasn't, look at how that context was built. Later labs cover those stages.

</details>
