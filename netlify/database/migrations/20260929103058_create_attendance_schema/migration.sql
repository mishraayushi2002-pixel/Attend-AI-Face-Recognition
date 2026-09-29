CREATE TABLE "alerts" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"type" text NOT NULL,
	"severity" text NOT NULL,
	"message" text NOT NULL,
	"ip_address" text,
	"user_agent" text,
	"student_id" uuid,
	"suspected_student_id" uuid,
	"snapshot_path" text,
	"is_resolved" boolean DEFAULT false NOT NULL,
	"resolved_by" uuid,
	"resolved_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "attendance" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"student_id" uuid NOT NULL,
	"attendance_date" date NOT NULL,
	"entry_time" timestamp with time zone NOT NULL,
	"exit_time" timestamp with time zone,
	"duration" integer,
	"session" text NOT NULL,
	"status" text NOT NULL,
	"verified" boolean DEFAULT false NOT NULL,
	"verification_status" text DEFAULT 'pending',
	"verification_confidence" real,
	"location" jsonb,
	"ip_address" text,
	"user_agent" text,
	"method" text DEFAULT 'face' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "pending_verifications" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"attendance_id" uuid NOT NULL,
	"student_id" uuid NOT NULL,
	"expires_at" timestamp with time zone NOT NULL,
	"status" text DEFAULT 'pending' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "students" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"name" text NOT NULL,
	"roll_number" text NOT NULL UNIQUE,
	"department" text NOT NULL,
	"semester" integer NOT NULL,
	"batch" text NOT NULL,
	"email" text,
	"phone" text,
	"face_encoding_ref" text,
	"is_face_registered" boolean DEFAULT false NOT NULL,
	"is_active" boolean DEFAULT true NOT NULL,
	"registered_by" uuid,
	"attendance_stats" jsonb DEFAULT '{"total":0,"present":0,"late":0,"absent":0,"partial":0,"percentage":0}' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"username" text NOT NULL UNIQUE,
	"email" text NOT NULL UNIQUE,
	"password" text NOT NULL,
	"role" text DEFAULT 'teacher' NOT NULL,
	"is_active" boolean DEFAULT true NOT NULL,
	"failed_login_attempts" integer DEFAULT 0 NOT NULL,
	"lock_until" timestamp with time zone,
	"refresh_token" text,
	"last_login" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now(),
	"updated_at" timestamp with time zone DEFAULT now()
);
--> statement-breakpoint
CREATE UNIQUE INDEX "attendance_student_date_session" ON "attendance" ("student_id","attendance_date","session");--> statement-breakpoint
ALTER TABLE "alerts" ADD CONSTRAINT "alerts_student_id_students_id_fkey" FOREIGN KEY ("student_id") REFERENCES "students"("id");--> statement-breakpoint
ALTER TABLE "alerts" ADD CONSTRAINT "alerts_suspected_student_id_students_id_fkey" FOREIGN KEY ("suspected_student_id") REFERENCES "students"("id");--> statement-breakpoint
ALTER TABLE "alerts" ADD CONSTRAINT "alerts_resolved_by_users_id_fkey" FOREIGN KEY ("resolved_by") REFERENCES "users"("id");--> statement-breakpoint
ALTER TABLE "attendance" ADD CONSTRAINT "attendance_student_id_students_id_fkey" FOREIGN KEY ("student_id") REFERENCES "students"("id");--> statement-breakpoint
ALTER TABLE "pending_verifications" ADD CONSTRAINT "pending_verifications_attendance_id_attendance_id_fkey" FOREIGN KEY ("attendance_id") REFERENCES "attendance"("id");--> statement-breakpoint
ALTER TABLE "pending_verifications" ADD CONSTRAINT "pending_verifications_student_id_students_id_fkey" FOREIGN KEY ("student_id") REFERENCES "students"("id");--> statement-breakpoint
ALTER TABLE "students" ADD CONSTRAINT "students_registered_by_users_id_fkey" FOREIGN KEY ("registered_by") REFERENCES "users"("id");