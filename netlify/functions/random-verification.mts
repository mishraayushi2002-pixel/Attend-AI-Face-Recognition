import type { Config } from '@netlify/functions'
import { db } from '../../db/index.js'
import { attendance, pendingVerifications } from '../../db/schema.js'
import { and, eq, isNull } from 'drizzle-orm'
export default async()=>{const today=new Date().toISOString().slice(0,10);const active=await db.select().from(attendance).where(and(eq(attendance.attendanceDate,today),isNull(attendance.exitTime)));if(active.length){const chosen=active[Math.floor(Math.random()*active.length)];const expiresAt=new Date(Date.now()+10*60_000);await db.insert(pendingVerifications).values({attendanceId:chosen.id,studentId:chosen.studentId,expiresAt})}}
export const config:Config={schedule:'*/15 * * * *'}
