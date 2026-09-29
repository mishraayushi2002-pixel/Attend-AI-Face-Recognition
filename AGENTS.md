# AttendAI contributor guide

The app is a TanStack Start React frontend backed by a wildcard Netlify Function and Netlify Database. `src/routes/index.tsx` contains the route-aware shell and feature views; `src/styles.css` is the design system. `netlify/functions/api.mts` owns HTTP and security policy. Database definitions are in `db/schema.ts`; every schema edit requires a generated migration in `netlify/database/migrations`. Random verification selection is a scheduled function.

The Python service in `ai-module` owns biometric processing and persists numerical encodings. The browser must never supply a trusted student identity during face attendance. Attendance history survives student deactivation.

Use camelCase in TypeScript and snake_case physical columns. Return failures as `{ success: false, message, code }`. Use `Netlify.env.get` for runtime configuration and never embed credentials. Preserve responsive layouts. Never edit generated migration snapshots manually.
