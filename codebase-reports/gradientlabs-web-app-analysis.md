# Gradient Labs Web App - Architectural Analysis

**Repository:** ~/src/github.com/gradientlabs-ai/web-app  
**Analysis Date:** 2025-01-23  
**Codebase Scale:** 186K+ lines across 1,363 files (primarily TypeScript/TSX)

## Executive Summary

Gradient Labs Web App is a sophisticated customer support AI platform built as a Next.js 15 monorepo with Turbo. The application facilitates AI-driven conversation management, procedure-based workflow automation, and comprehensive evaluation through scorecards. The architecture demonstrates enterprise-grade patterns with real-time capabilities, extensive integrations (Intercom, Zendesk, Salesforce), and a robust testing strategy spanning E2E, integration, and unit tests.

## Tech Stack & Scale

**Core Technologies:**
- **Frontend:** Next.js 15.2.4 with React 19, TypeScript 5.9.2
- **Styling:** Tailwind CSS with custom design system (Tenet package)
- **Monorepo:** Turbo + pnpm workspace with 3 packages (icons, tenet, eslint-config)
- **Backend Integration:** Encore microservices via generated client
- **State Management:** SWR for data fetching, React Context for app state
- **Authentication:** WorkOS AuthKit with iron-session
- **Real-time:** Server-Sent Events (SSE) with custom retry logic
- **Rich Text:** TipTap Pro editor with custom extensions
- **Database:** Vercel KV for caching, primary data via Encore services

**Scale Metrics:**
- 750 TSX components, 373 TypeScript files
- 16 E2E test suites, comprehensive unit test coverage (3,310+ test cases)
- Multi-environment deployment (local, staging, production via Vercel)

## Architecture Overview

### Monorepo Structure
```
apps/web-app/           # Main Next.js application
├── app/                # App Router (Next.js 13+ structure)
├── components/         # Reusable UI components
├── resources/          # API client abstractions
├── providers/          # React context providers
├── lib/                # Utility functions and hooks
├── encore/             # Generated API client
├── tiptap/             # Rich text editor configuration
└── e2e-tests/          # Playwright E2E tests

packages/
├── icons/              # SVG icon library (190+ icons)
├── tenet/              # Design system components
└── tenet-eslint-plugin # Custom ESLint rules
```

### Next.js App Router Architecture
- **Multi-tenant routing:** `[companySlug]` dynamic segments for workspace isolation
- **Nested layouts:** Hierarchical layout system with company-specific navigation
- **Server/Client separation:** Clear boundaries with "use client" directives
- **Middleware:** WorkOS authentication with environment-aware redirects

## Entry Points & Flow

### Primary Entry Points
1. **`/apps/web-app/app/layout.tsx`** - Root application layout with providers
2. **`/apps/web-app/middleware.ts`** - Authentication and routing middleware
3. **`/apps/web-app/app/[companySlug]/layout.tsx`** - Company-scoped layout

### Request Flow Architecture
```
Middleware (Auth) → App Router → Server Components → API Resources → Encore Services
                                     ↓
Client Components ← SWR Cache ← API Routes ← Encore Client
```

### Key Business Domain Entry Points
- **Conversations:** `/[companySlug]/conversations` - Main conversation management
- **Procedures:** `/[companySlug]/procedures` - AI workflow automation
- **Agent Settings:** `/[companySlug]/agent-settings` - AI agent configuration
- **Insights:** `/[companySlug]/insights` - Analytics and reporting
- **Integrations:** `/[companySlug]/settings` - Third-party platform connections

## Business Logic Architecture

### Core Domains

#### 1. Conversation Management (`/components/conversations/`)
- **Timeline System:** Event-driven conversation history with 20+ event types
- **Real-time Updates:** SSE streams for live conversation monitoring
- **Multi-channel Support:** Intercom, Zendesk, email, web chat, voice calls
- **AI Interaction:** Message processing, tool execution, guardrail enforcement
- **Review System:** Human-in-the-loop feedback and quality control

#### 2. Procedure System (`/[companySlug]/procedures/`)
- **Intent-based Automation:** AI procedures triggered by user intent detection
- **Rich Text Editor:** TipTap Pro with custom extensions for procedure authoring
- **Testing Framework:** Simulated conversation testing with batch processing
- **Version Control:** Draft/live procedure states with revision history
- **Tool Integration:** External API calls and database operations

#### 3. Scorecard Evaluation (`/components/scorecard/`)
- **Quality Assessment:** Multi-dimensional conversation evaluation
- **Rating System:** Emoji reactions, numeric scores, and qualitative feedback
- **Outcome Tracking:** Success/failure indicators for procedure effectiveness
- **Batch Processing:** Automated evaluation of conversation batches

#### 4. Integration Platform
- **Intercom:** Full conversation sync, team assignment, state management
- **Zendesk:** Ticket integration with conversation API
- **Salesforce:** CRM data synchronization
- **Freshworks:** Customer support platform integration
- **API Management:** Webhook handling, rate limiting, error recovery

## Component Architecture & Design System

### Design System (Tenet Package)
- **Base Components:** Button, Avatar, StatusPill, TextLink, Tooltip
- **Composition Patterns:** Consistent styling via class-variance-authority
- **Theme System:** Tailwind-based with custom CSS properties
- **Accessibility:** ARIA labels, keyboard navigation, screen reader support

### Component Patterns
- **Server/Client Distinction:** Clear separation with `-server.tsx` and `-client.tsx` conventions
- **Action Pattern:** Server actions co-located with components (`_actions/` directories)
- **Hook Pattern:** Custom hooks in `_hooks/` directories for reusable logic
- **Story Pattern:** Storybook stories for component documentation and testing

### UI Component Hierarchy
```
components/ui/           # Primitive components (Button, Input, Dialog)
components/conversations/ # Domain-specific conversation components
components/scorecard/    # Evaluation and feedback components
components/integrations/ # Third-party platform integrations
components/navigation/   # App navigation and workspace switching
```

## Integration Patterns

### External Service Architecture
1. **Encore Microservices:** Generated TypeScript client with 50+ service endpoints
2. **WorkOS Authentication:** OAuth 2.0 with SAML/SSO support
3. **Vercel Deployment:** Edge functions, ISR, and analytics integration
4. **Sentry Monitoring:** Error tracking with custom middleware wrapper
5. **Livekit:** Real-time voice call infrastructure

### API Integration Strategy
- **Resource Pattern:** Abstraction layer in `/resources/` for API calls
- **Error Handling:** Comprehensive error boundaries with Sentry integration
- **Retry Logic:** Exponential backoff for failed requests
- **Caching:** SWR with custom fetcher configuration
- **Type Safety:** Full TypeScript coverage with generated API types

### Real-time Features
- **SSE Streams:** Custom hook (`useSSEStream`) for live data updates
- **Voice Calls:** WebRTC integration with Livekit for customer calls
- **Live Collaboration:** Real-time procedure editing with conflict resolution
- **Status Broadcasting:** Live agent status and conversation updates

## Testing Strategy

### Multi-layered Testing Approach

#### E2E Testing (Playwright)
- **Visual Regression:** Screenshot comparison for UI consistency
- **User Workflows:** Complete user journeys from login to task completion
- **Cross-browser:** Chrome/Chromium testing with device emulation
- **Environment Support:** Local, staging, and preview environment testing

#### Integration Testing
- **API Integration:** Full stack testing with real backend services
- **MSW Mocking:** Mock Service Worker for controlled test environments
- **Database State:** Test isolation with cleanup procedures

#### Unit Testing (Jest)
- **Component Testing:** React Testing Library for UI components
- **Logic Testing:** Pure function testing for business logic
- **Hook Testing:** Custom hook validation with testing utilities
- **Utility Testing:** Date formatting, text processing, API utilities

### Test Organization
```
e2e-tests/               # Playwright E2E tests
├── procedures/          # Procedure creation and management
├── knowledge-base/      # Knowledge management testing
├── timeline/           # Conversation timeline testing
└── utils/              # E2E testing utilities

integration-tests/       # API and service integration tests
**/*.test.{ts,tsx}      # Unit tests co-located with source
```

## Data Flow & State Management

### State Architecture
- **Server State:** SWR for API data with automatic revalidation
- **Client State:** React Context for user preferences and UI state
- **Form State:** React Hook Form with Zod validation
- **URL State:** nuqs for synchronized search parameters

### Data Flow Patterns
1. **Server Components → API Resources → Encore Services**
2. **Client Components → SWR hooks → Cached responses**
3. **Form submissions → Server Actions → API mutations → Cache invalidation**
4. **Real-time updates → SSE streams → Local state updates**

### Caching Strategy
- **Next.js ISR:** Static generation with revalidation
- **SWR Cache:** Client-side caching with stale-while-revalidate
- **Vercel KV:** Redis-compatible caching for session data
- **CDN Caching:** Static asset optimization via Vercel Edge Network

## Key Architectural Decisions

### 1. Monorepo with Turbo
- **Benefits:** Shared tooling, consistent builds, optimized caching
- **Trade-offs:** Complexity in dependency management
- **Implementation:** Workspace-based package management with pnpm

### 2. Next.js App Router
- **Benefits:** Modern React patterns, server components, nested layouts
- **Trade-offs:** Learning curve, migration complexity from Pages Router
- **Implementation:** Full adoption with server/client component strategy

### 3. Encore Backend Integration
- **Benefits:** Type-safe API client generation, microservice architecture
- **Trade-offs:** Vendor lock-in, generated code maintenance
- **Implementation:** Auto-generated client with custom resource abstractions

### 4. TipTap Rich Text Editor
- **Benefits:** Extensible, headless editor with collaborative features
- **Trade-offs:** Complex configuration, Pro license requirements
- **Implementation:** Custom extensions for procedure-specific needs

### 5. WorkOS Authentication
- **Benefits:** Enterprise SSO support, SAML integration
- **Trade-offs:** Third-party dependency for critical functionality
- **Implementation:** Middleware-based authentication with session management

## Development & Deployment

### Development Workflow
- **Hot Reloading:** Turbopack for fast development builds
- **Type Safety:** Strict TypeScript with custom lint rules
- **Code Quality:** ESLint, Prettier, Husky pre-commit hooks
- **Testing:** Jest for unit tests, Playwright for E2E

### Deployment Pipeline
- **Platform:** Vercel with automatic deployments
- **Environments:** Production (gradient-labs.ai), Staging (gradient-labs.dev)
- **Preview:** PR-based preview deployments
- **Monitoring:** Sentry error tracking, Vercel Analytics

### Build Optimization
- **Bundle Splitting:** Automatic code splitting via Next.js
- **Image Optimization:** Next.js Image component with remote patterns
- **CSS Optimization:** Tailwind purging with JIT compilation
- **Tree Shaking:** Automatic unused code elimination

## Scalability Considerations

### Performance Architecture
- **Server Components:** Reduced JavaScript bundle size
- **Streaming:** React 18 streaming for faster page loads
- **Edge Computing:** Vercel Edge Functions for global performance
- **Caching Layers:** Multi-level caching (CDN, server, client)

### Technical Debt & Future Improvements
1. **Security:** Implement CSP nonces to remove unsafe-inline policies
2. **Accessibility:** Comprehensive WCAG 2.1 AA compliance audit
3. **Performance:** Bundle size optimization and lazy loading improvements
4. **Testing:** Increase E2E test coverage for complex workflows
5. **Documentation:** API documentation and component library docs

## Next Steps & Recommendations

### Immediate Priorities
1. **Security Hardening:** CSP nonce implementation for XSS protection
2. **Performance Audit:** Core Web Vitals optimization
3. **Accessibility Review:** Screen reader and keyboard navigation testing
4. **Error Boundary Enhancement:** More granular error handling strategies

### Strategic Improvements
1. **Micro-frontend Architecture:** Consider module federation for team scaling
2. **Advanced Caching:** Implement more sophisticated cache invalidation
3. **Real-time Scaling:** WebSocket integration for high-frequency updates
4. **AI/ML Integration:** Enhanced conversation analysis and prediction models

---

This analysis represents a mature, well-architected customer support AI platform with strong engineering practices, comprehensive testing, and scalable patterns suitable for enterprise deployment.
