# AI Learning Assistant - Architectural Analysis

## Executive Summary

The AI Learning Assistant is a sophisticated TypeScript React application that creates personalized, interactive learning experiences through AI-generated content and visual knowledge mapping. The system uses a hierarchical learning structure where users explore subjects through interconnected articles, questions, and visual maps, with real-time content generation via Claude AI.

## Tech Stack & Scale

**Languages & Framework:**
- TypeScript: 94 files, 25,635 lines (primary)
- TSX: 51 files, 4,695 lines (React components)
- SQL: 8 files, 168 lines (Prisma migrations)
- CSS: 1 file, 164 lines (TailwindCSS + custom)

**Core Technologies:**
- **Frontend**: React 19, TanStack Router, TanStack Query, React Flow (graph visualization)
- **Styling**: TailwindCSS, Shadcn/ui, Framer Motion
- **Backend**: TanStack Start (full-stack React), Prisma ORM, PostgreSQL
- **AI/LLM**: Anthropic Claude 3.7 Sonnet, OpenAI (dual provider support)
- **Auth**: Better Auth with session management
- **Deployment**: Vercel-ready with static output
- **Tools**: Biome (linting/formatting), Vitest (testing), TypeScript 5.7

## Architecture Overview

The application follows a **hierarchical learning domain model** with these core entities:

### Domain Model (from `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/docs/modelling-the-domain.md`)

1. **Subject** - Top-level educational topics (e.g., "JavaScript", "Machine Learning")
2. **LearningMap** - User's personalized exploration journey through knowledge space
3. **Article** - AI-generated educational content with contextual tooltips
4. **Question** - Connections between articles (both user-generated and suggested)
5. **ContextualTooltip** - Article-specific explanations for highlighted terms

### Database Schema (Prisma)

The PostgreSQL schema centers around user learning journeys:

```sql
Subject (id, title, initiallyFamiliarConcepts[], userId)
├── LearningMap (id, subjectId, createdAt, updatedAt)
    ├── Article (id, content, summary, takeaways[], type, tooltips, isRoot)
    └── Question (id, text, parentArticleId, childArticleId)
```

**Key relationships:**
- User → Subjects (1:many)
- Subject → LearningMaps (1:many) 
- LearningMap → Articles & Questions (1:many)
- Articles ↔ Questions (many:many through parent/child relations)

## Entry Points & Application Flow

### 1. Authentication & Subject Selection
- **Entry**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/routes/index.tsx`
- Users authenticate, then select/create learning subjects
- Recent subjects displayed for quick access
- Dynamic topic suggestions via LLM (planned feature)

### 2. Knowledge Calibration
- **Route**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/routes/calibration/$subjectId.tsx`
- Users select familiar concepts to personalize their learning path
- Results stored as `initiallyFamiliarConcepts[]` on Subject model
- Calibration component: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/calibration/calibration.tsx`

### 3. Learning Interface (Core Experience)
- **Route**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/routes/learning/$subjectId.tsx`
- **Main Component**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/learning-interface.tsx`
- Split-screen interface:
  - **Left**: Interactive React Flow knowledge map
  - **Right**: Article content with streaming generation and suggested questions

### 4. Article Viewing & Generation
- **Route**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/routes/learning/article/$articleId.tsx`
- Real-time article generation via streaming API
- **Streaming Hook**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-stream-article-content.ts`
- **API Endpoint**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/routes/api/lesson-stream.ts`

## Key Technical Innovations

### 1. **LLM Content Generation Pipeline**

**Multi-Provider LLM Architecture**:
- Base interface: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/features/llm-base.ts`
- Anthropic provider: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/features/anthropic.ts`
- OpenAI provider: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/features/openai.ts`
- Robust retry logic: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/lib/robust-llm-call.ts`

**Content Generators** (`/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/features/generators/`):
- `lesson.ts` - Main article content generation
- `suggested-questions.ts` - Follow-up question suggestions
- `tooltips.ts` - Contextual term explanations
- `knowledge-nodes.ts` - Learning map node generation
- `article-summary.ts` - Content summarization

### 2. **React Flow Knowledge Mapping**

**Core Components**:
- **Map Container**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/learning-map/index.tsx`
- **Layout Engine**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/services/layouts/elk.ts` (ELK.js integration)
- **Node Types**: Article nodes and Question nodes with custom styling

**State Management**:
- **Map Core Logic**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/learning-map/use-map-core.ts`
- **Layout Hook**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-react-flow-layout.test.ts`
- **Reconciliation**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-map-reconciliation.ts`

### 3. **Real-time Streaming & State Synchronization**

**Streaming Architecture**:
- Server-Sent Events for real-time article generation
- **Streaming Display**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/streaming-article-display/streaming-article-display.tsx`
- **Content Hook**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-stream-article-content.ts`

**State Management**:
- TanStack Query for server state management
- **API Hooks** (`/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/api/`):
  - `articles.ts`, `learning-maps.ts`, `questions.ts`, `subjects.ts`
- **Stable Map Hook**: `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-stable-learning-map.ts`

## Key Discoveries

### 1. **Sophisticated Prompt Engineering System**

The application has a well-structured prompt system (`/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/prompts/`):
- **Chat Prompts**: Lesson generation, summaries, tooltips, suggested questions
- **Roadmap Prompts**: Knowledge node generation and roadmap creation
- Context-aware prompts that adapt to user's knowledge calibration

### 2. **Dual Database Strategy**

**Development**: SQLite (`prisma/dev.db`)
**Production**: PostgreSQL (via `DATABASE_URL`)

Migration system with 8 migrations tracking the evolution:
- Initial schema (March 2025)
- User authentication integration (July 2025)  
- Article type system (August 2025)

### 3. **Comprehensive Testing Strategy**

**Testing Infrastructure**:
- Vitest with browser testing capability
- React Testing Library integration
- **Key Test Files**:
  - `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/hooks/use-react-flow-layout.test.ts`
  - `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/learning-interface.test.tsx`

### 4. **Production-Ready Monitoring**

**Observability**:
- OpenTelemetry integration for distributed tracing
- Helicone integration for LLM call monitoring
- Custom Logger class with contextual logging
- Structured error handling and retry logic

### 5. **Planned Enhancement System**

The `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/plans.md` reveals a sophisticated roadmap:
- **Article Types**: Deep dive, conceptual overview, challenge exercises
- **Question Categories**: Go deeper, detour, challenge
- **Dynamic Topic Seeds**: LLM-powered subject suggestions
- **Enhanced UI**: Category-based question styling and visualization

## Development Patterns & Design Decisions

### 1. **File-Based Routing with TanStack Router**
- Type-safe routing with automatic route tree generation
- Server functions for API endpoints
- Loaders for data fetching with built-in error boundaries

### 2. **Composition Over Inheritance**
- Reusable UI components in `/Users/jasonliggi/src/github.com/personal/learning-assistant-app/src/components/ui/`
- Custom hooks for complex state logic
- Provider pattern for React Flow and authentication contexts

### 3. **Zod-First Data Validation**
- Schema-driven development with Prisma-Zod generator
- Runtime type safety for LLM responses
- Consistent validation across client and server

### 4. **Progressive Enhancement Architecture**
- Server-side rendering with TanStack Start
- Client hydration for interactive features
- Graceful degradation for JavaScript-disabled scenarios

## Code Organization Excellence

### Domain-Driven Structure
- **Features**: Business logic grouped by domain (`/features/generators/`, `/features/subject-selection/`)
- **Components**: UI components with clear separation of concerns
- **Services**: External integrations and complex algorithms
- **Types**: Centralized type definitions with serialization utilities

### Testing Strategy
- **Unit Tests**: Individual function and component testing
- **Integration Tests**: API and database interaction testing
- **Hook Tests**: Custom React hook behavior validation

### Performance Optimizations
- **Caching**: LLM response caching with TTL
- **Memoization**: React.memo and useMemo for expensive calculations
- **Lazy Loading**: Dynamic imports for large components
- **Streaming**: Real-time content delivery for better perceived performance

## Development Guide

### Adding New Features
1. **Database Changes**: Update `prisma/schema.prisma`, create migration
2. **Types**: Update `src/types/serialized.ts` and serializers
3. **API**: Create server functions in `src/routes/api/` or `src/features/`
4. **UI**: Build components following the established patterns
5. **Integration**: Add TanStack Query hooks for state management

### Key Files for Common Tasks

**Adding New LLM Generators**:
- Create in `src/features/generators/`
- Add prompts in `src/prompts/`
- Follow the pattern from `knowledge-nodes.ts`

**Extending the Learning Map**:
- Modify `src/components/learning-map/`
- Update node types in `types.ts`
- Extend layout logic in `use-map-core.ts`

**Authentication Changes**:
- Configure in `src/lib/auth.ts`
- Update middleware in `src/lib/auth.server.ts`
- Modify session handling in routes

## Next Steps

### Immediate Development Priorities
1. **Implement Article Types System** - Enable different learning content formats
2. **Add Question Categories** - Enhance learning path personalization  
3. **Dynamic Topic Seeds** - Improve subject discovery experience
4. **Enhanced Error Handling** - Better user experience for LLM failures

### Architecture Improvements
1. **Performance Monitoring** - Add real user metrics
2. **Content Versioning** - Track article evolution
3. **Offline Support** - Progressive Web App capabilities
4. **Mobile Optimization** - Responsive learning interface

### Scalability Considerations
1. **Database Optimization** - Add indexes for large-scale usage
2. **Caching Strategy** - Redis integration for session data
3. **CDN Integration** - Static asset optimization
4. **Load Testing** - Validate concurrent user handling

The AI Learning Assistant represents a sophisticated blend of modern web development practices, AI integration, and educational technology. Its architecture supports both rapid feature development and long-term scalability while maintaining excellent developer experience through comprehensive tooling and testing infrastructure.
