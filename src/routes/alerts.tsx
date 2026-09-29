import { createFileRoute } from '@tanstack/react-router'
import { App } from './index'

export const Route = createFileRoute('/alerts')({ component: App })
