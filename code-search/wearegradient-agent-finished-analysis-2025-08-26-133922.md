# Agent Finished Field Analysis - `agent_finished = TRUE` Logic

**Project:** wearegradient  
**Search Topic:** agent_finished field semantics and triggers  
**Date:** 2025-08-26 13:39:22  

## Executive Summary

The `agent_finished` field in the `conversation_list_dimensions` table is set to `TRUE` when an agent emits an `agent.finish` event, indicating the agent has **completed its participation** in a conversation. This occurs in specific termination scenarios but does NOT necessarily mean the conversation was resolved successfully.

**Key Finding:** The current "handed_off" filter logic `(agent_finished = FALSE OR hand_off_reason IS NOT NULL)` appears **semantically incorrect** because:
1. An agent can finish a conversation due to timeout/no-reply and still have `agent_finished = TRUE`
2. An agent can finish a conversation and then have it handed off afterward
3. The logic should likely be `(hand_off_reason IS NOT NULL)` exclusively

## File Tree Visualization

```
conversations/
├── conversations-list/
│   ├── reducer/
│   │   └── agent_finish.go                    ⭐ Sets agent_finished = true
│   └── db/
│       └── queries/
│           └── list.sql                       ⭐ "handed_off" filter logic
├── conversation-agent/
│   └── state/
│       ├── accepting_first_message.go         → Emits FinishEvent on timeout
│       └── dispatching_operations.go          → Emits FinishEvent on close
├── conversation-synthesizor/
│   └── workflows/
│       └── generate_reply.go                  → Emits FinishEvent on NoReply
└── common/
    └── agent/
        └── finish_event.go                    ⭐ Event definition & reasons
```

## Code Architecture Map

```
Customer Timeout/No Response
    ↓
accepting_first_message.go → agent.FinishEvent(ctx) 
    ↓
agent_finish.go → register(agent.EventTypeFinish, applyAgentFinish)
    ↓
applyAgentFinish() → p.AgentFinished = true
    ↓
conversation_list_dimensions.agent_finished = TRUE

Agent Decides "No Reply" Needed  
    ↓
generate_reply.go → agent.FinishEventWithData(ctx, FinishReasonNoReply)
    ↓
Same flow → agent_finished = TRUE

Integration Disconnect/Close
    ↓  
dispatching_operations.go → agent.FinishEventWithData(ctx, FinishReasonNoReply)
    ↓
Same flow → agent_finished = TRUE
```

## Detailed File Analysis

### `/conversations/conversations-list/reducer/agent_finish.go` (Lines 12-22)
**Purpose:** Event handler that sets `agent_finished = TRUE`

```go
func init() {
    register(agent.EventTypeFinish, applyAgentFinish)  // Line 13
}

// applyAgentFinish marks a conversation as contained. Note: we do not currently reverse this
// decision if, for example, the conversation gets re-opened.
func applyAgentFinish(ctx context.Context, _ string, _ conversation.Events, p *sqlc.UpsertListDimensionsParams) (bool, *sqlc.UpsertListDimensionsParams, error) {
    p.AgentFinished = true                            // Line 19 - THE KEY SET
    p.RolloutMode = database.NullString(string(RolloutModeLive))
    return true, p, nil
}
```

### `/conversations/conversations-list/db/queries/list.sql` (Lines 48-55)
**Purpose:** Filter logic for "handed_off" conversations

```sql
OR (
  @resolution_status::TEXT = 'handed_off'
  AND (
    d.agent_finished = FALSE      -- ⚠️ PROBLEMATIC: Excludes finished agents
    OR d.hand_off_reason IS NOT NULL
  )
)
```

### `/common/agent/finish_event.go` (Lines 25-36)  
**Purpose:** Event creation and finish reasons

```go
const EventTypeFinish = "agent.finish"

// FinishEvent brings the conversation to a close and terminates the agent.
func FinishEvent(ctx Context) *conversation.Event {
    return event(ctx, EventTypeFinish, FinishEventData{})
}

type FinishReason string
const (
    FinishReasonCustomerRequest FinishReason = "customer-request"      // Customer said resolved
    FinishReasonNoReply        FinishReason = "customer-unresponsive"  // Timeout/ghosted  
    FinishReasonProcedure      FinishReason = "procedure"              // Procedure decided to close
    FinishReasonOpeningHours   FinishReason = "opening-hours"          // Would handoff but closed
)
```

### `/conversations/conversation-agent/state/accepting_first_message.go` (Lines 54-57)
**Purpose:** Agent timeout handling

```go
// If there was an idle timeout, we should dispatch a finish event
// as well as set it to Done.
if idleTimeout {
    return DispatchingOperations(f.sm, []*conversation.Event{
        agent.FinishEvent(ctx),     // Sets agent_finished = TRUE even on timeout!
    }), nil
}
```

### `/conversations/conversation-synthesizor/workflows/generate_reply.go` (Lines 38-42)
**Purpose:** AI decides no reply is needed

```go
if reply.NoReply {
    events = append(events, agent.FinishEventWithData(ctx, agent.FinishEventData{
        Reason: agent.FinishReasonNoReply,  // Sets agent_finished = TRUE for no-reply
    }))
}
```

## Cross-Reference Map

**Event Flow Chain:**
1. **Trigger Events:** Customer timeout, AI "no reply", integration disconnect, procedure completion
2. **Event Creation:** `agent.FinishEvent(ctx)` or `agent.FinishEventWithData(ctx, reason)`  
3. **Event Processing:** `register(agent.EventTypeFinish, applyAgentFinish)` in `agent_finish.go`
4. **Database Update:** `p.AgentFinished = true` in `UpsertListDimensions`
5. **Query Filtering:** SQL filter logic in `list.sql`

**Semantic Issue:**
- **Line 51**: `d.agent_finished = FALSE` in handed_off filter excludes conversations where:
  - Agent timed out (`FinishReasonNoReply`) AND later got handed off
  - Agent finished properly BUT conversation was subsequently handed off
  - Agent completed procedure BUT conversation required human follow-up

## Implementation Summary

### What `agent_finished = TRUE` Actually Means:
- **NOT "conversation was resolved successfully"**  
- **YES "agent has completed its participation"**

### When `agent_finished` gets set to `TRUE`:
1. **Customer timeout/no response** (`FinishReasonNoReply`)
2. **AI determines no reply needed** (`FinishReasonNoReply`) 
3. **Integration disconnect** (`FinishReasonNoReply`)
4. **Customer says issue resolved** (`FinishReasonCustomerRequest`)
5. **Procedure decides to finish** (`FinishReasonProcedure`)
6. **Would handoff but support closed** (`FinishReasonOpeningHours`)

### Current Filter Logic Problem:
The "handed_off" filter currently requires `agent_finished = FALSE`, but this excludes valid scenarios where:
- Agent finished due to timeout, then human took over → `agent_finished = TRUE` + `hand_off_reason IS NOT NULL`
- Agent completed successfully, but issue required human follow-up → Same state

### Recommended Fix:
Change Line 51 in `list.sql` from:
```sql
d.agent_finished = FALSE
OR d.hand_off_reason IS NOT NULL
```

To:
```sql  
d.hand_off_reason IS NOT NULL
```

The `agent_finished` field should not be part of handoff detection logic since it represents agent termination, not conversation resolution status.

---

## Resolution Categories (Current Logic):

**"resolved":** `agent_finished = TRUE AND hand_off_reason IS NULL`  
**"handed_off":** `agent_finished = FALSE OR hand_off_reason IS NOT NULL` ← **INCORRECT**

**Should be:**
**"handed_off":** `hand_off_reason IS NOT NULL`

This would properly capture all conversations that were handed off to humans, regardless of whether the agent had already finished its participation.