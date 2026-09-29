import { HeadContent, Scripts, createRootRoute } from '@tanstack/react-router'
import '../styles.css'
const siteName='AttendAI — College Attendance Management System'
const siteDescription='Secure face-recognition attendance with liveness checks, campus verification, live analytics, and student management.'
export const Route=createRootRoute({head:()=>({meta:[{charSet:'utf-8'},{name:'viewport',content:'width=device-width, initial-scale=1'},{title:siteName},{name:'description',content:siteDescription},{property:'og:title',content:siteName},{property:'og:description',content:siteDescription},{property:'og:type',content:'website'}]}),shellComponent:Root})
function Root({children}:{children:React.ReactNode}){return <html lang="en"><head><HeadContent/><link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet"/></head><body>{children}<Scripts/></body></html>}
