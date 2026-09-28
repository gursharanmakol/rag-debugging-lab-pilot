CUSTOMER_VISIBLE = {"active", "published"}


def eligibility_report(searchable_docs):
    ineligible = [
        doc
        for doc in searchable_docs
        if doc.meta["status"] not in CUSTOMER_VISIBLE
    ]
    return (not ineligible, ineligible)
