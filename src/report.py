def format_evaluate(found, total, ok, ineligible, failures, verbose):
    lines = [
        f"Retrieval    {found}/{total} questions found the expected source in the top 3",
        f"Eligibility  {'PASS' if ok else 'FAIL'}  {_eligibility_phrase(len(ineligible))}",
    ]
    if verbose and not ok:
        lines.append("")
        lines.append("Ineligible searchable documents:")
        width = max(len(doc.id) for doc in ineligible)
        for doc in ineligible:
            lines.append(f"  {doc.id:<{width}}   status={doc.meta['status']}")
    if failures:
        lines.append("")
        lines.append("Retrieval failures")
        for item in failures:
            lines.append(f"  {item['id']}  {item['question']}")
            lines.append(f"       expected  {item['expected']}")
            lines.append(f"       got       {', '.join(item['got'])}")
    return "\n".join(lines)


def format_inspect(question, expected, candidates, finals, verbose, eligible):
    lines = [
        f"Question   {question}",
        f"Expected   {expected}",
        "",
        "Top candidates by similarity",
    ]
    id_width = max((len(doc.id) for doc, _score in candidates), default=0)
    if verbose:
        lines.append(f"rank  {'id':<{id_width}}  score  after eligibility")
        for rank, (doc, score) in enumerate(candidates, start=1):
            decision = "kept" if eligible(doc) else "removed"
            lines.append(
                f"{rank:<4}  {doc.id:<{id_width}}  {score:<5.3f}  {decision}"
            )
    else:
        for rank, (doc, score) in enumerate(candidates, start=1):
            lines.append(f"  {rank}  {doc.id:<{id_width}}  {score:.3f}")
    lines.append("")
    lines.append("Final results (top 3 after eligibility)")
    for rank, (doc, _score) in enumerate(finals, start=1):
        lines.append(f"{rank}  {doc.id}")
    return "\n".join(lines)


def _eligibility_phrase(count):
    if count == 1:
        return "1 ineligible document is searchable"
    return f"{count} ineligible documents are searchable"
