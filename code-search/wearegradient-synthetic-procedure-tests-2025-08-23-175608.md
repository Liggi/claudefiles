# Synthetic Procedure Tests Analysis - wearegradient

**Generated:** 2025-08-23 17:56:08  
**Project:** wearegradient (Go backend)  
**Search Topic:** Synthetic procedure test handling and implementation  

## Executive Summary

The wearegradient codebase contains a comprehensive synthetic procedure testing system that allows testing AI agent procedures using synthetic conversations. The system is built around two main components:

1. **Conversation Synthesizer** (`conversations/conversation-synthesizor/`) - Handles creating and running synthetic conversations
2. **Procedure Test Conversations** (`procedures/procedures-conversations/`) - Manages procedure-specific test conversations

The system supports both single synthetic tests and batch synthetic tests for procedures.

## File Tree Visualization

```
wearegradient/
├── apis/web-api/web-procedure-conversations-api/
│   ├── start_synthetic.go                    # Start single synthetic test
│   ├── start_synthetic_batch.go             # Start batch synthetic tests
│   ├── read_synthetic_batch.go              # Read batch results
│   ├── read_synthetic_batch_sse.go          # Stream batch results
│   └── list_synthetic_batches.go            # List batches
├── conversations/conversation-synthesizor/
│   ├── start.go                             # Core synthetic conversation logic
│   ├── start_batch.go                       # Batch synthetic conversation logic
│   ├── finish.go                            # Complete synthetic conversations
│   ├── conversation/
│   │   ├── batch.go                         # Batch data structures
│   │   └── conversation.go                  # Conversation data structures
│   ├── workflows/
│   │   ├── generate_reply.go                # Generate synthetic replies
│   │   └── synthesize_reply_workflow.go     # Workflow orchestration
│   └── db/
│       ├── queries/conversations.sql        # Database queries
│       └── queries/batches.sql              # Batch queries
├── procedures/procedures-conversations/
│   ├── create.go                            # Create test conversations
│   ├── conversation_workflow.go             # Test conversation workflows
│   └── db/queries/
│       ├── test_conversations.sql           # Test conversation queries
│       └── test_conversation_events.sql     # Event queries
└── platform/platform/db/migrations/
    ├── 079_procedures_test_conversations.up.sql    # Initial schema
    ├── 314_procedure_test_conversations_add_type.up.sql  # Add type field
    └── 315_conversation_synthesizor_add_procedure_id.up.sql  # Link to procedures
```

## Code Architecture Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web API Layer                            │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│  │ start_synthetic.go  │  │   start_synthetic_batch.go       │  │
│  │ (Single Test)       │  │   (Batch Tests)                  │  │
│  └─────────────────────┘  └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Conversation Synthesizer                       │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│  │ Start() function    │  │   StartBatch() function          │  │
│  │ - Validate params   │  │   - Create batch                 │  │
│  │ - Create synthetic  │  │   - Launch multiple synthetics   │  │
│  │ - Copy resources    │  │   - Manage batch state          │  │
│  └─────────────────────┘  └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                Procedure Conversations                          │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Create() - Creates test conversation record                 │ │
│  │ ApplyTestConversationEvents() - Apply events to test       │ │
│  │ StartWorkflow() - Launch conversation workflow              │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Database Layer                             │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │ test_conversations   │  │ conversationsynthesizor.         │ │
│  │ - id                 │  │ conversations                    │ │
│  │ - procedure_id       │  │ - synthetic_external_id          │ │
│  │ - revision           │  │ - synthetic_internal_id          │ │
│  │ - type (synthetic)   │  │ - tool_config                    │ │
│  │ - status             │  │ - batch_id                       │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed File Analysis

### 1. Web API Endpoints

#### `/apis/web-api/web-procedure-conversations-api/start_synthetic.go`
- **Purpose**: Start single synthetic test conversation for a procedure
- **Key Functions**:
  - `ProcedureStartSyntheticTestConversation()` - Main API endpoint
  - **Line 57-112**: Core function implementation
- **Parameters**:
  - `Revision int` - Procedure revision to test
  - `SourceConversationID string` - Real conversation to bootstrap from
  - `ToolConfig` - Mock tool responses configuration
  - `MockResourceIDs []string` - Optional mock resources
- **Integration**: Calls `conversationsynthesizor.Start()`

#### `/apis/web-api/web-procedure-conversations-api/start_synthetic_batch.go`
- **Purpose**: Start batch of synthetic test conversations
- **Key Functions**:
  - `ProcedureStartSyntheticBatch()` - Main API endpoint
  - **Line 54-100**: Core function with batch configuration
- **Additional Parameters**:
  - `BatchSize` - Fixed at 50 conversations per batch
  - `AgentPullRequestNumber` - For testing with preview agents
  - `CustomerAgentPullRequestNumber` - For testing with preview customer agents

### 2. Core Synthetic Conversation Logic

#### `/conversations/conversation-synthesizor/start.go`
- **Purpose**: Core logic for creating synthetic conversations
- **Key Functions**:
  - `Start()` - **Line 123-318**: Main function for starting synthetic conversations
  - `validateToolConfig()` - **Line 140**: Validates tool configuration
  - `getEventsUntilSyntheticStartPoint()` - **Line 404-505**: Determines conversation starting point
  - `copyResourcesUntilAgentFirstReply()` - **Line 517-650**: Copies resources from source conversation
- **Key Logic Flow**:
  1. Validate parameters and tool configuration
  2. Read source conversation (must be finished)
  3. Extract events until synthetic start point
  4. Create procedure test conversation if procedure-specific
  5. Copy relevant resources from source
  6. Store synthetic conversation metadata

#### `/conversations/conversation-synthesizor/start_batch.go`
- **Purpose**: Batch synthetic conversation management
- **Key Functions**:
  - `StartBatch()` - Creates and manages batches of synthetic conversations
  - Handles batch state tracking and coordination

### 3. Procedure Test Conversations

#### `/procedures/procedures-conversations/create.go`
- **Purpose**: Creates procedure test conversation records
- **Key Functions**:
  - `Create()` - **Line 88-186**: Main creation function
  - **Line 135-144**: Database insertion with test conversation metadata
  - **Line 207**: Uses `conversation.ProcedureTestConversationTypeSynthetic` type
- **Key Features**:
  - Validates procedure revision is ready for testing
  - Supports "based on" functionality for replaying conversations
  - Optional workflow startup to prevent race conditions

### 4. Database Schema

#### Test Conversations Table (`procedures.test_conversations`)
```sql
CREATE TABLE procedures.test_conversations (
  id           TEXT PRIMARY KEY,
  company_id   TEXT NOT NULL,
  procedure_id TEXT NOT NULL,
  revision     BIGINT NOT NULL,
  type         TEXT NOT NULL,  -- 'synthetic' or 'manual'
  status       TEXT NOT NULL,
  creator      TEXT NOT NULL,
  created      TIMESTAMP WITH TIME ZONE NOT NULL
);
```

#### Synthetic Conversations Table (`conversationsynthesizor.conversations`)
```sql
INSERT INTO conversationsynthesizor.conversations (
  synthetic_external_id,
  synthetic_internal_id,
  company_id,
  source_id,
  procedure_id,
  procedure_revision,
  tool_config,
  batch_id
) VALUES (...)
```

## Cross-Reference Map

### Data Flow for Single Synthetic Test:
1. **API Call** → `start_synthetic.go:ProcedureStartSyntheticTestConversation()`
2. **Validation** → Check procedure exists and user permissions
3. **Synthesis** → `conversationsynthesizor.Start()`
4. **Test Creation** → `proceduresconversations.Create()` with `TypeSynthetic`
5. **Resource Copying** → Copy resources from source conversation
6. **Database Storage** → Insert into both `test_conversations` and `conversationsynthesizor.conversations`
7. **Workflow Launch** → Start conversation generation workflow

### Data Flow for Batch Synthetic Tests:
1. **API Call** → `start_synthetic_batch.go:ProcedureStartSyntheticBatch()`
2. **Batch Creation** → `conversationsynthesizor.StartBatch()`
3. **Multiple Synthetics** → Launch 50 synthetic conversations per batch
4. **State Tracking** → Track batch completion and results
5. **Preview Integration** → Support for testing with PR-specific agents

### Tool Configuration System:
- **Tool Config Structure** → `syntheticconversation.ToolConfig`
- **Validation** → `validateToolConfig()` ensures tools match procedure requirements
- **Mock Responses** → Tools return predetermined responses during synthetic tests
- **Resource Mocks** → `MockResourceIDs` provide test data for procedure resources

## Implementation Summary

The synthetic procedure testing system provides a comprehensive framework for testing AI agent procedures using controlled, reproducible synthetic conversations. Key architectural decisions include:

### Core Components:
1. **Web API Layer**: Provides REST endpoints for starting and monitoring synthetic tests
2. **Conversation Synthesizer**: Handles the creation and management of synthetic conversations
3. **Procedure Conversations**: Manages procedure-specific test conversation lifecycle
4. **Workflow System**: Orchestrates synthetic conversation generation using Temporal workflows

### Key Features:
1. **Single & Batch Testing**: Support for both individual tests and large-scale batch testing
2. **Resource Management**: Automatic copying of resources from source conversations to synthetic tests
3. **Tool Mocking**: Configurable mock responses for tools used during procedures
4. **Preview Integration**: Support for testing with preview/PR-specific agent versions
5. **Event Replay**: Ability to bootstrap synthetic conversations from real conversation history
6. **Type Safety**: Strong typing for procedure test conversation types (`synthetic` vs `manual`)

### Database Design:
- **Dual Storage**: Synthetic conversations stored in both procedure-specific tables and synthesizer tables
- **Event Sourcing**: Test conversation events stored separately for isolation
- **Batch Tracking**: Complete batch lifecycle management with status tracking
- **Resource Links**: Foreign key relationships ensure data consistency

The system enables comprehensive testing of AI agent procedures by creating realistic synthetic conversations that can validate procedure logic, tool integrations, and agent responses in a controlled environment.

---

## Configuration Files and Setup Code

### Feature Flags Integration:
- Uses `featureflags` service for controlling synthetic conversation features
- Supports environment-specific feature toggles

### Authentication & Authorization:
- Requires `permission.ProcedureConversationWrite` permission
- Supports staff-only features for advanced testing scenarios
- Company-scoped access control

### Temporal Integration:
- Uses Temporal workflows for reliable synthetic conversation generation
- Supports background processing and retry logic
- Activity-based architecture for scalability

This system represents a mature, production-ready approach to synthetic testing of conversational AI procedures with comprehensive error handling, monitoring, and scalability features.