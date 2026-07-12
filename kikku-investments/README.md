# Kikku Investments

Django investment platform for VIP plans, MTN MoMo deposits, withdrawals, and referral commissions.

## Features

- User registration and login (phone number + password)
- VIP investment plans (VIP 1–9)
- MTN MoMo deposits to **0783108892** with screenshot upload
- **Daily income** — VIP 1–5 for **10 days**, VIP 6–9 for **15 days**
- Recharge after plan completes (new deposit)
- Withdrawal requests (admin sends to user's phone via MoMo)
- 10% referral commission (credited on deposit approval)
- Default referrer: **admin** when no referral code is used
- Admin panel to monitor activity + Django admin for approvals
- WhatsApp & Telegram community links

## How the platform works

1. User **registers** with phone number and password
2. User **chooses a VIP plan** and sends MTN MoMo to `0783108892`
3. User **uploads payment screenshot**
4. **Admin verifies** and approves in Django Admin
5. **Daily earnings start** — credited to balance once per day:
   - VIP 1–5 → **10 days** of daily income
   - VIP 6–9 → **15 days** of daily income
6. When the plan ends, user **recharges** with a new deposit
7. **Referrals** — share link, earn 10% when referral's deposit is approved
8. Users without a referral code are linked to the **admin account**
9. **Withdrawals** — user requests, admin approves and sends MoMo to user's phone

### VIP 9 example

- Investment: **400,000 FRW**
- Daily reward: **35,000 FRW** × 15 days = **525,000 FRW** total
- Profit: **125,000 FRW** (525,000 − 400,000)

## Tech Stack

- Python 3.12+
- Django 5.1
- Bootstrap 5
- SQLite (local development)
- MySQL (PythonAnywhere production)
- Pillow (deposit proof images)

## Project Structure

```
kikku_investments/
├── manage.py
├── requirements.txt
├── .env.example          # Copy to .env and configure
├── accounts/             # CustomUser, auth
├── dashboard/            # User dashboard views
├── investments/          # Deposits, VIP plans, approval logic
├── transactions/         # Transaction records
├── payments/             # (reserved)
├── referrals/            # (reserved)
├── templates/
├── static/
└── media/deposit_proofs/
```

## Local Development

### 1. Clone and enter the project

```bash
cd kikku-investments
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux / macOS
```

Edit `.env` and set your **WhatsApp group invite link**:

```env
WHATSAPP_COMMUNITY_URL=https://chat.whatsapp.com/YOUR_GROUP_INVITE_CODE
```

**How to get your WhatsApp group link:**

1. Open WhatsApp on your phone
2. Open your Kikku Investments group
3. Tap the group name → **Invite via link**
4. Copy the link (looks like `https://chat.whatsapp.com/AbCdEf...`)
5. Paste it into `.env` as `WHATSAPP_COMMUNITY_URL`

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

Your custom user model requires a phone number. Example via shell:

```bash
python manage.py shell
```

```python
from accounts.models import CustomUser
CustomUser.objects.create_superuser(
    username="admin",
    email="admin@kikku.local",
    password="your-password",
    phone_number="+250780000000",
)
```

### 7. Run the development server

```bash
..\venv\Scripts\activate
python manage.py runserver
```

Open:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Dashboard: http://127.0.0.1:8000/dashboard/

---

## Deploy to PythonAnywhere

### 1. Push code to GitHub

Upload your project to GitHub (or upload a zip to PythonAnywhere).

### 2. Open a Bash console on PythonAnywhere

Go to **Consoles** → **Bash**.

### 3. Clone the project

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/kikku-investments.git
cd kikku-investments
```

### 4. Create a virtual environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 kikku-env
# or: python3.10 -m venv venv && source venv/bin/activate

pip install -r requirements.txt
```

> **Note:** If `mysqlclient` fails to install, use PythonAnywhere's preinstalled MySQL support or install system dependencies from the PythonAnywhere help docs.

### 5. Create `.env` for production

```bash
cp .env.example .env
nano .env
```

Example production `.env`:

```env
SECRET_KEY=generate-a-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com

MOMO_NUMBER=0783108892
REFERRAL_COMMISSION_PERCENT=10

WHATSAPP_PHONE=+250783108892
WHATSAPP_CONTACT_URL=https://wa.me/250783108892
WHATSAPP_COMMUNITY_URL=https://chat.whatsapp.com/YOUR_GROUP_INVITE_CODE
TELEGRAM_GROUP_URL=https://t.me/yourgroup

DB_ENGINE=mysql
DB_NAME=yourusername$kikku
DB_USER=yourusername
DB_PASSWORD=your-mysql-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_PORT=3306
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Create MySQL database on PythonAnywhere

1. Go to **Databases**
2. Create a new MySQL database (e.g. `kikku`)
3. Copy the host, username, and password into `.env`

### 7. Run migrations and collect static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 8. Configure the Web app

Go to **Web** → **Add a new web app** → **Manual configuration** → **Python 3.10**.

**Source code:** `/home/yourusername/kikku-investments`

**Virtualenv:** `/home/yourusername/.virtualenvs/kikku-env`

**WSGI configuration file** — edit and set:

```python
import os
import sys

path = '/home/yourusername/kikku-investments'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'kikku_investments.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 9. Static files mapping

On the **Web** tab, under **Static files**, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/kikku-investments/staticfiles` |
| `/media/` | `/home/yourusername/kikku-investments/media` |

### 10. Schedule daily earnings (required)

On PythonAnywhere, go to **Tasks** and add a daily scheduled task:

```bash
python /home/yourusername/kikku-investments/manage.py process_daily_earnings
```

Set it to run once per day (e.g. midnight **Africa/Kigali** time).

This credits daily VIP income to each active investor's balance.

### 11. Set admin role

In Django Admin → Users, set your account **Role** to `Admin` so:
- Users without referral codes are assigned to you
- You see the **Admin Panel** in the dashboard sidebar

### 12. Reload the web app

Click the green **Reload** button on the Web tab.

Your site will be live at:

```
https://yourusername.pythonanywhere.com
```

---

## Admin Workflow

### Approve deposits

1. Go to `/admin/investments/deposit/`
2. Open the proof screenshot to verify MTN MoMo payment to **0783108892**
3. Select pending deposits → **Approve selected deposits**

On approval:

- User's VIP plan starts (10 or 15 days depending on plan)
- Referrer receives **10%** commission in balance immediately
- Daily income begins on next scheduled `process_daily_earnings` run

### Approve withdrawals

1. Go to `/admin/transactions/transaction/`
2. Filter by type: **Withdrawal**, status: **Pending**
3. Action: **Approve selected withdrawals**

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Random 50-char string |
| `DEBUG` | Debug mode | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hosts | `yourusername.pythonanywhere.com` |
| `CSRF_TRUSTED_ORIGINS` | HTTPS origins | `https://yourusername.pythonanywhere.com` |
| `MOMO_NUMBER` | MTN MoMo number for deposits | `0783108892` |
| `WHATSAPP_COMMUNITY_URL` | WhatsApp **group** invite link | `https://chat.whatsapp.com/...` |
| `WHATSAPP_CONTACT_URL` | Direct WhatsApp chat link | `https://wa.me/250783108892` |
| `TELEGRAM_GROUP_URL` | Telegram group link | `https://t.me/yourgroup` |
| `DB_ENGINE` | Set to `mysql` on PythonAnywhere | `mysql` |
| `DB_NAME` | MySQL database name | `yourusername$kikku` |

---

## URLs

| Path | Description |
|------|-------------|
| `/` | Landing page |
| `/register/` | User registration |
| `/login/` | User login |
| `/dashboard/` | User dashboard |
| `/dashboard/deposit/` | Submit deposit |
| `/dashboard/withdraw/` | Request withdrawal |
| `/dashboard/referrals/` | Referral link, list of referrals, earnings |
| `/dashboard/admin/` | Admin monitoring (admin users only) |
| `/dashboard/profile/` | User profile |
| `/admin/` | Django admin |

---

## Security Checklist (Production)

- [ ] Set `DEBUG=False`
- [ ] Use a strong `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain only
- [ ] Set `CSRF_TRUSTED_ORIGINS`
- [ ] Use MySQL on PythonAnywhere (not SQLite)
- [ ] Change default admin password
- [ ] Never commit `.env` to Git

---

## License

Private project — Kikku Investments.
