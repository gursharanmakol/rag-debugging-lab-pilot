def is_eligible(doc):
    """Return True if a document may appear in customer search results."""
    return doc.meta.get("status") == "active"
