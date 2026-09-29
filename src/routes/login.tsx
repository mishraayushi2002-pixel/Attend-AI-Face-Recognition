import { createFileRoute } from '@tanstack/react-router'
import { App } from './index'

export const Route = createFileRoute('/login')({ component: App })
