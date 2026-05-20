# Tumaini Bakery Management System

> **Developer:** Fidon Amos Takakwa — Dar es Salaam, Tanzania  
> **Contact:** fidonamos@gmail.com | WhatsApp: +255 713 529 019  
> **Client:** Tumaini Bakery, Dodoma, Tanzania | +255 625 511 541  
> **Project Start:** April 2026  
> **Stack:** Django · PostgreSQL/SQLite · Bootstrap 5 · jQuery · DataTables  

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
12. [Deployment — PythonAnywhere (Free Tier)](#12-deployment--pythonanywhere-free-tier)
13. [Build Progress — Phase Tracker](#13-build-progress--phase-tracker)
14. [Upgrading to PostgreSQL](#14-upgrading-to-postgresql)
15. [Known Gotchas & Hard-Won Lessons](#15-known-gotchas--hard-won-lessons)

---

## 1. Project Overview

A role-based web application that digitalizes daily operations for a bakery business — replacing manual registers with a real-time, multi-user platform.

**Three departments, each with tailored access:**

| Role | Primary Capability |
|---|---|
| **Admin** | Full system control — users, inventory, reports, waste approvals |
| **Production** | Log daily snack production, view own history |
| **Sales** | Process sales transactions (POS-style), view own history |

**Five core modules (all complete):**
1. **Inventory** — Snack item master list with real-time stock tracking
2. **Production** — Daily batch production logging per item
3. **Sales** — POS-style cart checkout with transaction history
4. **Waste Management** — Two-step report → approve workflow with stock deduction
5. **Reports & Analytics** — Filterable, printable, exportable reports per role

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
    ├── static/
    │   ├── css/
    │   │   ├── base.css
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
    │   │   ├── sales/
    │   │   │   ├── new.css
    │   │   │   ├── history.css
    │   │   │   └── detail.css
    │   │   ├── waste/
    │   │   │   ├── report.css
    │   │   │   ├── history.css
    │   │   │   └── pending.css
    │   │   └── reports/
    │   │       ├── base_report.css     ← shared report stylesheet
    │   │       ├── production.css      ← @import base_report.css + overrides
    │   │       ├── sales.css
    │   │       ├── waste.css
    │   │       └── summary.css
    │   │
    │   └── js/
    │       ├── base.js
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
    │       ├── sales/
    │       │   ├── new.js
    │       │   ├── history.js
    │       │   └── detail.js
    │       ├── waste/
    │       │   ├── report.js
    │       │   ├── history.js
    │       │   └── pending.js
    │       └── reports/
    │           ├── production.js
    │           ├── sales.js
    │           ├── waste.js
    │           └── summary.js
    │
    ├── staticfiles/                ← collectstatic output (not committed)
    │
    ├── templates/
    │   ├── base.html
    │   ├── accounts/
    │   │   ├── login.html
    │   │   ├── dashboard.html
    │   │   ├── set_new_password.html
    │   │   ├── profile.html
    │   │   └── user_list.html
    │   ├── inventory/
    │   │   └── item_list.html
    │   ├── production/
    │   │   ├── log.html
    │   │   └── history.html
    │   ├── sales/
    │   │   ├── new.html
    │   │   ├── history.html
    │   │   └── detail.html
    │   ├── waste/
    │   │   ├── report.html
    │   │   ├── history.html
    │   │   └── pending.html
    │   └── reports/
    │       ├── production.html
    │       ├── sales.html
    │       ├── waste.html
    │       └── summary.html
    │
    └── apps/
        ├── __init__.py
        ├── base_model.py
        ├── accounts/
        ├── inventory/
        ├── production/
        ├── sales/
        ├── waste/
        └── reports/
```

> **Rule:** Every Django app's `name` field in `apps.py` follows the pattern `apps.<appname>` — e.g., `apps.accounts`, `apps.inventory`. Apps live inside the `apps/` subdirectory.

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

# PostgreSQL — uncomment when moving to paid hosting
# DB_NAME=bakery_db
# DB_USER=postgres
# DB_PASSWORD=your-db-password
# DB_HOST=localhost
# DB_PORT=5432

# Run migrations
cd bakery_app
python manage.py migrate

# Create superuser (admin role)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Key `settings.py` Configuration

```python
INSTALLED_APPS = [
    ...
    'django.contrib.humanize',
    'apps.accounts',
    'apps.inventory',
    'apps.production',
    'apps.sales',
    'apps.waste',
    'apps.reports',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'
TIME_ZONE = 'Africa/Dar_es_Salaam'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Session hardening
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 8  # 8 hours

# Context processor — injects pending_waste_count into ALL templates
'apps.accounts.context_processors.bakery_context'
```

### Middleware Order (critical — do not reorder)

```python
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',
'apps.accounts.middleware.NoCacheMiddleware',          # prevents back-button after logout
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'apps.accounts.middleware.ForcePasswordChangeMiddleware',
'apps.accounts.middleware.AjaxSessionExpiredMiddleware', # returns 401 JSON on expired Ajax
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

> `first_name` and `last_name` from AbstractUser are set to `None` — not used.

### `inventory_snackitem`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `name` | VARCHAR | unique |
| `unit` | VARCHAR | choices: piece, dozen, kg, g, tray, pack |
| `price` | DECIMAL(10,2) | selling price in TZS |
| `current_stock` | POSITIVE INT | live stock — updated atomically |
| `description` | TEXT | optional |
| `is_active` | BOOLEAN | |
| `created_by` | FK → CustomUser | |
| `created_at` / `updated_at` | DATETIME | |

### `production_productionlog`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `snack_item` | FK → SnackItem | PROTECT |
| `quantity` | POSITIVE INT | |
| `production_date` | DATE | |
| `notes` | TEXT | optional |
| `logged_by` | FK → CustomUser | |
| `created_at` / `updated_at` | DATETIME | |

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
| `created_at` / `updated_at` | DATETIME | |

### `sales_saletransactionitem`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `transaction` | FK → SaleTransaction (CASCADE) | related_name=`items` |
| `snack_item` | FK → SnackItem | PROTECT |
| `quantity` | POSITIVE INT | |
| `unit_price` | DECIMAL(10,2) | price snapshot at time of sale |
| `subtotal` | DECIMAL(12,2) | auto-calculated on model `.save()` — never pass explicitly |

### `waste_wastereport`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `snack_item` | FK → SnackItem | PROTECT |
| `quantity` | POSITIVE INT | |
| `reason` | TEXT | whitespace-only input rejected by `clean_reason()` |
| `waste_date` | DATE | |
| `status` | VARCHAR | choices: `pending`, `approved`, `rejected` |
| `reported_by` | FK → CustomUser | |
| `reviewed_by` | FK → CustomUser | nullable |
| `reviewed_at` | DATETIME | nullable |
| `admin_notes` | TEXT | optional |
| `created_at` / `updated_at` | DATETIME | |

### Stock Movement Rules (Critical)

All stock changes use `SnackItem.objects.filter(pk=...).update(current_stock=F('current_stock') + N)` inside `transaction.atomic()` — **never `.save()`**.

| Event | Stock Effect |
|---|---|
| Production log saved | `+= quantity` |
| Sale transaction completed | `-= quantity` |
| Sale transaction cancelled (admin) | `+= quantity` (restored) |
| Production log deleted (admin) | `-= quantity` (reversed) |
| Waste report approved (admin) | `-= quantity` |

> Waste approval uses `select_for_update()` to lock the row. If `current_stock < report.quantity`, approval is **blocked** — stock cannot go below zero.

---

## 6. Application Architecture

### URL Namespaces

| Namespace | Base URL |
|---|---|
| `accounts` | `/` |
| `inventory` | `/inventory/` |
| `production` | `/production/` |
| `sales` | `/sales/` |
| `waste` | `/waste/` |
| `reports` | `/reports/` |

### Complete URL Map

**accounts:**
```
/                              → dashboard
/login/                        → login_view
/logout/                       → logout_view
/set-new-password/             → set_new_password
/profile/                      → profile
/profile/edit/                 → profile_edit
/change-password/              → change_password
/users/                        → user_list
/users/add/                    → user_add
/users/<uuid>/edit/            → user_edit
/users/<uuid>/toggle-active/   → user_toggle_active
/users/<uuid>/reset-password/  → user_reset_password
/users/<uuid>/delete/          → user_delete
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
/production/log/           → log (GET: render | POST: JSON batch)
/production/history/       → history
/production/<uuid>/delete/ → delete (admin only — reverses stock)
```

**sales:**
```
/sales/                    → history
/sales/new/                → new (GET: render | POST: JSON cart)
/sales/<uuid>/detail/      → detail
/sales/<uuid>/cancel/      → cancel (admin only — restores stock)
/sales/item/<uuid>/price/  → get_item_price (Ajax endpoint)
```

**waste:**
```
/waste/report/             → report_view (GET + POST — production/sales only)
/waste/history/            → history_view
/waste/pending/            → pending_view (admin only)
/waste/<uuid>/review/      → review_view (admin only, POST: approve/reject)
```

**reports:**
```
/reports/production/   → production_report (admin + production)
/reports/sales/        → sales_report (admin + sales)
/reports/waste/        → waste_report (all roles)
/reports/summary/      → summary_report (admin only)
```

### Permission Mixins (`apps/accounts/mixins.py`)

| Mixin / Decorator | Who Can Access |
|---|---|
| `AdminRequiredMixin` / `@admin_required` | admin only |
| `ProductionRequiredMixin` / `@production_required` | admin + production |
| `SalesRequiredMixin` / `@sales_required` | admin + sales |

---

## 7. Authentication & Security

### Login Flow
- Username + password only (no email login)
- Username stored and compared lowercase
- Ajax POST returning JSON — no page reload on error
- Hidden `<input name="next">` in login.html supports `?next=` redirect after login
- `login.js` sends `next` explicitly in the POST data object (not via `serialize()`)

### First Login / Password Reset
1. Admin creates user → default password = `USERNAME_IN_CAPS`
2. `must_change_password = True`
3. `ForcePasswordChangeMiddleware` blocks ALL URLs except `/set-new-password/` and `/logout/`
4. After change → `must_change_password = False`
5. Admin password reset restores same default + sets flag again

### Custom Middleware (`apps/accounts/middleware.py`)

**`ForcePasswordChangeMiddleware`** — blocks all URLs until password changed.

**`NoCacheMiddleware`** — sets `Cache-Control: no-store` on every response. Prevents browser back-button access after logout.

**`AjaxSessionExpiredMiddleware`** — intercepts 302 redirects to `/login/` on Ajax requests. Returns `{'success': False, 'session_expired': True, 'error': '...'}` with HTTP 401 instead of silently redirecting. `base.js` handles this globally via `$(document).ajaxError()` — shows a toast then redirects to `/login/?next=<current_path>` after 1.8 seconds.

### Context Processor
`bakery_context` injects `pending_waste_count` (pending `WasteReport` objects) into every template — powers sidebar badge and topbar bell for admin.

---

## 8. Role-Based Access Control

| Module / Action | Admin | Production | Sales |
|---|---|---|---|
| Inventory — view | ✓ | ✓ | ✓ |
| Inventory — add | ✓ | ✓ | — |
| Inventory — edit / delete / toggle | ✓ | — | — |
| Production — log | ✓ | ✓ | — |
| Production — history | ✓ (all) | ✓ (dept) | — |
| Production — delete log | ✓ | — | — |
| Sales — new transaction | ✓ | — | ✓ |
| Sales — history | ✓ (all) | — | ✓ (dept) |
| Sales — detail | ✓ | — | ✓ (own only) |
| Sales — cancel | ✓ | — | — |
| Waste — report | — | ✓ | ✓ |
| Waste — history | ✓ (all) | ✓ (dept) | ✓ (dept) |
| Waste — pending / approve | ✓ | — | — |
| Reports — production | ✓ | ✓ | — |
| Reports — sales | ✓ | — | ✓ |
| Reports — waste | ✓ | ✓ | ✓ |
| Reports — summary | ✓ | — | — |
| User management | ✓ | — | — |

> **Waste reporting:** Admin is **blocked** from the report form — redirected to Pending Approvals with an error if they attempt to access it.

---

## 9. Module Breakdown

### Inventory
- Admin: full CRUD + toggle active/inactive
- Production: add only
- Sales: read-only
- Stock pill: green (≥10), amber (<10), red (0)
- Delete blocked by Django PROTECT FK if item has production/sales records

### Production — Batch Logging
1. Select item (Tom Select) → enter quantity → Enter to add
2. Client-side duplicate check
3. Submit JSON batch → server validates + saves atomically + increments stock

**Payload:** `{ production_date, rows: [{ snack_item, quantity, notes }] }`

### Sales — POS Cart
1. Select item → quantity → Add
2. Client-side stock validation before adding
3. Checkout → server validates stock again server-side → saves atomically → deducts stock
4. Server returns `redirect_url` → JS redirects to transaction detail
5. `unit_price` snapshotted at sale time — price changes don't affect history

**Payload:** `{ sale_date, notes, rows: [{ snack_item, quantity }] }`

### Waste Module
- Production/Sales report waste: item, quantity, reason, date
- Admin reviews pending reports from `waste/pending.html`
- On approval: stock deducted atomically using `select_for_update()`
- Approval blocked if `current_stock < report.quantity`
- `WasteReportForm.clean_reason()` rejects whitespace-only input

**Department scoping for history:**
- Admin: all reports
- Production: `reported_by__role='production'`
- Sales: `reported_by__role='sales'`

### Reports Module
All reports use GET-based filter forms (shareable/bookmarkable URLs).

| Report | Access | Filters |
|---|---|---|
| Production | Admin + Production | Date range, user, item |
| Sales | Admin + Sales | Date range, user, item |
| Waste | All roles | Date range, status, reported_by |
| Summary | Admin only | Cross-department combined view |

**Data scope:**
- Production report: `logged_by__role__in=['admin', 'production']`
- Sales report: `sold_by__role__in=['admin', 'sales']`

**Stat cards** are computed server-side from the filtered queryset — not from DataTables.

**`footerCallback`** on production report sums quantity column from `{ search: 'applied' }` rows only — footer total updates as user filters.

**Top item:** `.values(...).annotate(total=Sum(...)).order_by('-total').first()` — returns `None` if no data, template guards with `{% if top_item %}`.

### Dashboards
Single `dashboard.html` handles all three roles with `{% if request.user.role == '...' %}` branching.

**Admin:** production_today, sales_amount_today, sales_count_today, pending_waste, active_items, recent_sales (×5), recent_production (×5)

**Production:** my_today_logs, my_today_total, month_total, active_items

**Sales:** my_sales_amount_today, my_sales_count_today, month_total, top_item, recent_sales (×5), available_items

### Profile Edit — Role-Based Rules
- **Admin:** can update Full Name, Username, Phone
- **Production / Sales:** Username and Phone only — Full Name rendered as disabled with "contact admin to change" hint
- `ProfileEditForm` receives `user_role` kwarg; pops `full_name` from `self.fields` server-side for non-admins (prevents malicious POST)
- `clean_username()` strips, lowercases, checks uniqueness excluding own pk
- After username change, user must log in with the new username

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
--clr-sidebar-w:   260px
--clr-topbar-h:    60px
```

### Layout
- Fixed sidebar (260px) + fixed topbar (60px) + scrollable main content
- Mobile (< 992px): sidebar slides off-screen, toggle button appears, overlay tap-to-close
- Footer: offsets with sidebar on desktop, full-width on mobile

### CDN Load Order in `base.html`

**In `<head>`:**
```
Bootstrap 5 CSS → Bootstrap Icons → Tom Select CSS → Tom Select JS → base.css → {% block extra_css %}
```
> Tom Select JS loads in `<head>` before jQuery — it's vanilla JS, not jQuery-dependent

**Before `</body>`:**
```
jQuery → Bootstrap 5 JS bundle → base.js → {% block extra_js %}
```

> DataTables CDN scripts load **per-page** inside `{% block extra_js %}`, never in base.html

### Files Per Page Rule — No Exceptions
```
templates/[app]/[page].html
static/css/[app]/[page].css
static/js/[app]/[page].js
```

### Reports CSS Architecture
`reports/base_report.css` is the **shared** stylesheet for all report pages. The four per-page CSS files each start with:
```css
@import url('../reports/base_report.css');
/* page-specific overrides below */
```

### Form Convention — Floating Labels with Icon Prefix
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

### Component Reference

**Buttons:**
```html
<button class="btn-primary-bakery">Primary</button>
<button class="btn-outline-bakery">Outline</button>
<button class="btn-danger-bakery">Danger</button>
<button class="btn-approve-bakery">Approve (green)</button>
```

**Status badges:**
```html
<span class="status-badge active">Active</span>
<span class="status-badge blocked">Inactive</span>
<span class="status-badge completed">Completed</span>
<span class="status-badge cancelled">Cancelled</span>
<span class="status-badge pending">Pending</span>
<span class="status-badge approved">Approved</span>
<span class="status-badge rejected">Rejected</span>
```

**Stock pills:**
```html
<span class="stock-pill ok">45</span>
<span class="stock-pill low">8</span>
<span class="stock-pill out">0</span>
```

**Action buttons (table rows):**
```html
<button class="btn-action edit"    data-url="..."><i class="bi bi-pencil"></i></button>
<button class="btn-action delete"  data-url="..."><i class="bi bi-trash"></i></button>
<button class="btn-action block"   data-url="..."><i class="bi bi-slash-circle"></i></button>
<button class="btn-action unblock" data-url="..."><i class="bi bi-check-circle"></i></button>
<button class="btn-action approve" data-url="..."><i class="bi bi-check-lg"></i></button>
<button class="btn-action reject"  data-url="..."><i class="bi bi-x-lg"></i></button>
<a      class="btn-action view"    href="..."><i class="bi bi-eye"></i></a>
<button class="btn-action cancel"  data-url="..."><i class="bi bi-x-circle"></i></button>
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

### CSRF — Pages with Ajax POST but No Form
```html
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}" />
```
Place immediately after `{% block content %}`. JS reads: `$('[name=csrfmiddlewaretoken]').val()`

### JSON POST (batch/cart submissions)
```javascript
$.ajax({
  url: url,
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(payload),
  headers: { 'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val() },
});
```

### Standard Form POST
```javascript
$.ajax({
  url: url,
  method: 'POST',
  data: $form.serialize(), // includes csrfmiddlewaretoken automatically
});
```

> When building a manual data object (not `serialize()`), you must explicitly include every field — including `next`, hidden inputs, etc.

### JsonResponse Conventions (backend)
```python
return JsonResponse({'success': True, 'message': 'Done.'})
return JsonResponse({'success': False, 'errors': form.errors})    # plural — form validation dict
return JsonResponse({'success': False, 'error': 'Single msg.'})   # singular — other errors
```

### Session Expiry (global in `base.js`)
```javascript
$(document).ajaxError(function (event, xhr) {
  if (xhr.status === 401) {
    // parse session_expired flag → show toast → redirect to /login/?next=current_path after 1.8s
  }
});
```

### Global Helpers (`base.js`)
```javascript
showToast('success' | 'error' | 'warning' | 'info', 'message');
showFormError('#error-div-id', 'message');
hideFormError('#error-div-id');

// Tom Select
const selects = makeSearchable('#my-select', { placeholder: '...' });
const mySelect = selects['my-select'];
mySelect.clear(); // visual reset — must use stored instance
```

### Form Error HTML (required on every form)
```html
<div id="FORM-ID-error" class="error-alert mb-3" style="display:none;">
  <i class="bi bi-exclamation-circle-fill"></i><span></span>
</div>
```

---

## 12. Deployment — PythonAnywhere (Free Tier)

- **Live URL:** `yourusername.pythonanywhere.com`
- **DB:** SQLite (`bakery_app/db.sqlite3`) — PostgreSQL config preserved but commented out
- **Static files:** `collectstatic` → `/home/yourusername/bakery_app/staticfiles/` served by Whitenoise
- **`DEBUG = False`** via `.env`
- **WSGI file** points to `bakery_app.settings`
- Run `python manage.py collectstatic` before each deployment push

**Deliverables shipped:**
- Live web application on PythonAnywhere
- Source code on GitHub (`github.com/Fidon/bakery_app`)
- User Manual — `Tumaini_Bakery_User_Manual.docx` (covers all 3 roles)

---

## 13. Build Progress — Phase Tracker

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Project foundation, models, base layout, login | ✅ Complete |
| **Phase 2** | Auth flow, user management, permissions, profile | ✅ Complete |
| **Phase 3** | Inventory, Production, Sales, Dashboards | ✅ Complete |
| **Phase 4** | Waste module, Reports & Analytics | ✅ Complete |
| **Phase 5** | Security hardening, session management, deployment | ✅ Complete |

**The application is fully built and live.**

---

## 14. Upgrading to PostgreSQL

When moving off PythonAnywhere free tier to a paid/VPS host:

1. Uncomment in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```
2. Uncomment `DB_*` variables in `.env` with production values
3. `pip install psycopg2-binary` and add to `requirements.txt`
4. `python manage.py migrate`
5. Update `ALLOWED_HOSTS` with new domain
6. Set up Nginx + Gunicorn
7. Configure HTTPS via Let's Encrypt

> SQLite is adequate for the bakery's user count. Upgrade before scaling beyond ~10 concurrent users due to SQLite write locking.

---

## 15. Known Gotchas & Hard-Won Lessons

| Issue | Root Cause | Fix |
|---|---|---|
| Delete toast showed "undefined" | `pk` variable scope — row reference lost after modal opened | Store row on modal element: `$('#modal').data('row', $row)` |
| Tom Select wouldn't visually reset | DOM property lookup instead of stored instance | Always store `makeSearchable()` return value and call `.clear()` on it directly |
| CSS truncation failing on DataTables cells | DataTables overrides inline styles | Use `!important` on truncation CSS |
| CSRF 403 on Ajax POST pages without forms | No `csrfmiddlewaretoken` in DOM | Add hidden input `value="{{ csrf_token }}"` immediately after `{% block content %}` |
| Race condition on stock updates | `.save()` loads full object → Python increments → saves; concurrent requests cause double-counting | Always `filter().update(current_stock=F(...) + N)` inside `transaction.atomic()` |
| `{% empty %}` crashes DataTables | DataTables replaces tbody — Django's empty block conflicts | Never use `{% empty %}` on DataTables-managed tables |
| `is_blocked` confusion | Field was originally planned, then removed | Activation/deactivation uses Django's built-in `is_active` only |
| App import errors | `name` in `apps.py` not matching directory path | All app `name` fields must be `apps.<appname>` |
| Back-button showed authenticated pages after logout | Browser cached responses | `NoCacheMiddleware` sets `Cache-Control: no-store` on every response |
| Ajax silently redirected to login on session expiry | Django returns 302; jQuery follows it silently | `AjaxSessionExpiredMiddleware` intercepts 302→login redirects on XHR and returns 401 JSON instead; `base.js` handles globally |
| Login `?next=` redirect not working with Ajax login | `serialize()` on manual data objects doesn't auto-include hidden fields | `login.js` explicitly includes `next: $("input[name=next]").val()` in the POST data object |
| Negative stock on waste approval | No stock check before deducting | `select_for_update()` locks the row; approval blocked if `current_stock < quantity` |

---

*Last updated: May 2026 — Project complete and deployed.*
