The Next.js frontend is built, committed, and pushed. Here's what was created under `frontend/`:

---

**Structure**
```
frontend/
├── src/
│   ├── app/
│   │   ├── login/page.tsx          ← Login with JWT auth
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx          ← Protected layout + Sidebar
│   │   │   ├── dashboard/page.tsx  ← Stats + Recharts
│   │   │   ├── students/page.tsx   ← CRUD + search + pagination
│   │   │   ├── teachers/page.tsx   ← CRUD + search + pagination
│   │   │   ├── attendance/page.tsx ← Mark by class/date + report
│   │   │   ├── fees/page.tsx       ← Invoice list + payment modal
│   │   │   └── exams/page.tsx      ← Exams + schedule + marks entry
│   ├── components/
│   │   ├── layout/  (Sidebar, Header)
│   │   └── ui/      (Button, Input, Select, Card, Badge, Table, Modal)
│   ├── hooks/useAuth.ts
│   ├── lib/ (api.ts — axios + auto-refresh, auth.ts)
│   └── types/index.ts
├── Dockerfile  (multi-stage standalone)
└── package.json / tsconfig / tailwind / next.config
```

**Key features:**
- Role-based sidebar (admin sees all, teacher sees students/attendance/exams)
- Auto token refresh on 401 with redirect to login on failure
- All forms use `react-hook-form` with validation
- `react-hot-toast` notifications
- Recharts for dashboard visualizations