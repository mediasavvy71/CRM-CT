"""
Chronic Trace CRM
-----------------
A lightweight desktop CRM that stores all data in a single Excel workbook
(ChronicTraceCRM.xlsx) instead of a database, while giving you a real
application UI on top of it.

Run:
    python3 app.py

Phase 1 of this app implements:
    - Dashboard  (key metrics, org breakdown, recent activity)
    - Organizations (search, filter, add/edit/delete, notes, linked contacts)
    - Contacts (search, add/edit/delete, linked organization)

Everything else in the sidebar (Opportunities, Activities, Follow-ups,
Pilot Programs, Partnerships, Grant Tracker, Reports) is scaffolded as a
"coming soon" placeholder so the navigation shell doesn't need to change
as those phases get built.
"""

import os

import customtkinter as ctk
from tkinter import ttk, messagebox

from data_manager import CRMWorkbook, ORG_TYPES

APP_TITLE = "Chronic Trace CRM"
DEFAULT_WORKBOOK_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "ChronicTraceCRM.xlsx"
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

NAV_ITEMS = [
    ("Dashboard", True),
    ("Organizations", True),
    ("Contacts", True),
    ("Sales Opportunities", False),
    ("Activities", False),
    ("Follow Ups", False),
    ("Pilot Programs", False),
    ("Partnerships", False),
    ("Grant Tracker", False),
    ("Reports", False),
    ("Settings", False),
]

PRIMARY = "#1F2A44"
ACCENT = "#3B82F6"
BG = "#F4F6FA"
CARD_BG = "#FFFFFF"
MUTED = "#6B7280"


class App(ctk.CTk):
    def __init__(self, workbook_path: str = DEFAULT_WORKBOOK_PATH):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1200x760")
        self.minsize(1000, 640)
        self.configure(fg_color=BG)

        self.wb = CRMWorkbook(workbook_path)

        self.nav_buttons = {}
        self.current_frame = None

        self._build_sidebar()
        self._build_content_area()
        self.show_screen("Dashboard")

    # ------------------------------------------------------------------ #
    # Shell / navigation
    # ------------------------------------------------------------------ #
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=PRIMARY)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        title = ctk.CTkLabel(
            sidebar, text="Chronic Trace", font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
        )
        title.pack(pady=(24, 0), padx=20, anchor="w")
        subtitle = ctk.CTkLabel(
            sidebar, text="CRM", font=ctk.CTkFont(size=13), text_color="#93A3C4",
        )
        subtitle.pack(pady=(0, 24), padx=20, anchor="w")

        for name, enabled in NAV_ITEMS:
            label = name if enabled else f"{name}"
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                anchor="w",
                fg_color="transparent",
                hover_color="#2C3B5F" if enabled else PRIMARY,
                text_color="white" if enabled else "#5B6B8C",
                font=ctk.CTkFont(size=14),
                corner_radius=6,
                height=36,
                state="normal" if enabled else "disabled",
                command=(lambda n=name: self.show_screen(n)) if enabled else None,
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[name] = btn

        footer = ctk.CTkLabel(
            sidebar, text="Data stored locally in\nChronicTraceCRM.xlsx",
            font=ctk.CTkFont(size=10), text_color="#5B6B8C", justify="left",
        )
        footer.pack(side="bottom", pady=16, padx=20, anchor="w")

    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, fg_color=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def show_screen(self, name: str):
        for n, btn in self.nav_buttons.items():
            if n == name:
                btn.configure(fg_color="#2C3B5F")
            elif btn.cget("state") == "normal":
                btn.configure(fg_color="transparent")

        if self.current_frame is not None:
            self.current_frame.destroy()

        if name == "Dashboard":
            self.current_frame = DashboardScreen(self.content, self.wb, self)
        elif name == "Organizations":
            self.current_frame = OrganizationsScreen(self.content, self.wb, self)
        elif name == "Contacts":
            self.current_frame = ContactsScreen(self.content, self.wb, self)
        else:
            self.current_frame = ComingSoonScreen(self.content, name)

        self.current_frame.pack(fill="both", expand=True)

    def refresh(self):
        """Re-render whatever screen is currently active (after a save)."""
        for n, enabled in NAV_ITEMS:
            if self.current_frame.__class__.__name__.startswith(n.split()[0]):
                self.show_screen(n)
                return


# ---------------------------------------------------------------------- #
# Shared UI helpers
# ---------------------------------------------------------------------- #
def section_header(parent, title, subtitle=None):
    wrap = ctk.CTkFrame(parent, fg_color="transparent")
    wrap.pack(fill="x", padx=28, pady=(24, 8))
    ctk.CTkLabel(wrap, text=title, font=ctk.CTkFont(size=24, weight="bold"),
                 text_color=PRIMARY).pack(anchor="w")
    if subtitle:
        ctk.CTkLabel(wrap, text=subtitle, font=ctk.CTkFont(size=13),
                     text_color=MUTED).pack(anchor="w")
    return wrap


def metric_card(parent, label, value, color=ACCENT):
    card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10)
    ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=28, weight="bold"),
                 text_color=color).pack(anchor="w", padx=18, pady=(16, 0))
    ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=13),
                 text_color=MUTED).pack(anchor="w", padx=18, pady=(0, 16))
    return card


class ComingSoonScreen(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent, fg_color=BG)
        section_header(self, name, "This section hasn't been built yet.")
        ctk.CTkLabel(
            self,
            text=f"{name} is scaffolded in the navigation and will be added in a future phase.",
            font=ctk.CTkFont(size=14), text_color=MUTED,
        ).pack(padx=28, pady=12, anchor="w")


# ---------------------------------------------------------------------- #
# Dashboard
# ---------------------------------------------------------------------- #
class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, wb: CRMWorkbook, app: App):
        super().__init__(parent, fg_color=BG)
        self.wb = wb
        self.app = app

        section_header(self, "Dashboard", "Overview of your organizations and contacts.")

        metrics = self.wb.dashboard_metrics()

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", padx=28, pady=8)
        for i in range(3):
            cards.grid_columnconfigure(i, weight=1, uniform="card")

        metric_card(cards, "Total Organizations", metrics["total_orgs"]).grid(
            row=0, column=0, sticky="nsew", padx=(0, 12), pady=6)
        metric_card(cards, "Total Contacts", metrics["total_contacts"], color="#10B981").grid(
            row=0, column=1, sticky="nsew", padx=12, pady=6)
        metric_card(cards, "Decision Makers", metrics["decision_makers"], color="#F59E0B").grid(
            row=0, column=2, sticky="nsew", padx=(12, 0), pady=6)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=(12, 20))
        body.grid_columnconfigure(0, weight=1, uniform="body")
        body.grid_columnconfigure(1, weight=1, uniform="body")
        body.grid_rowconfigure(0, weight=1)

        # Organizations by type
        by_type_card = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=10)
        by_type_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        ctk.CTkLabel(by_type_card, text="Organizations by Type",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=PRIMARY).pack(anchor="w", padx=16, pady=(14, 8))
        if metrics["orgs_by_type"]:
            for org_type, count in metrics["orgs_by_type"].items():
                row = ctk.CTkFrame(by_type_card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=2)
                ctk.CTkLabel(row, text=org_type, text_color=MUTED,
                             font=ctk.CTkFont(size=13)).pack(side="left")
                ctk.CTkLabel(row, text=str(count), text_color=PRIMARY,
                             font=ctk.CTkFont(size=13, weight="bold")).pack(side="right")
        else:
            ctk.CTkLabel(by_type_card, text="No organizations yet.", text_color=MUTED).pack(
                padx=16, pady=8, anchor="w")
        ctk.CTkFrame(by_type_card, fg_color="transparent", height=12).pack()

        # Recently added
        recent_card = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=10)
        recent_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        ctk.CTkLabel(recent_card, text="Recently Added Organizations",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=PRIMARY).pack(anchor="w", padx=16, pady=(14, 8))
        if metrics["recent_orgs"]:
            for org in metrics["recent_orgs"]:
                row = ctk.CTkFrame(recent_card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=3)
                ctk.CTkLabel(row, text=org["Name"] or "(unnamed)", text_color=PRIMARY,
                             font=ctk.CTkFont(size=13)).pack(side="left")
                ctk.CTkLabel(row, text=org["CreatedDate"], text_color=MUTED,
                             font=ctk.CTkFont(size=11)).pack(side="right")
        else:
            ctk.CTkLabel(recent_card, text="No organizations yet.", text_color=MUTED).pack(
                padx=16, pady=8, anchor="w")
        ctk.CTkFrame(recent_card, fg_color="transparent", height=12).pack()


# ---------------------------------------------------------------------- #
# Organizations
# ---------------------------------------------------------------------- #
class OrganizationsScreen(ctk.CTkFrame):
    DISPLAY_COLUMNS = ["Name", "Type", "City", "State", "Phone", "LastContactDate"]

    def __init__(self, parent, wb: CRMWorkbook, app: App):
        super().__init__(parent, fg_color=BG)
        self.wb = wb
        self.app = app
        self.selected_org_id = None

        section_header(self, "Organizations", "Accounts, prospects, and customers.")

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=(0, 8))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var,
                                     placeholder_text="Search organizations...", width=280)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda e: self._refresh_table())

        self.type_filter = ctk.StringVar(value="All Types")
        type_menu = ctk.CTkOptionMenu(
            toolbar, variable=self.type_filter, values=["All Types"] + ORG_TYPES,
            command=lambda _: self._refresh_table(), width=160,
        )
        type_menu.pack(side="left", padx=8)

        add_btn = ctk.CTkButton(toolbar, text="+ Add Organization", fg_color=ACCENT,
                                 command=self._open_add_dialog)
        add_btn.pack(side="right")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=(4, 20))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        table_card = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=10)
        table_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self._build_table(table_card)

        self.detail_card = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=10)
        self.detail_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        self._render_detail_placeholder()

        self._refresh_table()

    def _build_table(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Org.Treeview", rowheight=28, font=("Helvetica", 11))
        style.configure("Org.Treeview.Heading", font=("Helvetica", 11, "bold"))

        self.tree = ttk.Treeview(
            parent, columns=self.DISPLAY_COLUMNS, show="headings",
            style="Org.Treeview", selectmode="browse",
        )
        for col in self.DISPLAY_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = self.wb.list_organizations()
        query = self.search_var.get().strip().lower()
        type_filter = self.type_filter.get()

        if type_filter != "All Types":
            df = df[df["Type"] == type_filter]
        if query:
            mask = df.apply(lambda r: query in " ".join(str(v).lower() for v in r), axis=1)
            df = df[mask]

        self._row_id_map = {}
        for _, row in df.iterrows():
            values = [row.get(c, "") for c in self.DISPLAY_COLUMNS]
            item = self.tree.insert("", "end", values=values)
            self._row_id_map[item] = row["OrgID"]

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        org_id = self._row_id_map.get(sel[0])
        if org_id:
            self.selected_org_id = org_id
            self._render_detail(org_id)

    def _render_detail_placeholder(self):
        for w in self.detail_card.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.detail_card, text="Select an organization to view details.",
                     text_color=MUTED, font=ctk.CTkFont(size=13)).pack(padx=16, pady=20)

    def _render_detail(self, org_id):
        for w in self.detail_card.winfo_children():
            w.destroy()

        org = self.wb.get_organization(org_id)
        if not org:
            self._render_detail_placeholder()
            return

        header = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 4))
        ctk.CTkLabel(header, text=org["Name"], font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=PRIMARY).pack(side="left")

        btns = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkButton(btns, text="Edit", width=70, fg_color=ACCENT,
                      command=lambda: self._open_edit_dialog(org)).pack(side="left")
        ctk.CTkButton(btns, text="Delete", width=70, fg_color="#DC2626",
                      hover_color="#B91C1C",
                      command=lambda: self._delete_org(org_id)).pack(side="left", padx=8)

        info_lines = [
            ("Type", org["Type"]),
            ("Phone", org["Phone"]),
            ("Website", org["Website"]),
            ("Address", f'{org["Address"]}, {org["City"]}, {org["State"]} {org["Zip"]}'.strip(", ")),
            ("Created", org["CreatedDate"]),
            ("Last Contact", org["LastContactDate"]),
        ]
        for label, value in info_lines:
            row = ctk.CTkFrame(self.detail_card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(row, text=label, text_color=MUTED, font=ctk.CTkFont(size=12),
                         width=90, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value or "-", text_color=PRIMARY, font=ctk.CTkFont(size=12),
                         anchor="w", justify="left", wraplength=220).pack(side="left", fill="x")

        ctk.CTkLabel(self.detail_card, text="Notes", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=PRIMARY).pack(anchor="w", padx=16, pady=(12, 2))
        notes_box = ctk.CTkTextbox(self.detail_card, height=70, fg_color="#F4F6FA")
        notes_box.pack(fill="x", padx=16, pady=(0, 8))
        notes_box.insert("1.0", org["Notes"] or "")
        notes_box.configure(state="disabled")

        ctk.CTkLabel(self.detail_card, text="Contacts", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=PRIMARY).pack(anchor="w", padx=16, pady=(8, 2))
        contacts = self.wb.contacts_for_org(org_id)
        if contacts.empty:
            ctk.CTkLabel(self.detail_card, text="No linked contacts.", text_color=MUTED,
                         font=ctk.CTkFont(size=12)).pack(anchor="w", padx=16, pady=(0, 12))
        else:
            for _, c in contacts.iterrows():
                row = ctk.CTkFrame(self.detail_card, fg_color="transparent")
                row.pack(fill="x", padx=16, pady=2)
                name = f'{c["FirstName"]} {c["LastName"]}'.strip()
                ctk.CTkLabel(row, text=name, text_color=PRIMARY,
                             font=ctk.CTkFont(size=12)).pack(side="left")
                ctk.CTkLabel(row, text=c["Title"] or "", text_color=MUTED,
                             font=ctk.CTkFont(size=11)).pack(side="right")

    def _delete_org(self, org_id):
        if messagebox.askyesno("Delete Organization",
                                "Delete this organization? Linked contacts will be unlinked, not deleted."):
            self.wb.delete_organization(org_id)
            self._refresh_table()
            self._render_detail_placeholder()

    def _open_add_dialog(self):
        OrgFormDialog(self, self.wb, on_save=self._after_save)

    def _open_edit_dialog(self, org):
        OrgFormDialog(self, self.wb, org=org, on_save=self._after_save)

    def _after_save(self, org_id):
        self._refresh_table()
        self.selected_org_id = org_id
        self._render_detail(org_id)


class OrgFormDialog(ctk.CTkToplevel):
    FIELDS = ["Name", "Type", "Industry", "Phone", "Website", "Address", "City", "State", "Zip", "Notes"]

    def __init__(self, parent, wb: CRMWorkbook, org=None, on_save=None):
        super().__init__(parent)
        self.wb = wb
        self.org = org
        self.on_save = on_save
        self.title("Edit Organization" if org else "Add Organization")
        self.geometry("420x560")
        self.grab_set()

        self.vars = {}
        form = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=16, pady=16)

        for field in self.FIELDS:
            ctk.CTkLabel(form, text=field, font=ctk.CTkFont(size=12), text_color=MUTED).pack(
                anchor="w", pady=(8, 2))
            if field == "Type":
                var = ctk.StringVar(value=(org["Type"] if org else ORG_TYPES[0]))
                ctk.CTkOptionMenu(form, variable=var, values=ORG_TYPES).pack(fill="x")
            elif field == "Notes":
                var = None
                self.notes_box = ctk.CTkTextbox(form, height=80)
                self.notes_box.pack(fill="x")
                if org:
                    self.notes_box.insert("1.0", org.get("Notes", ""))
            else:
                var = ctk.StringVar(value=(org.get(field, "") if org else ""))
                ctk.CTkEntry(form, textvariable=var).pack(fill="x")
            if var is not None:
                self.vars[field] = var

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 16))
        ctk.CTkButton(btns, text="Cancel", fg_color="#9CA3AF",
                      command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(btns, text="Save", fg_color=ACCENT,
                      command=self._save).pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _save(self):
        data = {f: v.get() for f, v in self.vars.items()}
        data["Notes"] = self.notes_box.get("1.0", "end").strip()

        if not data.get("Name", "").strip():
            messagebox.showerror("Missing Name", "Organization name is required.")
            return

        if self.org:
            self.wb.update_organization(self.org["OrgID"], data)
            org_id = self.org["OrgID"]
        else:
            org_id = self.wb.add_organization(data)

        if self.on_save:
            self.on_save(org_id)
        self.destroy()


# ---------------------------------------------------------------------- #
# Contacts
# ---------------------------------------------------------------------- #
class ContactsScreen(ctk.CTkFrame):
    DISPLAY_COLUMNS = ["FirstName", "LastName", "OrgName", "Title", "Email", "Phone", "DecisionMaker"]

    def __init__(self, parent, wb: CRMWorkbook, app: App):
        super().__init__(parent, fg_color=BG)
        self.wb = wb
        self.app = app

        section_header(self, "Contacts", "People linked to your organizations.")

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=(0, 8))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var,
                                     placeholder_text="Search contacts...", width=280)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda e: self._refresh_table())

        add_btn = ctk.CTkButton(toolbar, text="+ Add Contact", fg_color=ACCENT,
                                 command=self._open_add_dialog)
        add_btn.pack(side="right")

        table_card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10)
        table_card.pack(fill="both", expand=True, padx=28, pady=(4, 20))
        self._build_table(table_card)
        self._refresh_table()

    def _build_table(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Contacts.Treeview", rowheight=28, font=("Helvetica", 11))
        style.configure("Contacts.Treeview.Heading", font=("Helvetica", 11, "bold"))

        toolbar = ctk.CTkFrame(parent, fg_color="transparent")
        toolbar.pack(fill="x", padx=12, pady=(12, 0))

        self.tree = ttk.Treeview(
            parent, columns=self.DISPLAY_COLUMNS, show="headings",
            style="Contacts.Treeview", selectmode="browse",
        )
        for col in self.DISPLAY_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.tree.bind("<Double-1>", self._on_double_click)

        action_bar = ctk.CTkFrame(parent, fg_color="transparent")
        action_bar.pack(fill="x", padx=12, pady=(0, 12))
        ctk.CTkButton(action_bar, text="Edit Selected", width=110, fg_color=ACCENT,
                      command=self._edit_selected).pack(side="left")
        ctk.CTkButton(action_bar, text="Delete Selected", width=120, fg_color="#DC2626",
                      hover_color="#B91C1C", command=self._delete_selected).pack(side="left", padx=8)

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = self.wb.list_contacts()
        query = self.search_var.get().strip().lower()
        if query:
            mask = df.apply(lambda r: query in " ".join(str(v).lower() for v in r), axis=1)
            df = df[mask]

        self._row_id_map = {}
        for _, row in df.iterrows():
            values = [row.get(c, "") for c in self.DISPLAY_COLUMNS]
            item = self.tree.insert("", "end", values=values)
            self._row_id_map[item] = row["ContactID"]

    def _selected_contact(self):
        sel = self.tree.selection()
        if not sel:
            return None
        contact_id = self._row_id_map.get(sel[0])
        return self.wb.get_contact(contact_id) if contact_id else None

    def _on_double_click(self, event):
        self._edit_selected()

    def _edit_selected(self):
        contact = self._selected_contact()
        if not contact:
            messagebox.showinfo("No selection", "Select a contact first.")
            return
        ContactFormDialog(self, self.wb, contact=contact, on_save=lambda _id: self._refresh_table())

    def _delete_selected(self):
        contact = self._selected_contact()
        if not contact:
            messagebox.showinfo("No selection", "Select a contact first.")
            return
        if messagebox.askyesno("Delete Contact", f'Delete {contact["FirstName"]} {contact["LastName"]}?'):
            self.wb.delete_contact(contact["ContactID"])
            self._refresh_table()

    def _open_add_dialog(self):
        ContactFormDialog(self, self.wb, on_save=lambda _id: self._refresh_table())


class ContactFormDialog(ctk.CTkToplevel):
    FIELDS = ["FirstName", "LastName", "Title", "Email", "Phone", "Notes"]

    def __init__(self, parent, wb: CRMWorkbook, contact=None, on_save=None):
        super().__init__(parent)
        self.wb = wb
        self.contact = contact
        self.on_save = on_save
        self.title("Edit Contact" if contact else "Add Contact")
        self.geometry("420x560")
        self.grab_set()

        orgs_df = self.wb.list_organizations()
        self.org_lookup = {row["Name"]: row["OrgID"] for _, row in orgs_df.iterrows()}
        org_names = ["(None)"] + list(self.org_lookup.keys())

        form = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(form, text="Organization", font=ctk.CTkFont(size=12), text_color=MUTED).pack(
            anchor="w", pady=(8, 2))
        current_org_name = "(None)"
        if contact and contact.get("OrgID"):
            for name, oid in self.org_lookup.items():
                if oid == contact["OrgID"]:
                    current_org_name = name
                    break
        self.org_var = ctk.StringVar(value=current_org_name)
        ctk.CTkOptionMenu(form, variable=self.org_var, values=org_names or ["(None)"]).pack(fill="x")

        self.vars = {}
        for field in self.FIELDS:
            ctk.CTkLabel(form, text=field, font=ctk.CTkFont(size=12), text_color=MUTED).pack(
                anchor="w", pady=(8, 2))
            if field == "Notes":
                self.notes_box = ctk.CTkTextbox(form, height=80)
                self.notes_box.pack(fill="x")
                if contact:
                    self.notes_box.insert("1.0", contact.get("Notes", ""))
            else:
                var = ctk.StringVar(value=(contact.get(field, "") if contact else ""))
                ctk.CTkEntry(form, textvariable=var).pack(fill="x")
                self.vars[field] = var

        ctk.CTkLabel(form, text="Decision Maker?", font=ctk.CTkFont(size=12), text_color=MUTED).pack(
            anchor="w", pady=(8, 2))
        dm_value = str(contact.get("DecisionMaker", "")).lower() in ("y", "yes", "true") if contact else False
        self.dm_var = ctk.BooleanVar(value=dm_value)
        ctk.CTkCheckBox(form, text="Yes, this person is a decision maker", variable=self.dm_var).pack(anchor="w")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 16))
        ctk.CTkButton(btns, text="Cancel", fg_color="#9CA3AF",
                      command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(btns, text="Save", fg_color=ACCENT,
                      command=self._save).pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _save(self):
        data = {f: v.get() for f, v in self.vars.items()}
        data["Notes"] = self.notes_box.get("1.0", "end").strip()
        data["DecisionMaker"] = "Y" if self.dm_var.get() else "N"

        org_name = self.org_var.get()
        data["OrgID"] = self.org_lookup.get(org_name, "")

        if not data.get("FirstName", "").strip() and not data.get("LastName", "").strip():
            messagebox.showerror("Missing Name", "First or last name is required.")
            return

        if self.contact:
            self.wb.update_contact(self.contact["ContactID"], data)
            contact_id = self.contact["ContactID"]
        else:
            contact_id = self.wb.add_contact(data)

        if self.on_save:
            self.on_save(contact_id)
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
