# Gradient Labs Web Application - Comprehensive Codebase Analysis

**Generated:** 2025-08-23  
**Location:** `/Users/jasonliggi/src/github.com/gradientlabs-ai/web-app`

## Executive Summary

Gradient Labs operates a sophisticated **Next.js 15 customer operations platform** that serves as an autonomous AI agent management system. The application enables companies to configure, monitor, and analyze AI-powered customer service conversations across multiple channels (Intercom, Zendesk, Salesforce). The architecture follows a modern monorepo pattern with a custom design system (Tenet) and comprehensive backend integration via Encore.

## Tech Stack & Scale

### Core Technologies
- **Frontend Framework:** Next.js 15.2.4 with React 19.0.0, App Router
- **Backend Integration:** Encore-based microservices architecture
- **Language:** TypeScript 5.9.2 (98,000+ lines of TS/TSX code)
- **Design System:** Custom "Tenet" built on shadcn/ui + Radix UI
- **State Management:** SWR for server state, iron-session for auth
- **Styling:** Tailwind CSS with semantic tokens
- **Monorepo:** Turborepo with pnpm workspaces

### Scale & Complexity
```
Language            Files        Lines         Code
TSX                   750        96,786       87,878
TypeScript            373        44,102       32,953
Total                1,363       186,542      160,642
```

### Key Integrations
- **WorkOS AuthKit** for authentication
- **Vercel** deployment and analytics
- **Tiptap Pro** for rich text editing
- **LiveKit** for voice conversations
- **Sentry** for error monitoring
- **Multiple CRM integrations** (Intercom, Zendesk, Salesforce, Freshworks)

## Architecture Overview

### High-Level Structure
The application follows a **multi-tenant, company-scoped architecture** with the following key domains:

1. **Conversations Management** - Core AI chat handling
2. **Agent Configuration** - AI behavior settings, languages, tone
3. **Knowledge Management** - Articles, facts, procedures
4. **Task & Workflow Management** - Back-office procedures
5. **Analytics & Insights** - Performance monitoring
6. **Integrations Hub** - External platform connections

### Directory Architecture
```
apps/web-app/
├── app/                           # Next.js App Router
│   ├── [companySlug]/            # Multi-tenant routing
│   │   ├── conversations/        # Chat management
│   │   ├── agent-settings/       # AI configuration
│   │   ├── knowledge-store/      # Content management
│   │   ├── tasks/               # Workflow management
│   │   └── integrations/        # External platforms
│   └── api/                     # API routes
├── components/                   # Feature components
├── resources/                   # Data layer
├── tiptap/                     # Rich text editor
└── packages/
    └── tenet/                  # Design system
```

## Entry Points & Flow

### 1. Authentication Flow
- **Entry:** `/` → redirects to `/{companySlug}` after WorkOS auth
- **Middleware:** `/middleware.ts` handles auth with WorkOS AuthKit
- **Session:** Iron-session for state management

### 2. Main Application Flow
```
GET / 
→ GetCurrentUser() 
→ redirect(/{company.slug}) 
→ redirect(/{companySlug}/tasks) [default dashboard]
```

### 3. Key User Journeys
- **Conversation Management:** `/{companySlug}/conversations` → List/detail views
- **Agent Configuration:** `/{companySlug}/agent-settings` → AI behavior tuning
- **Knowledge Management:** `/{companySlug}/knowledge-store` → Content CRUD
- **Real-time Chat:** `/{companySlug}/chat` → Live conversation interface

### 4. Data Flow Pattern
```
Client Component 
→ SWR Hook 
→ API Route (/api/conversations) 
→ Encore Client 
→ Backend Microservice
```

## Key Discoveries

### 1. **Sophisticated Multi-tenant Architecture**
- Company-scoped routing with `[companySlug]` dynamic segments
- Permissions and feature flags system
- Isolated data access per tenant

### 2. **Advanced AI Conversation Management**
- Real-time SSE streams for live conversations (`/api/sse-streams/`)
- Voice call integration with LiveKit
- Comprehensive filtering and search capabilities
- Export functionality through `/api/conversations/route.ts`

### 3. **Rich Text Editing Ecosystem**
- Custom Tiptap Pro implementation with collaborative editing
- Turndown for markdown conversion
- Custom extensions for specialized content types

### 4. **Robust Integration Platform**
- OAuth flows for Intercom, Zendesk, Salesforce
- Webhook handling for real-time updates
- MCP (Model Context Protocol) server integration

### 5. **Comprehensive Testing Strategy**
- **Unit Tests:** Jest with React Testing Library
- **E2E Tests:** Playwright with visual regression
- **Integration Tests:** MSW for API mocking
- **Storybook:** Component documentation and testing

### 6. **Performance Optimizations**
- Turbo caching for monorepo builds
- SWR for intelligent data fetching
- Suspense boundaries for progressive loading
- Vercel edge functions and analytics

## Development Guide

### Adding a Conversation Export Feature

Based on the codebase patterns, here's how you would implement this:

#### 1. **API Route** (`/app/api/conversations/export/route.ts`)
```typescript
import { webconversationsapi } from "@/encore/client";
import { queryAPI } from "@/lib/query-api";

export async function POST(request: Request) {
  const { conversationIds, format } = await request.json();
  
  const response = await queryAPI(
    async (client) => {
      return await client.webconversationsapi.ExportConversations({
        conversation_ids: conversationIds,
        format: format
      });
    },
    { companySlug: "..." }
  );
  
  return new Response(response.data, {
    headers: {
      'Content-Type': 'application/json',
      'Content-Disposition': `attachment; filename="conversations.${format}"`
    }
  });
}
```

#### 2. **Component Integration** (`/components/conversations/export-conversations-dialog.tsx`)
```typescript
"use client";

import { Button } from "@gradient-labs/tenet";
import { Dialog } from "@/components/ui/dialog";

export function ExportConversationsDialog({ 
  selectedConversations, 
  companySlug 
}: {
  selectedConversations: string[];
  companySlug: string;
}) {
  // Implementation following existing dialog patterns
}
```

#### 3. **Add to Conversations List** (`/components/conversations/conversation-list/conversations-list.tsx`)
- Add selection state management
- Include bulk actions toolbar
- Integrate export dialog

### Key Development Patterns

1. **Server Actions:** Use for form submissions and data mutations
2. **Resource Functions:** `/resources/*.ts` for data fetching logic  
3. **Component Structure:** Separate `-client.tsx` and `-server.tsx` components
4. **API Design:** RESTful routes with comprehensive error handling
5. **State Management:** SWR with URL-based filter state using nuqs

### File Organization Conventions
- `page.tsx` - Route components
- `layout.tsx` - Route layouts
- `loading.tsx` - Loading states
- `_components/` - Route-specific components
- `_actions/` - Server actions for the route

## Next Steps & Recommendations

### Immediate Development Opportunities
1. **Conversation Export Feature** - High-value user request, clear implementation path
2. **Enhanced Filtering** - Extend conversation filters for better UX
3. **Performance Monitoring** - Add more Sentry integration points
4. **Mobile Optimization** - Responsive design improvements

### Architectural Considerations
1. **API Consolidation** - Consider consolidating similar API routes
2. **Type Safety** - Enhance end-to-end type safety with Encore client
3. **Caching Strategy** - Implement more granular SWR cache invalidation
4. **Bundle Optimization** - Analyze and optimize JavaScript bundle sizes

### Quality & Testing
1. **E2E Coverage** - Expand Playwright test coverage for critical flows
2. **Accessibility Audit** - Comprehensive a11y testing with Storybook
3. **Performance Budget** - Establish Core Web Vitals targets
4. **Documentation** - Expand inline documentation for complex business logic

---

## Technical Architecture Insights

### Backend Integration Pattern
The application uses **Encore** as a backend-as-a-service platform, with auto-generated TypeScript clients. This provides:
- Type-safe API communication
- Automatic client generation
- Microservices architecture benefits
- Built-in observability

### Multi-tenant Security Model
- Company-scoped data access enforced at middleware level
- WorkOS-based authentication with session management
- Permission-based feature access
- Secure OAuth integration flows

### Real-time Communication
- Server-Sent Events for live conversation updates
- WebSocket fallbacks for voice communication
- Optimistic UI updates with SWR

This codebase represents a **mature, production-ready platform** with sophisticated AI conversation management capabilities, robust multi-tenant architecture, and comprehensive developer tooling.
