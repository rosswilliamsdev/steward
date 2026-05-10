# Auth & Permissions Implementation Plan

## Overview
Build Django authentication layer with role-based access control for donor and admin users.

---

## Step 1: Settings Configuration

**Goal:** Point Django to CustomUser model and configure auth URLs

**Tasks:**
- Add `AUTH_USER_MODEL = 'core.CustomUser'` to settings.py
- Set `LOGIN_URL = '/login/'`
- Set `LOGIN_REDIRECT_URL = '/'`
- Set `LOGOUT_REDIRECT_URL = '/login/'`

**Files modified:**
- `steward/settings.py`

---

## Step 2: Login/Logout Views

**Goal:** Implement authentication views using Django's built-in auth system

**Tasks:**
- Use Django's `LoginView` (class-based, built-in)
- Use Django's `LogoutView` (class-based, built-in)
- Create login form template at `core/templates/registration/login.html`

**Files created:**
- `core/templates/registration/login.html`

**Files modified:**
- `core/views.py` (if customization needed, otherwise use built-in views)

---

## Step 3: URL Routing

**Goal:** Wire up authentication URLs

**Tasks:**
- Add auth URL patterns to `core/urls.py`
- Include auth URLs in main `steward/urls.py`
- Routes needed:
  - `/login/` → LoginView
  - `/logout/` → LogoutView

**Files modified:**
- `core/urls.py`
- `steward/urls.py`

---

## Step 4: Base Template Infrastructure

**Goal:** Create reusable base template with authentication UI

**Tasks:**
- Create `core/templates/base.html` with:
  - Navbar showing username when logged in
  - Logout link when authenticated
  - Login link when anonymous
  - Content block for child templates
  - Basic CSS/styling (minimal)

**Files created:**
- `core/templates/base.html`

---

## Step 5: Permission Mixins

**Goal:** Create reusable permission checks for donor and admin views

**Tasks:**
- Create `DonorRequiredMixin` in `core/mixins.py`:
  - Inherits from `LoginRequiredMixin` + `UserPassesTestMixin`
  - `test_func()` returns `self.request.user.is_donor`
- Create `AdminRequiredMixin`:
  - Inherits from `LoginRequiredMixin` + `UserPassesTestMixin`
  - `test_func()` returns `self.request.user.is_admin`

**Files created:**
- `core/mixins.py`

---

## Step 6: Test Protected View

**Goal:** Build one simple protected view to verify auth works end-to-end

**Tasks:**
- Create `DashboardView` in `core/views.py`:
  - Uses `LoginRequiredMixin`
  - Shows different content for donors vs admins
  - Simple template just displays user info
- Create `core/templates/core/dashboard.html`
- Add URL route `/` → DashboardView

**Files created:**
- `core/templates/core/dashboard.html`

**Files modified:**
- `core/views.py`
- `core/urls.py`

---

## Step 7: Manual Testing

**Goal:** Verify auth system works before building features

**Test cases:**
1. **Anonymous access:**
   - Visit `/` → should redirect to `/login/`

2. **Login flow:**
   - Login with superuser (admin account)
   - Should redirect to `/` (dashboard)

3. **Authenticated access:**
   - Dashboard should show username and role
   - Navbar should show logout link

4. **Logout flow:**
   - Click logout → should redirect to `/login/`
   - Try to access `/` → should redirect to login again

5. **Permission checks:**
   - Login as donor user → verify donor-only views work
   - Login as admin user → verify admin-only views work
   - Try to access admin view as donor → should get 403 Forbidden

**Commands:**
```bash
python manage.py runserver
# Then manually test in browser at http://localhost:8000
```

---

## Success Criteria

- ✅ Can login with existing superuser
- ✅ Can logout successfully
- ✅ Anonymous users redirected to login
- ✅ Logged-in users see personalized dashboard
- ✅ Permission mixins block unauthorized access
- ✅ All auth flows work without errors

---

## Common Pitfalls to Avoid

1. **Skipping AUTH_USER_MODEL:** Must be set before first migration (already done ✓)
2. **Forgetting LoginRequiredMixin:** Always combine with UserPassesTestMixin
3. **Wrong mixin order:** LoginRequiredMixin must come FIRST in inheritance chain
4. **Missing template directories:** Ensure `core/templates/` is in TEMPLATES['DIRS']
5. **Testing with wrong user type:** Create both donor and admin test users

---

## Next Steps After Auth

Once auth is complete and tested:
1. Build donor views (fund list, contribution history, grant recommendations)
2. Build admin views (approve grants, create funds/contributions)
3. Customize Django admin for staff workflows
4. Build React dashboard component
