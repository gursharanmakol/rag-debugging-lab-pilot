import os
import sys

_RESET = "\033[0m"
_GREEN = "\033[32m"
_RED = "\033[31m"


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _pass_label() -> str:
    return f"{_GREEN}PASS{_RESET}" if _color_enabled() else "PASS"


def _fail_label() -> str:
    return f"{_RED}FAIL{_RESET}" if _color_enabled() else "FAIL"


def format_evaluate(results, ok, ineligible, verbose):
    passed = sum(1 for item in results if item["passed"])
    failed = len(results) - passed
    lines = ["Retrieval evaluation"]
    for item in results:
        label = _pass_label() if item["passed"] else _fail_label()
        lines.append("")
        lines.append(f"{item['id']}  {label}  {item['question']}")
        lines.append(f"     expected  {item['expected']}")
        lines.append(f"     got       {', '.join(item['got'])}")
    lines.append("")
    lines.append("Summary")
    lines.append(f"Retrieval    {passed} {_pass_label()} / {failed} {_fail_label()}")
    outcome = _pass_label() if ok else _fail_label()
    lines.append(f"Eligibility  {outcome}  {_eligibility_phrase(len(ineligible))}")
    if verbose and not ok:
        lines.append("")
        lines.append("Ineligible searchable documents:")
        width = max(len(doc.id) for doc in ineligible)
        for doc in ineligible:
            lines.append(f"  {doc.id:<{width}}   status={doc.meta['status']}")
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
