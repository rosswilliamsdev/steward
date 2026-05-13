# Senior Engineering Assessment: Steward

**Review Date:** 2026-05-11
**Reviewer:** Senior Engineer AI
**Target:** Job Interview in 3 Days

---

## **Executive Summary**

This is **interview-ready with 4 critical fixes**. The codebase demonstrates strong Django fundamentals, thoughtful architecture decisions, and solid test coverage. The computed balance property is your strongest architectural call. Address the N+1 queries, exception handling, and race condition before your interview.

---

## **What's Working**

### **Strong Architecture Fundamentals**
- **Computed balance property** ([core/models.py:23-28](../../core/models.py#L23-L28)) — This is solid. You avoided the stored-balance trap that creates race conditions. Smart decision for this scale.
- **Two-role permission model** — `is_donor`/`is_admin` with `UserPassesTestMixin` enforcement is appropriate. Clean separation of concerns.
- **Clean data modeling** — FKs with `PROTECT` prevent accidental cascades, `limit_choices_to` on donor FK is thoughtful, status choices are well-structured.

### **Good Django Conventions**
- **Proper CBV usage** throughout with correct mixin ordering (`LoginRequiredMixin, UserPassesTestMixin`)
- **Clean separation** between API (DRF) and template views
- **Solid test coverage** — 555 lines of real functional tests covering permissions, form validation, view logic, API contracts
- **Admin customization** shows you understand Django admin isn't just CRUD scaffolding

### **React Integration Shows Restraint**
- You didn't over-engineer this with Redux/router when a single component suffices
- Component decomposition (MetricCards, BalanceChart, RecentGrantsTable) is clean
- Loading/error states are handled
- Tailwind integration is consistent

---

## **Issues & What to Fix**

### 🔴 **Must Fix Before Interview**

#### **Issue 1: Serializer Validation Mismatch**
**Location:** [core/views.py:163-164](../../core/views.py#L163-L164)

**Current Code:**
```python
serializer = DashboardSerializer(data=data)
serializer.is_valid(raise_exception=True)
return Response(data)  # ← You validate but don't use serializer.data
```

**Problem:** You're validating the shape but returning unvalidated data. This defeats the purpose of the serializer.

**Impact:** Data inconsistencies could slip through; serializer serves no purpose.

**Fix Prompt:**
```
In core/views.py, the DashboardAPIView validates data with DashboardSerializer
but returns the original `data` dict instead of `serializer.validated_data`.
Either use serializer.validated_data in the Response, or remove the validation
entirely since the view already controls the data structure. Update the code
to follow best practices.
```

---

#### **Issue 2: Bare Exception Swallows Critical Errors**
**Location:** [core/views.py:168-170](../../core/views.py#L168-L170)

**Current Code:**
```python
except Exception:
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

**Problem:** This hides database errors, serialization bugs, auth failures — everything. You can't debug in production.

**Impact:** Production debugging impossible; masks serious bugs.

**Fix Prompt:**
```
In core/views.py, the DashboardAPIView catches all exceptions with a bare
`except Exception` and returns HTTP 500 without logging. Add proper logging
using Python's logging module so errors are captured for debugging. Import
logging, create a logger, and log the exception with traceback before
returning the 500 response.
```

---

#### **Issue 3: N+1 Query in Balance Calculation**
**Location:** [core/views.py:44-54](../../core/views.py#L44-L54) and [core/views.py:398-403](../../core/views.py#L398-L403)

**Current Code:**
```python
for fund in funds:
    fund_contributions = fund.contributions.aggregate(...)  # ← Separate query per fund
```

**Problem:** If a donor has 10 funds, this hits the DB 20+ times.

**Impact:** Performance degrades linearly with fund count; unacceptable at scale.

**Fix Prompt:**
```
In core/views.py DashboardView (lines 44-54) and FundListView (lines 398-403),
the total_contributed calculation loops through funds and aggregates
contributions separately for each fund, creating N+1 queries. Refactor to use
a single aggregate query filtering Contribution.objects by fund__donor=user.
Optimize both methods to execute in a single database query.
```

---

#### **Issue 4: Race Condition on Grant Form Validation**
**Location:** [core/forms.py:44-48](../../core/forms.py#L44-L48)

**Current Code:**
```python
if amount > fund.balance:
    raise ValidationError(...)
```

**Problem:** Balance is computed. Between form validation and save, another grant could be approved, making this check stale. You'll approve grants that exceed the balance.

**Impact:** Allows overdrafts; breaks core business rule.

**Fix Prompt:**
```
In core/forms.py, the GrantRecommendationForm validates that the amount
doesn't exceed fund.balance, but there's a race condition between validation
and save. Move this check to the view's form_valid method in
core/views.py GrantRecommendationCreateView. Use a database transaction with
select_for_update() on the fund to ensure balance is checked atomically at
save time, preventing concurrent approvals from creating overdrafts.
```

---

### 🟡 **Should Fix**

#### **Issue 5: Missing API Permission Class**
**Location:** [core/views.py:88-98](../../core/views.py#L88-L98)

**Current Code:**
```python
permission_classes = [IsAuthenticated]

def get(self, request):
    if not request.user.is_donor:
        return Response(status=status.HTTP_403_FORBIDDEN)
```

**Problem:** Manual permission check should be a reusable permission class.

**Fix Prompt:**
```
In core/views.py, DashboardAPIView manually checks if request.user.is_donor
in the get method. Create a custom DRF permission class called IsDonor that
checks user.is_authenticated and user.is_donor, then replace the manual check
with this permission class. Put the new class in a core/permissions.py file
and update the view to use permission_classes = [IsDonor].
```

---

#### **Issue 6: Time Zone Assumption**
**Location:** [core/views.py:57](../../core/views.py#L57)

**Current Code:**
```python
year_start = timezone.now().replace(month=1, day=1, ...)
```

**Problem:** This breaks across time zones. The year boundary is ambiguous.

**Fix Prompt:**
```
In core/views.py lines 57 and 137, the year_start calculation uses
timezone.now().replace() which has timezone ambiguity issues. Refactor to
use timezone.now().date() to get a date object, then construct the year_start
as date(today.year, 1, 1), and convert to timezone-aware datetime using
timezone.make_aware(datetime.combine(year_start_date, datetime.min.time())).
Apply this fix in both DashboardView and DashboardAPIView.
```

---

#### **Issue 7: Balance Calculation Duplicated**
**Location:** [core/views.py:172-226](../../core/views.py#L172-L226) and [core/views.py:228-287](../../core/views.py#L228-L287)

**Current Code:**
Two methods `_calculate_balance_over_time` and `_calculate_balance_over_time_all_funds` share 90% logic.

**Problem:** DRY violation; maintenance burden.

**Fix Prompt:**
```
In core/views.py, the methods _calculate_balance_over_time (lines 172-226)
and _calculate_balance_over_time_all_funds (lines 228-287) are nearly
identical. Refactor into a single method that accepts optional user and fund
parameters. If fund is provided, filter by that fund; if user is provided,
filter by fund__donor=user. Remove code duplication while maintaining the
same functionality.
```

---

#### **Issue 8: Grants This Year Uses List Comprehension**
**Location:** [core/views.py:58-69](../../core/views.py#L58-L69)

**Current Code:**
```python
for fund in funds:
    grants_this_year.extend(fund.grant_recommendations.filter(...))
```

**Problem:** N queries instead of 1.

**Fix Prompt:**
```
In core/views.py DashboardView (lines 58-69), grants_this_year is built by
looping through funds and extending a list, creating N queries. Replace with
a single GrantRecommendation.objects.filter() query that filters by
fund__donor=request.user, status='approved', and reviewed_at__gte=year_start.
Calculate the total using aggregate(Sum('amount')) and count using .count().
Optimize to use a single query.
```

---

### 🟢 **Consider**

#### **Issue 9: Missing Database Indexes**
**Location:** [core/models.py](../../core/models.py)

**Problem:** Frequent filtering by `status`, `reviewed_at`, `fund__donor` without indexes.

**Fix Prompt:**
```
In core/models.py GrantRecommendation model, add database indexes for common
query patterns. Add a Meta.indexes list with: 1) composite index on
['status', 'reviewed_at'] for grants_this_year queries, and 2) composite
index on ['fund', 'status'] for per-fund grant filtering. This will improve
query performance as data grows.
```

---

#### **Issue 10: Hardcoded "All Funds" String**
**Location:** [core/views.py:149](../../core/views.py#L149) and [core/views.py:106](../../core/views.py#L106)

**Current Code:**
```python
fund_name = funds.first().name if funds.count() == 1 else 'All Funds'
```

**Problem:** Magic string appears in multiple places.

**Fix Prompt:**
```
In core/views.py, the string 'All Funds' appears in DashboardAPIView at
lines 106 and 149. Extract this to a module-level constant MULTI_FUND_LABEL
= 'All Funds' at the top of the file, then reference the constant in both
locations for easier maintenance.
```

---

#### **Issue 11: Admin save_model Incomplete**
**Location:** [core/admin.py:50-57](../../core/admin.py#L50-L57)

**Current Code:**
```python
def save_model(self, request, obj, form, change):
    if change and 'status' in form.changed_data:
        if obj.status in ['approved', 'denied']:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
```

**Problem:** Only sets reviewed_by/reviewed_at on status change during update. If staff creates a grant directly as "approved", fields stay null.

**Fix Prompt:**
```
In core/admin.py GrantRecommendationAdmin.save_model (lines 50-57), the
reviewed_by and reviewed_at fields are only set when 'change' is True and
status changes. This misses the case where staff creates a new grant directly
with status='approved' or 'denied'. Update the logic to also check if
'not change' (new object) and status is approved/denied, then set the fields
appropriately.
```

---

## **Test Coverage: Strong**

Your tests hit the important paths:
- ✅ Permission boundaries (donor can't see other donor's data)
- ✅ Form validation (balance check)
- ✅ Balance calculation correctness
- ✅ API data structure

**Missing:**
- Concurrency tests (approve same grant twice, simultaneous contributions)
- Edge cases (zero balance, negative amounts, deleted donor)

**Test Improvement Prompt:**
```
Add concurrency tests to core/tests.py to verify the grant approval race
condition is handled correctly. Create a test that simulates two simultaneous
grant approvals on the same fund using Django's TransactionTestCase and
threading. Also add edge case tests for: zero balance handling, negative
amount rejection, and behavior when a donor is deleted (should be prevented
by PROTECT).
```

---

## **React Component: Solid**

- Clean component split, proper error handling, loading states
- `fontVariantNumeric: 'tabular-nums'` shows attention to detail
- StatusBadge config is a nice pattern

**Minor Issue:**
You're parsing `balance` as float. Keep as string or use a Decimal library to avoid floating point errors (`0.30000000000000004`).

**React Improvement Prompt:**
```
In static/js/DonorDashboard.jsx, monetary values are parsed with
parseFloat() which can introduce floating-point precision errors. Since the
API returns amounts as strings (e.g., "1234.56"), format them directly for
display without converting to float. Update all parseFloat() calls to work
with string values and format using toLocaleString() on the string-parsed
number, or use a library like decimal.js for precise decimal arithmetic.
```

---

## **Documentation: Exceptional**

Your README is portfolio-grade. Architecture decisions are clear. Git workflow is specified. You even documented the "why" behind computed balance. This is rare and impressive.

---

## **Interview Preparation**

### **Questions You'll Get**

1. **"What happens if two staff approve the same grant simultaneously?"**
   Your current code has no locking. Be ready to discuss `select_for_update()` or optimistic locking via version field. Show you fixed Issue #4.

2. **"How does this scale to 10,000 donors?"**
   Your N+1 queries will kill you. Talk about `prefetch_related()`, caching, read replicas. Show you fixed Issue #3.

3. **"Why computed balance vs stored?"**
   You made the right call — explain the tradeoff (simplicity + correctness vs performance). Show you thought about it.

4. **"How do you handle negative balances?"**
   You don't currently. Form validation only checks at submission time. What if balance goes negative due to concurrent approvals? Show Issue #4 fix.

5. **"Walk me through your test strategy"**
   Lead with permission boundaries and balance calculation tests. Acknowledge missing concurrency tests and explain how you'd add them.

---

## **Final Verdict**

**This is interview-ready with fixes 1-4 completed.**

You have a clean, well-tested Django app that demonstrates real-world modeling skills. The architecture decisions are sound. The code quality is consistent. You understand Django patterns.

### **Action Plan (Priority Order)**

**Before Your Interview:**
1. ✅ Fix Issue #3 (N+1 queries) — biggest red flag for scalability
2. ✅ Fix Issue #2 (exception swallowing) — shows production thinking
3. ✅ Fix Issue #4 (race condition) — demonstrates understanding of concurrency
4. ✅ Fix Issue #1 (serializer validation) — shows DRF knowledge

**Nice to Have:**
5. Fix Issue #5 (permission class) — cleaner DRF patterns
6. Fix Issue #6 (timezone) — shows edge case awareness
7. Fix Issue #8 (grants query) — more N+1 query optimization

### **In the Interview**

**Lead with:**
- The computed balance decision — it's your strongest architectural call
- Your comprehensive test coverage (555 lines covering real scenarios)
- Django best practices (CBVs, mixins, admin customization)

**Acknowledge:**
- The N+1 issues you fixed (shows growth mindset)
- How you'd add caching/indexing for scale
- That you built this in a week (time-boxed projects show prioritization skills)

**Be Ready to Discuss:**
- Tradeoffs between computed vs stored balance
- How you'd handle concurrent operations at scale
- Your testing strategy and what you'd test next
- Why you chose Django over other frameworks
- How you'd deploy this to production (environment variables, migrations, static files)

---

## **Conclusion**

**You're going to do great.** This codebase shows senior-level thinking in domain modeling, testing, and architecture. The issues are fixable and common in v1 builds. Any interviewer who codes in Django will respect this work.

The computed balance property demonstrates you think about correctness over convenience. The test coverage shows you build for maintainability. The documentation proves you think about the next developer.

Fix the 4 critical issues, practice explaining your architectural decisions, and you'll nail this interview.

---

**Next Steps:**
1. Work through Issues 1-4 using the fix prompts above
2. Run the full test suite to verify no regressions
3. Review the "Interview Preparation" section
4. Practice explaining the computed balance decision
5. Be ready to discuss how you'd scale this to 10,000 users

Good luck! 🚀
