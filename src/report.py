def format_evaluate(found, ok, ineligible, failures, verbose):
    lines = [
        f"Retrieval    {found}/10 questions found the expected source in the top 3",
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
    status_width = max(
        (len(str(doc.meta["status"])) for doc, _score in candidates),
        default=0,
    )
    for rank, (doc, score) in enumerate(candidates, start=1):
        status = str(doc.meta["status"])
        line = (
            f"  {rank}  {doc.id:<{id_width}}  {score:.3f}  "
            f"status={status:<{status_width}}"
        )
        if verbose:
            line += "   " + ("kept" if eligible(doc) else "removed")
        lines.append(line.rstrip())
    lines.append("")
    lines.append("Final results (top 3)")
    for doc, _score in finals:
        lines.append(f"  {doc.id}")
    return "\n".join(lines)


def _eligibility_phrase(count):
    if count == 1:
        return "1 ineligible document is searchable"
    return f"{count} ineligible documents are searchable"
