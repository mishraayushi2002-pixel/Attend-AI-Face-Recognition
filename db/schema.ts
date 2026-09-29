import { pgTable, uuid, text, boolean, integer, real, timestamp, jsonb, date, uniqueIndex } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(), username: text('username').notNull().unique(), email: text('email').notNull().unique(),
  password: text('password').notNull(), role: text('role').notNull().default('teacher'), isActive: boolean('is_active').notNull().default(true),
  failedLoginAttempts: integer('failed_login_attempts').notNull().default(0), lockUntil: timestamp('lock_until', { withTimezone: true }),
  refreshToken: text('refresh_token'), lastLogin: timestamp('last_login', { withTimezone: true }), createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(), updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow(),
})

export const students = pgTable('students', {
  id: uuid('id').defaultRandom().primaryKey(), name: text('name').notNull(), rollNumber: text('roll_number').notNull().unique(), department: text('department').notNull(),
  semester: integer('semester').notNull(), batch: text('batch').notNull(), email: text('email'), phone: text('phone'), faceEncodingRef: text('face_encoding_ref'),
  isFaceRegistered: boolean('is_face_registered').notNull().default(false), isActive: boolean('is_active').notNull().default(true), registeredBy: uuid('registered_by').references(() => users.id),
  attendanceStats: jsonb('attendance_stats').notNull().default({ total: 0, present: 0, late: 0, absent: 0, partial: 0, percentage: 0 }),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(), updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow(),
})

export const attendance = pgTable('attendance', {
  id: uuid('id').defaultRandom().primaryKey(), studentId: uuid('student_id').notNull().references(() => students.id), attendanceDate: date('attendance_date').notNull(),
  entryTime: timestamp('entry_time', { withTimezone: true }).notNull(), exitTime: timestamp('exit_time', { withTimezone: true }), duration: integer('duration'), session: text('session').notNull(),
  status: text('status').notNull(), verified: boolean('verified').notNull().default(false), verificationStatus: text('verification_status').default('pending'), verificationConfidence: real('verification_confidence'),
  location: jsonb('location'), ipAddress: text('ip_address'), userAgent: text('user_agent'), method: text('method').notNull().default('face'),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(), updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow(),
}, (t) => [uniqueIndex('attendance_student_date_session').on(t.studentId, t.attendanceDate, t.session)])

export const alerts = pgTable('alerts', {
  id: uuid('id').defaultRandom().primaryKey(), type: text('type').notNull(), severity: text('severity').notNull(), message: text('message').notNull(), ipAddress: text('ip_address'),
  userAgent: text('user_agent'), studentId: uuid('student_id').references(() => students.id), suspectedStudentId: uuid('suspected_student_id').references(() => students.id), snapshotPath: text('snapshot_path'),
  isResolved: boolean('is_resolved').notNull().default(false), resolvedBy: uuid('resolved_by').references(() => users.id), resolvedAt: timestamp('resolved_at', { withTimezone: true }), createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
})

export const pendingVerifications = pgTable('pending_verifications', {
  id: uuid('id').defaultRandom().primaryKey(), attendanceId: uuid('attendance_id').notNull().references(() => attendance.id), studentId: uuid('student_id').notNull().references(() => students.id),
  expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(), status: text('status').notNull().default('pending'), createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
})
