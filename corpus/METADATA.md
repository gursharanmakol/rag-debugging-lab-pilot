# Help Center Metadata

Every document in this folder starts with a front matter block. Search and
the support assistant use these fields.

## Fields

| Field | Required | Meaning |
|---|---|---|
| id | yes | Unique document ID. Never reused. |
| title | yes | Page title shown to customers. |
| type | yes | `policy` or `help`. |
| status | yes | Publication state. See below. |
| effective_date | policies only | Date the policy takes effect (YYYY-MM-DD). |
| updated | yes | Date the page was last edited (YYYY-MM-DD). |

## Status values

| Value | Meaning | Customer visible |
|---|---|---|
| draft | Written but not approved. | No |
| published | Approved and current. | Yes |
| superseded | Replaced by a newer version. Kept for records. | No |

## Legacy values

Pages created before the move to the new content system (February 2026)
were not re-saved during the migration. Their status field still uses the
old value `active`, which means the same as `published`. These pages are
scheduled to be re-saved in the new system, but no date has been set.
