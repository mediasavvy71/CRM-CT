# Chronic Trace CRM

A full CRM that runs entirely as one HTML file — no installs, no server,
no database. Double-click `ChronicTraceCRM.html` to open it in your browser
and it just works.

## Open it

Double-click `ChronicTraceCRM.html` (or right-click → Open With → your
browser). Requires an internet connection the first time you open it (it
loads a small Excel-reading library from a CDN); everything else works
offline.

## What's included

Every section from the original plan is now built:

- **Dashboard** — total organizations, contacts, decision makers, total
  pipeline, expected (weighted) revenue, and win rate (Sales pipeline),
  organizations by type, opportunities by pipeline, activities/follow-ups
  due today and overdue, recently added organizations.
- **Organizations** — searchable/filterable table, add/edit/delete, notes,
  detail panel showing linked contacts and opportunities.
- **Contacts** — searchable table, add/edit/delete, linked to an
  organization, decision-maker flag.
- **Pipelines** — HubSpot-style multiple pipelines, each with its own stages:
  Sales (Prospecting → Qualification → Proposal Sent → Negotiation → Closed
  Won/Lost), Research (Idea → Literature Review → Study Design → IRB
  Approval → Data Collection → Published/Discontinued), Partnership
  (Prospecting → Discussions → Agreement Drafting → Active/Ended), Funding
  (Researching → Preparing Application → Applied → Awarded/Declined), and
  Feedback (Collected → Under Review → Actioned → Published/Archived).
  Switch pipelines with tabs at the top; each shows its own Kanban board (with
  a per-card stage dropdown), table view, and forecast summary. Deals from
  every pipeline can still link to an organization, and Activities can link
  to a deal from any of them.
- **Activities** — log of calls, emails, meetings, and demos, linked to an
  organization, contact, and optionally an opportunity.
- **Follow Ups** — grouped into Overdue, Due Today, Upcoming, and Done, with
  a one-click checkbox to mark complete.
- **Pilot Programs** — cards showing status, participant count vs. target
  with a progress bar, start/end dates, and a milestone checklist you can
  add to, check off, or remove.
- **Partnerships** — type (Curriculum/Clinical/Technology/Distribution),
  status, start date, notes, linked to an organization.
- **Grant Tracker** — funder, amount, status, deadline (overdue deadlines
  highlighted in red), optionally linked to an organization.
- **Reports** — pipeline-by-stage (pick any of the 5 pipelines), revenue by
  month (Sales pipeline, closed-won), sales by month (Sales pipeline
  opportunities created), and lead sources (Sales pipeline) — all as simple
  bar charts, no extra dependency. Revenue/Sales-by-month/Lead-Sources are
  scoped to the Sales pipeline since it's the only one where "amount"
  reliably means dollars.
- **Settings** — export everything to a real `.xlsx` backup, import it back
  in, or clear and reset to sample data.

Sample data is preloaded (3 organizations, 3 contacts, 8 opportunities spread
across all 5 pipelines, activities, follow-ups, one pilot program with
milestones, one partnership, one grant) so you can see how everything looks
and connects. Clear it from Settings whenever you're ready for real data.

If you have data saved from an earlier version of this CRM (before
pipelines existed), it loads in fine — every existing opportunity is
automatically treated as a "Sales" pipeline deal, no data is lost.

## Your data

Everything auto-saves to this browser's local storage as you work — closing
and reopening the file keeps your data, as long as you use the same browser
on the same computer. Because it's not written to a file on disk
automatically, get in the habit of using **Settings → Export to Excel**
occasionally, especially before switching computers or browsers. Import
brings a previously exported file straight back in, sheets and all.

## How it's built

Single self-contained file, vanilla HTML/CSS/JS, no build step, no
framework. Everything reads and writes through one `Store` object (mirroring
the shape of a proper backend), which is what makes the whole thing testable
even outside a browser. All the domain logic — CRUD for organizations,
contacts, opportunities, activities, follow-ups, pilots, partnerships,
grants, plus the dashboard metrics and Excel export/import — lives in that
`Store` object and a matching set of `render*()` functions, one per screen.

## A note on the other files in this folder

`app.py`, `data_manager.py`, `requirements.txt`, and `data/ChronicTraceCRM.xlsx`
are an earlier Python/CustomTkinter desktop version that only has Dashboard,
Organizations, and Contacts — it was not updated with this round's new
sections. `ChronicTraceCRM.html` is the current, complete version. Ignore
the Python files unless you specifically want the installable desktop
version instead of the browser one.

## What's next

The CRM itself is feature-complete against the original plan. From here,
reasonable next steps would be things like: recurring/scheduled follow-up
reminders, file attachments on organizations or pilots, a calendar view
instead of grouped lists for follow-ups, or wiring this up to a real backend
if you outgrow browser storage. Let me know if you want any of that.
