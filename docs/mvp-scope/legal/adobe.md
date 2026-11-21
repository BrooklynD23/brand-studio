# Adobe terms: clause record (B1)

Status: PARTLY CLOSED. Owner use on the owner's machine is allowed. Shipping to others, AI/ML use, and the new developer tools terms (at adobe.com/go/new-developer-tools-terms) are still open.

Quotes below come from agent extraction of the owner's local PDFs. Verify each against the PDF before relying on it.

## Documents read

| Document | File | Version | Language | Status |
|---|---|---|---|---|
| Adobe Developer Terms | `Downloads/Developer-Terms-en_US-20240618.pdf` | 2024-06-18, 16 pp | English | Read. May be superseded; Adobe's current version not yet confirmed |
| New Developer Tools Terms (addendum) | `Downloads/new-developer-tools-terms-2026v1.pdf` | 2026v1, 1 p (metadata created 2026-03-13) | English | Read. Applies only to Firefly Creative Production customers not on 2026v2 or later |
| PSLT, Creative Cloud, Firefly and Substance 3D APIs | `Downloads/pslt-adobecreativeapi-jp-2026v2.pdf` | 2026v2, 9 pp (EN pp1-4, JP pp5-9) | Bilingual; filename says jp | Read. Worldwide (ww) copy not provided. Section 10 does not exist in this file |
| New developer tools terms (URL) | adobe.com/go/new-developer-tools-terms | unknown | unknown | NOT READ. Referenced by PSLT section 9 |
| General Terms | adobe.com/legal/terms.html | Oct 3 2025 | English | Read earlier by research (web); quotes unverified against PDF |

## Developer Terms (2024) clauses that matter

| Clause | Quote (extracted) | Effect on owner's own use | Effect on shipping to others |
|---|---|---|---|
| 4.1(A) | "...distribute the Developer Tools (or portions thereof) solely in and with your approved Developer Software in object code form only." | Development and testing use allowed | Only inside approved software, object code only |
| 5.1 | "We may restrict distribution of any Developer Software ... not approved by us." | Not triggered | Adobe approval needed; may require re-approval after updates; 10 days to stop distribution on notice |
| 5.2 | "We may require you to distribute approved Developer Software only through Adobe Exchange, Adobe Express Add-on Marketplace, or other channels approved by us." | None | Approved channels only |
| 6.7 | Usage limits, including limits on calls accepted by an API | Applies | Applies to end users too |
| 6.8 | "You may not (A) sublicense the Developer Tools for use by a third party..." | None | Customers cannot receive Adobe SDK rights |
| 6.10 / 6.15 | Own end-user licence agreement and privacy notice required | None | Required |
| 6.11 | No re-identification of natural persons by linking data | Applies | Applies |
| 6.16 | No use of Adobe services, software, or output "derived from" them to create, train, test, or improve AI, or for identifying natural persons | Applies (see conflict 5, option B) | Applies |
| 14.2 / 14.3 | Adobe may terminate at any time; on termination, stop distributing immediately | Adobe can cut access | Stop distribution |
| 2.22 | "Developer Software" includes "add-ons, extensions, plug-ins" | The plugin is Developer Software | Full distribution rules apply |
| 23.1 | Says "Development Software"; likely a typo | - | - |

No explicit clause on bots, scraping, or automated access was found. Closest: 6.1, 6.7, 3.1.

## PSLT 2026v2 clauses that matter

| Clause | Quote (extracted, EN) | Effect |
|---|---|---|
| 1.4 | "Customer Software means any software applications... intended to access, function, or interoperate with the Developer Tools..." | The plugin is Customer Software |
| 2 | Licence "for the sole purpose of developing, testing and building integrations with Customer Software" | Owner use fine; no distribution right here |
| 3 | "Under no circumstances can Customer distribute the Content Files on a stand-alone basis, outside of the Customer Software." | Bundle inside plugin only |
| 5.3 | Beta: "must not... use the Beta Version (and any outputs...) for any public or external use, unless approved by Adobe in writing." | Internal beta OK; external blocked without written approval |
| 6.1 | "Customer Software must add significant functionality or features beyond the capabilities in Developer Tools" | Plugin must add real features |
| 6.2 | AI/ML: no use of "the Developer Tools (or any content, data, output...)" to "create, train, test, or otherwise improve" AI | Same as Developer Terms 6.16 |
| 6.3 | "Customer Software must not be provided to third parties (for example, by offering Customer Software as an external facing product to consumers or clients)." | Shipping to others blocked unless the Sales Order allows it |
| 6.4 | Sample Files not distributable standalone | Fine |
| 6.5 | No representation that Adobe endorsed the software | Marketing must not imply endorsement |
| 6.6(A) | "Adobe recommends against embedding API credentials in mobile environments or other client-side applications..." | Plugin must not embed Adobe API credentials |
| 6.6(C) | Adobe may rate-limit API calls; notify Adobe before user "Spikes" | Plugin batch jobs may be throttled |
| 7.1-7.3 | Firefly output is Customer Content; output may not be unique; indemnity only if in Sales Order, and excludes use after Adobe's stop instruction | No indemnity unless the Sales Order says so |
| 8.2 | Third-party service outputs are excluded from the agreement | Custom nodes not covered |
| 9 | New developer tools are subject to the terms at adobe.com/go/new-developer-tools-terms | That URL is NOT READ |

## New developer tools addendum (2026v1)

- Section 1.1: Section 1 does not apply to customers on 2026v2 or later. Our PSLT copy is 2026v2, so section 1 does not apply to us.
- Section 1.2(B): third-party custom nodes are governed by the customer's own agreement, and their outputs get no Adobe indemnity.

## Open items

1. Read adobe.com/go/new-developer-tools-terms (owner logged in). This is the document that governs new developer tools, which likely includes the plugin.
2. Confirm Adobe's current Developer Terms (the copy read is 2024).
3. Obtain the worldwide PSLT copy (the file read is bilingual Japanese).
4. Check the signed Sales Order for Firefly indemnity and any distribution rights.
5. Decide whether the MVP uses Firefly at all. If not, PSLT items 6.2 and 7.x are dormant.

## Decisions that depend on this file

- Conflict 5 (option B): Adobe-touched assets go to human review only; §6.16 and PSLT §6.2 are the basis.
- Conflict 6: plugin stays out of public repos; §4.1(A) and §5.1 are the basis.
- No Adobe API credentials in the plugin (PSLT §6.6(A)).
