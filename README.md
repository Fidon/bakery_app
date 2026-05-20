# Tumaini Bakery Management System

> **Developer:** Fidon Amos Takakwa — Dar es Salaam, Tanzania  
> **Contact:** fidonamos@gmail.com | WhatsApp: +255 713 529 019  
> **Client:** Tumaini Bakery, Dodoma, Tanzania | +255 625 511 541  
> **Project Start:** April 2026  
> **Stack:** Django · PostgreSQL · Bootstrap 5 · jQuery · DataTables  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Repository & Folder Structure](#3-repository--folder-structure)
4. [Environment Setup](#4-environment-setup)
5. [Database Schema](#5-database-schema)
6. [Application Architecture](#6-application-architecture)
7. [Authentication & Security](#7-authentication--security)
8. [Role-Based Access Control](#8-role-based-access-control)
9. [Module Breakdown](#9-module-breakdown)
10. [UI Architecture & Conventions](#10-ui-architecture--conventions)
11. [JavaScript Conventions](#11-javascript-conventions)
12. [Deployment — PythonAnywhere (Free Tier)](#13-deployment--pythonanywhere-free-tier)
13. [Build Progress — Phase Tracker](#14-build-progress--phase-tracker)
14. [Phase 4 — What to Build Next](#15-phase-4--what-to-build-next)
15. [Known Gotchas & Hard-Won Lessons](#16-known-gotchas--hard-won-lessons)

---

## 1. Project Overview

A role-based web application that digitalizes daily operations for a bakery business — replacing manual registers with a real-time, multi-user platform.

**Three departments, each with tailored access:**

| Role | Primary Capability |
|---|---|
| **Admin** | Full system control — users, inventory, reports, waste approvals |
| **Production** | Log daily snack production, view own history |
| **Sales** | Process sales transactions (POS-style), view own history |

**Five core modules:**
1. **Inventory** — Snack item master list with real-time stock tracking
2. **Production** — Daily batch production logging per item
3. **Sales** — POS-style cart checkout with transaction history
4. **Waste Management** — Two-step report → approve workflow (Phase 4)
5. **Reports & Analytics** — Filterable, printable, exportable reports (Phase 4)

---

## 2. Tech Stack

| Layer | Technology | Version/Notes |
|---|---|---|
| Backend | Python / Django | Latest stable |
| Database | PostgreSQL (prod) / SQLite (free-tier) | `bakery_db` |
| Frontend CSS | Bootstrap 5 | 5.3.3 via CDN |
| Frontend Icons | Bootstrap Icons | 1.11.3 via CDN |
| Frontend JS | jQuery | 3.7.1 via CDN |
| Tables | DataTables + Buttons | 2.0.8 + 3.0.2 via CDN |
| Searchable Selects | Tom Select | 2.3.1 via CDN |
| Static Files | Whitenoise | Configured for production |
| Config | python-decouple | `.env` file based |
| Number Formatting | django.contrib.humanize | `intcomma` template filter |
| Deployment | PythonAnywhere (free tier) | SQLite on free tier |

---

## 3. Repository & Folder Structure

**GitHub:** `github.com/Fidon/bakery_app`

```
bakery_project/                     ← root
├── venv/                           ← virtual environment (not committed)
└── bakery_app/                     ← Django project root (manage.py lives here)
    ├── manage.py
    ├── .env                        ← secrets (not committed)
    ├── bakery_db.sqlite3           ← SQLite DB (free-tier deployment only)
    ├── requirements.txt
    │
    ├── bakery_app/                 ← main Django config folder
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── static/                     ← source static files
    │   ├── css/
    │   │   ├── base.css            ← global palette, layout, components
    │   │   ├── accounts/
    │   │   │   ├── login.css
    │   │   │   ├── user_list.css
    │   │   │   ├── profile.css
    │   │   │   └── dashboard.css
    │   │   ├── inventory/
    │   │   │   └── item_list.css
    │   │   ├── production/
    │   │   │   ├── log.css
    │   │   │   └── history.css
    │   │   └── sales/
    │   │       ├── new.css
    │   │       ├── history.css
    │   │       └── detail.css
    │   │
    │   └── js/
    │       ├── base.js             ← sidebar toggle, showToast(), showFormError()
    │       ├── accounts/
    │       │   ├── login.js
    │       │   ├── user_list.js
    │       │   ├── profile.js
    │       │   └── dashboard.js
    │       ├── inventory/
    │       │   └── item_list.js
    │       ├── production/
    │       │   ├── log.js
    │       │   └── history.js
    │       └── sales/
    │           ├── new.js
    │           ├── history.js
    │           └── detail.js
    │
    ├── staticfiles/                ← collectstatic output (not committed)
    │
    ├── templates/
    │   ├── base.html               ← master layout
    │   ├── accounts/
    │   │   ├── login.html
    │   │   ├── dashboard.html      ← role-aware dashboard (3 in 1)
    │   │   ├── set_new_password.html
    │   │   ├── profile.html
    │   │   └── user_list.html
    │   ├── inventory/
    │   │   └── item_list.html
    │   ├── production/
    │   │   ├── log.html
    │   │   └── history.html
    │   └── sales/
    │       ├── new.html
    │       ├── history.html
    │       └── detail.html
    │
    └── apps/                       ← all Django apps live here
        ├── __init__.py
        ├── base_model.py           ← UUIDModel abstract base
        ├── accounts/               ← auth, users, dashboard
        ├── inventory/              ← snack items + stock
        ├── production/             ← production logs
        ├── sales/                  ← transactions + items
        ├── waste/                  ← waste reports (Phase 4)
        └── reports/                ← analytics views (Phase 4)
```

> **Rule:** Every Django app's `name` field in `apps.py` follows the pattern `apps.<appname>` — e.g., `apps.accounts`, `apps.inventory`. This is because apps live inside the `apps/` subdirectory.

---

## 4. Environment Setup

### Local Development

```bash
# Clone
git clone https://github.com/Fidon/bakery_app.git
cd bakery_app

# Virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment file — create bakery_app/.env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=bakery_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Run migrations
cd bakery_app
python manage.py migrate

# Create superuser (admin role)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Key settings.py Configuration

```python
# INSTALLED_APPS (order matters)
'django.contrib.humanize',
'apps.accounts',
'apps.inventory',
'apps.production',
'apps.sales',
'apps.waste',
'apps.reports',

# Auth
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Timezone
TIME_ZONE = 'Africa/Dar_es_Salaam'

# Static files (Whitenoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Context processor — injects pending_waste_count into ALL templates
'apps.accounts.context_processors.bakery_context'
```

### Middleware Order (critical — do not reorder)

```python
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',       # must be 2nd
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'apps.accounts.middleware.ForcePasswordChangeMiddleware',  # custom — forces pw change
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
```

---

## 5. Database Schema

### `accounts_customuser` (extends AbstractUser)

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | auto-generated |
| `full_name` | VARCHAR(150) | replaces first_name/last_name |
| `username` | VARCHAR | unique, always stored lowercase |
| `phone` | VARCHAR(20) | optional |
| `role` | VARCHAR | choices: `admin`, `production`, `sales` |
| `is_active` | BOOLEAN | Django built-in — used for activate/deactivate |
| `is_deleted` | BOOLEAN | soft delete flag |
| `must_change_password` | BOOLEAN | forces password change on first login |
| `created_at` | DATETIME | auto |
| `updated_at` | DATETIME | auto |

> `first_name` and `last_name` from AbstractUser are set to `None` — not used. `full_name` replaces them.

### `inventory_snackitem`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `name` | VARCHAR | unique |
| `unit` | VARCHAR | choices: piece, dozen, kg, g, tray, pack |
| `price` | DECIMAL(10,2) | selling price in TZS |
| `current_stock` | POSITIVE INT | live stock count — updated atomically |
| `description` | TEXT | optional |
| `is_active` | BOOLEAN | |
| `created_by` | FK → CustomUser | |
| `created_at` | DATETIME | |
| `updated_at` | DATETIME | |

### `production_productionlog`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `snack_item` | FK → SnackItem | PROTECT (cannot delete item with logs) |
| `quantity` | POSITIVE INT | |
| `production_date` | DATE | |
| `notes` | TEXT | optional |
| `logged_by` | FK → CustomUser | |
| `created_at` | DATETIME | |
| `updated_at` | DATETIME | |

### `sales_saletransaction`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `transaction_ref` | VARCHAR | unique, format: `TXN-YYYYMMDD-XXXXX` |
| `sale_date` | DATE | |
| `total_amount` | DECIMAL(12,2) | auto-recalculated via `recalculate_total()` |
| `status` | VARCHAR | choices: `completed`, `cancelled` |
| `notes` | TEXT | optional |
| `sold_by` | FK → CustomUser | |
| `created_at` | DATETIME | |
| `updated_at` | DATETIME | |

### `sales_saletransactionitem`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `transaction` | FK → SaleTransaction (CASCADE) | related_name=`items` |
| `snack_item` | FK → SnackItem | PROTECT |
| `quantity` | POSITIVE INT | |
| `unit_price` | DECIMAL(10,2) | price at time of sale |
| `subtotal` | DECIMAL(12,2) | auto-calculated on model `.save()` — `qty × unit_price` |

> **Critical:** Never pass `subtotal` explicitly in `.create()` calls — the model's `save()` method calculates it automatically.

### `waste_wastereport`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `snack_item` | FK → SnackItem | PROTECT |
| `quantity` | POSITIVE INT | |
| `reason` | TEXT | |
| `waste_date` | DATE | |
| `status` | VARCHAR | choices: `pending`, `approved`, `rejected` |
| `reported_by` | FK → CustomUser | |
| `reviewed_by` | FK → CustomUser | nullable |
| `reviewed_at` | DATETIME | nullable |
| `admin_notes` | TEXT | optional, admin's comment on review |
| `created_at` | DATETIME | |
| `updated_at` | DATETIME | |

### Stock Movement Rules (Critical)

All stock changes use `SnackItem.objects.filter(pk=...).update(current_stock=F('current_stock') + N)` inside `transaction.atomic()` — **never `.save()`** (race condition risk).

| Event | Stock Effect |
|---|---|
| Production log saved | `current_stock += quantity` |
| Sale transaction completed | `current_stock -= quantity` |
| Sale transaction cancelled (admin) | `current_stock += quantity` (restored) |
| Production log deleted (admin) | `current_stock -= quantity` (reversed) |
| Waste report approved (Phase 4) | `current_stock -= quantity` |

---

## 6. Application Architecture

### URL Namespaces

| Namespace | Base URL | App |
|---|---|---|
| `accounts` | `/` | Dashboard, auth, users, profile |
| `inventory` | `/inventory/` | Snack items |
| `production` | `/production/` | Production logs |
| `sales` | `/sales/` | Sale transactions |
| `waste` | `/waste/` | Waste reports |
| `reports` | `/reports/` | Analytics |

### Complete URL Map

**accounts:**
```
/                            → dashboard
/login/                      → login_view
/logout/                     → logout_view
/set-new-password/           → set_new_password
/profile/                    → profile
/profile/edit/               → profile_edit
/change-password/            → change_password
/users/                      → user_list
/users/add/                  → user_add
/users/<uuid>/edit/          → user_edit
/users/<uuid>/toggle-active/ → user_toggle_active
/users/<uuid>/reset-password/→ user_reset_password
/users/<uuid>/delete/        → user_delete
```

**inventory:**
```
/inventory/                        → item_list
/inventory/add/                    → item_add
/inventory/<uuid>/edit/            → item_edit
/inventory/<uuid>/toggle-active/   → item_toggle_active
/inventory/<uuid>/delete/          → item_delete
```

**production:**
```
/production/log/               → log (GET: render page | POST: JSON batch save)
/production/history/           → history
/production/<uuid>/delete/     → delete (admin only — reverses stock)
```

**sales:**
```
/sales/                        → history
/sales/new/                    → new (GET: render page | POST: JSON cart checkout)
/sales/<uuid>/detail/          → detail
/sales/<uuid>/cancel/          → cancel (admin only — restores stock)
/sales/item/<uuid>/price/      → get_item_price (Ajax endpoint)
```

**waste (Phase 4 — stub views exist, not yet implemented):**
```
/waste/report/         → report_view
/waste/history/        → history_view
/waste/pending/        → pending_view (admin only)
/waste/<uuid>/review/  → review_view (admin only)
```

**reports (Phase 4 — stub views exist, not yet implemented):**
```
/reports/              → home
/reports/production/   → production_report
/reports/sales/        → sales_report
/reports/waste/        → waste_report
/reports/summary/      → summary_report (admin only)
```

### Permission Mixins (`apps/accounts/mixins.py`)

| Mixin / Decorator | Who Can Access |
|---|---|
| `AdminRequiredMixin` / `@admin_required` | admin only |
| `ProductionRequiredMixin` / `@production_required` | admin + production |
| `SalesRequiredMixin` / `@sales_required` | admin + sales |

All redirect to dashboard with error toast if unauthorized.

---

## 7. Authentication & Security

### Login Flow
- Username + password only (no email login)
- Username stored and compared as lowercase
- Ajax POST returning JSON — no page reload on error

### First Login / Password Reset Flow
1. Admin creates user → default password = `USERNAME_IN_CAPS` (e.g., username `john` → password `JOHN`)
2. `must_change_password = True` is set on the user record
3. On next login, server detects this flag → returns redirect to `/set-new-password/`
4. `ForcePasswordChangeMiddleware` blocks ALL URLs except `/set-new-password/` and `/logout/` until completed
5. After user sets new password → `must_change_password = False`

**Admin password reset** resets back to `username.upper()` and sets `must_change_password = True` again.

### Context Processor (`apps/accounts/context_processors.py`)
`bakery_context` is registered globally and injects `pending_waste_count` (count of `WasteReport` objects with `status='pending'`) into every template — powers the sidebar badge and topbar notification bell for admins.

---

## 8. Role-Based Access Control

| Module / Action | Admin | Production | Sales |
|---|---|---|---|
| Inventory — view list | ✓ | ✓ | ✓ |
| Inventory — add item | ✓ | ✓ | — |
| Inventory — edit / delete / toggle | ✓ | — | — |
| Production — log batch | ✓ | ✓ | — |
| Production — view history | ✓ (all users) | ✓ (own only) | — |
| Production — delete log | ✓ | — | — |
| Sales — new transaction | ✓ | — | ✓ |
| Sales — view history | ✓ (all users) | — | ✓ (own only) |
| Sales — view detail | ✓ (all) | — | ✓ (own only) |
| Sales — cancel transaction | ✓ | — | — |
| Waste — report | ✓ | ✓ | ✓ |
| Waste — view history | ✓ | ✓ | ✓ |
| Waste — pending approvals | ✓ | — | — |
| Reports — production | ✓ | ✓ | — |
| Reports — sales | ✓ | — | ✓ |
| Reports — waste | ✓ | ✓ | ✓ |
| Reports — summary | ✓ | — | — |
| User management | ✓ | — | — |

---

## 9. Module Breakdown

### Module A — Inventory (`apps/inventory`)
- **Admin:** Full CRUD — add, edit, delete, toggle active/inactive
- **Production:** Add only
- **Sales:** View only (read-only table)
- Stock column shows color-coded pill: green (ok, ≥10), amber (low, <10), red (out, 0)
- Delete is blocked by Django's PROTECT FK if the item has any production/sales records — deactivation is the alternative

### Module B — Production Logging (`apps/production`)
**UX Pattern (batch/cart):**
1. Select item from Tom Select searchable dropdown
2. Enter quantity (Enter key triggers add)
3. Client-side duplicate check before adding to batch
4. Submit entire batch as JSON payload in a single POST
5. Server validates all rows, saves atomically, increments stock

**JSON payload:**
```json
{
  "production_date": "2026-04-11",
  "rows": [
    { "snack_item": "uuid-here", "quantity": 48, "notes": "Morning batch" }
  ]
}
```
- Admin can view all users' logs; Production users see their own only
- Admin can delete individual log entries (stock is reversed atomically)

### Module C — Sales (`apps/sales`)
**UX Pattern (POS cart):**
1. Select item → quantity → Add to cart
2. Client-side stock validation (prevents over-selling before hitting server)
3. Running total updates in real-time
4. Checkout sends JSON payload; server validates stock again server-side
5. On success: redirect to transaction detail page (server returns `redirect_url`)
6. Transaction items snapshot `unit_price` at time of sale — historical accuracy preserved even if item price changes later

**JSON payload:**
```json
{
  "sale_date": "2026-04-11",
  "notes": "",
  "rows": [{ "snack_item": "uuid-here", "quantity": 10 }]
}
```
- Admin can cancel completed transactions (stock restored atomically)
- `transaction_ref` format: `TXN-YYYYMMDD-XXXXX` (e.g., `TXN-20260411-00001`)

### Module D — Dashboards (`apps/accounts` → `dashboard.html`)
Single template handles all three roles with `{% if request.user.role == '...' %}` branching.

**Admin context variables:**
- `production_today` — total units produced today (all staff)
- `sales_amount_today` — total sales amount today (TZS)
- `sales_count_today` — number of completed transactions today
- `pending_waste` — count of pending waste reports
- `active_items` — count of active snack items
- `recent_sales` — last 5 SaleTransaction objects
- `recent_production` — last 5 ProductionLog objects

**Production context variables:**
- `my_today_logs` — today's ProductionLog queryset for this user
- `my_today_total` — sum of quantities logged today by this user
- `month_total` — sum of quantities this month by this user
- `active_items` — all active SnackItem objects

**Sales context variables:**
- `my_sales_amount_today` — today's sales total (TZS) by this user
- `my_sales_count_today` — today's transaction count by this user
- `month_total` — this month's sales total (TZS) by this user
- `top_item` — dict with `snack_item__name` and `total_qty` (most sold this month)
- `recent_sales` — last 5 SaleTransaction objects by this user
- `available_items` — count of active items with stock > 0

---

## 10. UI Architecture & Conventions

### Color Palette (CSS variables in `base.css`)

```css
--clr-gold:        #F3CF7A    /* highlights, active states */
--clr-amber:       #BE6A15    /* primary action color */
--clr-rust:        #AC3F21    /* danger/hover states */
--clr-brown:       #6E3B3B    /* headings, text */
--clr-brown-dark:  #4a2828    /* sidebar background */
--clr-amber-light: #fdf3e3    /* table headers, offcanvas headers */
--clr-amber-pale:  #fef9f0    /* table row hover */
```

### Layout
- Fixed sidebar: 260px wide (`--clr-sidebar-w`)
- Fixed topbar: 60px tall (`--clr-topbar-h`)
- Main content: `margin-left: 260px; margin-top: 60px`
- On mobile (< 992px): sidebar slides off-screen, toggle button appears
- Footer: matches sidebar offset on desktop, full-width on mobile

### CDN Load Order in `base.html`

**In `<head>`:**
```
Bootstrap 5 CSS → Bootstrap Icons → Tom Select CSS → base.css → {% block extra_css %}
```
> Tom Select JS loads in `<head>` (before jQuery — it's vanilla JS)

**Before `</body>`:**
```
jQuery → Bootstrap 5 JS → base.js → {% block extra_js %}
```
> DataTables CDN scripts load per-page inside `{% block extra_js %}`, never in base.html

### Files Per Page Rule
Every page has **exactly three files** — no exceptions:
```
templates/[app]/[page].html
static/css/[app]/[page].css
static/js/[app]/[page].js
```

### Form Convention — Bootstrap Floating Labels with Icon Prefix
```html
<div class="input-group">
  <span class="input-group-text"><i class="bi bi-person"></i></span>
  <div class="form-floating flex-fill">
    <input type="text" id="field-id" name="field_name"
           class="form-control" placeholder="Label" required />
    <label for="field-id">Label</label>
  </div>
</div>
```

### Add/Edit → Bootstrap Offcanvas (slides from right, 420px wide)
### Confirmations (delete, reset) → Bootstrap Modal (centered, small)
### Tables → DataTables with copy/excel/pdf/print buttons

### Standard DataTables Config
```javascript
$('#table-id').DataTable({
  responsive: true,
  pageLength: 25,
  columnDefs: [{ orderable: false, targets: -1 }],
  dom:
    '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3"Bf>' +
    '<"table-responsive"t>' +
    '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mt-3"lip>',
  buttons: [
    { extend: 'copy',  className: 'btn btn-sm btn-outline-button1 me-1', text: '<i class="bi bi-clipboard"></i> Copy' },
    { extend: 'excel', className: 'btn btn-sm btn-outline-button2 me-1', text: '<i class="bi bi-file-earmark-excel"></i> Excel' },
    { extend: 'pdf',   className: 'btn btn-sm btn-outline-button3 me-1', text: '<i class="bi bi-file-earmark-pdf"></i> PDF' },
    { extend: 'print', className: 'btn btn-sm btn-outline-bakery',       text: '<i class="bi bi-printer"></i> Print' },
  ],
});
```

### Number Formatting
- Templates: `{{ value|floatformat:0|intcomma }}` (requires `{% load humanize %}`)
- JavaScript: `number.toLocaleString('en-US')`

### Status Badges
```html
<span class="status-badge active">Active</span>       <!-- green -->
<span class="status-badge blocked">Inactive</span>    <!-- red -->
<span class="status-badge completed">Completed</span> <!-- blue -->
<span class="status-badge cancelled">Cancelled</span> <!-- grey -->
<span class="status-badge pending">Pending</span>     <!-- amber -->
<span class="status-badge approved">Approved</span>   <!-- green -->
<span class="status-badge rejected">Rejected</span>   <!-- red -->
```

---

## 11. JavaScript Conventions

### URLs — Never Hardcoded in JS

```html
<!-- Static URL (no pk) → on form tag -->
<form id="form-add-item" data-url="{% url 'inventory:item_add' %}">

<!-- Dynamic URL (needs pk) → on the row button -->
<button data-url="{% url 'inventory:item_edit' item.pk %}">
```

In JS: `const url = $('#form-id').data('url');` or `$('#form-edit').data('url', $(this).data('url'));`

### CSRF Token — Ajax POST without a Form
```html
<!-- Add this immediately after {% block content %} on pages with no form -->
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}" />
```
JS reads it: `$('[name=csrfmiddlewaretoken]').val()`

### JSON POST Pattern (Production Log, New Sale)
```javascript
$.ajax({
  url: url,
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(payload),
  headers: { 'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val() },
});
```

### Standard Form POST Pattern
```javascript
$.ajax({
  url: url,
  method: 'POST',
  data: $form.serialize(), // includes csrfmiddlewaretoken automatically
});
```

### JsonResponse Conventions (backend)
```python
# Success
return JsonResponse({'success': True, 'message': 'Done.'})

# Form validation errors
return JsonResponse({'success': False, 'errors': form.errors})  # dict, plural key

# Single error
return JsonResponse({'success': False, 'error': 'Something went wrong.'})  # string, singular key
```

### Global Helpers (`base.js`)
```javascript
// Toast notifications
showToast('success', 'User created.');
showToast('error', 'Something went wrong.');
showToast('warning', 'Low stock detected.');
showToast('info', 'Note: ...');

// Form error display
showFormError('#form-id-error', 'Error message here.');
hideFormError('#form-id-error');
```

### Form Error HTML (required on every form)
```html
<div id="FORM-ID-error" class="error-alert mb-3" style="display:none;">
  <i class="bi bi-exclamation-circle-fill"></i><span></span>
</div>
```

### Tom Select — Searchable Selects
```javascript
// makeSearchable() is a global utility defined in base.js
// Returns an object keyed by element id
const selects = makeSearchable('#item-select', { placeholder: 'Search items...' });
const itemSelect = selects['item-select'];

// To visually reset after use:
itemSelect.clear();  // must use stored instance — DOM property lookup is unreliable
```

---

## 12. Deployment — PythonAnywhere (Free Tier)

- **DB:** SQLite (`bakery_db.sqlite3`) — PostgreSQL config preserved in settings.py but commented out
- **Static files:** Served by Whitenoise via `collectstatic`
- **`DEBUG = False`** in production via `.env`
- Run `python manage.py collectstatic` before each deployment

**To switch to PostgreSQL (paid tier):**
1. Uncomment PostgreSQL config in `settings.py`
2. Set `DB_*` variables in `.env`
3. Run `python manage.py migrate`

---

## 13. Build Progress — Phase Tracker

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Project foundation, models, base layout, login | ✅ Complete |
| **Phase 2** | Auth flow, user management, permissions, profile | ✅ Complete |
| **Phase 3** | Inventory, Production, Sales, Dashboards | ✅ Complete |
| **Phase 4** | Waste module, Reports & Analytics | 🔲 Not Started |
| **Phase 5** | QA, Polish, Production Deployment hardening | 🔲 Not Started |

---

## 14. Phase 4 — What to Build Next

### A — Waste Module (`apps/waste`)

**Role access:** Admin approves/rejects; Production + Sales report waste

**Pages to build:**
- `waste/report.html` — form: item (Tom Select), quantity, reason, date
- `waste/history.html` — DataTable with status badges, filterable
- `waste/pending.html` — Admin only; approve/reject with notes

**Critical implementation note:**
When admin approves a waste report → `SnackItem.current_stock -= quantity` atomically. If stock would go below 0, **block the approval** with a clear error — do not allow negative stock.

**URL patterns:**
```
/waste/report/         → report_view (GET + POST)
/waste/history/        → history_view
/waste/pending/        → pending_view (admin only)
/waste/<uuid>/review/  → review_view (admin only, POST: approve/reject)
```

### B — Reports Module (`apps/reports`)

**All report pages use:** DataTables with copy/excel/pdf/print + filter form (GET-based, not POST — for shareable/bookmarkable URLs)

**Pages to build:**
- `reports/production.html` — filter: date range, user, item
- `reports/sales.html` — filter: date range, user, item; totals row
- `reports/waste.html` — filter: date range, status, reported_by
- `reports/summary.html` — admin only; cross-department combined view

---

## 15. Known Gotchas & Hard-Won Lessons

| Issue | Root Cause | Fix |
|---|---|---|
| Delete toast showed "undefined" | `pk` variable scope issue — row reference lost after modal opened | Store row reference on the modal element: `$('#modal').data('row', $row)` |
| Tom Select wouldn't visually reset | Using DOM property lookup instead of stored instance | Always store the return value of `new TomSelect()` and call `.clear()` on it directly |
| CSS truncation not working on DataTables cells | DataTables overrides inline styles | Use `!important` on truncation CSS |
| CSRF 403 on Ajax POST pages without forms | No `csrfmiddlewaretoken` in DOM | Add hidden `<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}" />` immediately after `{% block content %}` |
| Race condition on stock updates | Using `.save()` loads the full object, increments in Python, then saves — concurrent requests cause double-counting | Always use `filter().update(current_stock=F('current_stock') + N)` inside `transaction.atomic()` |
| `{% empty %}` block crashes DataTables | DataTables replaces tbody content — Django's empty block conflicts | Never use `{% empty %}` on tables managed by DataTables |
| `is_blocked` field confusion | Field was originally planned, then removed | Activation/deactivation uses Django's built-in `is_active` only — no `is_blocked` field exists |
| App import errors | App name in `apps.py` not matching `apps/<name>` directory pattern | All app `name` fields in `apps.py` must be `apps.<appname>` |

---
