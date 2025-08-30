# Back-Office Functionality Analysis - Web Application

**Project**: gradient-labs-ai/web-app  
**Analysis Date**: 2025-01-26 15:20:00  
**Focus**: Back-office components, procedure types, and task type restrictions  

## Executive Summary

The back-office functionality in the web application currently supports **exactly 2 procedure types**:
1. **Address Verification** (`address-verification`)
2. **Politically Exposed Person Review** (`politically-exposed-person-review`) 

However, **the UI is hardcoded to only show "Address Verification"** in the testing interface. While the backend supports PEP reviews, the frontend test dialog is specifically built only for address verification scenarios.

## File Tree Visualization

```
back-office/
├── page.tsx                                    # Main back-office listing page
├── procedure/[id]/page.tsx                     # Individual procedure view
├── _actions/
│   ├── back-office-tasks.actions.ts           # API calls for task creation
│   └── upload-attachment.actions.ts           # File upload handling
├── _components/
│   ├── back-office-procedures-list.tsx        # Table showing all procedures
│   ├── back-office-task-stream.tsx           # Live task execution stream
│   ├── back-office.tsx                       # Main layout component
│   ├── procedure-view.tsx                    # Individual procedure display
│   ├── test-procedure-dialog.tsx             # Testing dialog (ADDRESS ONLY)
│   └── testing-sidebar.tsx                   # Test interface sidebar
├── _hooks/
│   └── use-back-office-task-stream.ts        # Task streaming hook
└── _lib/
    └── back-office-tasks.ts                  # Task type definitions
```

## Code Architecture Map

```
┌─────────────────────────────────────────────────────────┐
│                    Back Office System                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   List View     │    │     Individual Procedure    │ │
│  │   (page.tsx)    │───▶│      (procedure/[id])      │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│           │                           │                  │
│           ▼                           ▼                  │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ Procedures List │    │      Back Office Layout     │ │
│  │   Component     │    │       + Testing Sidebar     │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│                                       │                  │
│                                       ▼                  │
│                          ┌─────────────────────────────┐ │
│                          │   Test Procedure Dialog    │ │
│                          │   (ADDRESS VERIFICATION    │ │
│                          │         ONLY)              │ │
│                          └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Detailed File Analysis

### 1. Task Type Definitions (`_lib/back-office-tasks.ts`)

**Lines 1-6:**
```typescript
export const backOfficeTasks = {
  "address-verification": "Address Verification",
  "politically-exposed-person-review": "PEP Review",
} as const;

export type BackOfficeTask = keyof typeof backOfficeTasks;
```

**Purpose**: Defines the two supported back-office task types
**Integration**: Used throughout the UI for type safety and display names

### 2. Test Procedure Dialog (`_components/test-procedure-dialog.tsx`)

**Key Restrictions Found:**
- **Line 108**: `taskType: "address-verification"` (HARDCODED!)
- **Lines 109-117**: Form inputs are specifically for address data:
  - `full_name`
  - `address.address_lines`  
  - `address.postcode`
  - `address.country_code`
- **Lines 38-57**: Form schema validates address-specific fields only
- **Line 149**: Dialog title: "Test Address Verification Procedure"

**Critical Finding**: This dialog cannot handle PEP reviews - it's completely hardcoded for address verification.

### 3. Testing Sidebar (`_components/testing-sidebar.tsx`)

**Line 88-89**: Description hardcoded to address verification:
```typescript
"Test the Address Verification procedure with sample
inputs to see how it performs."
```

### 4. API Integration (`_actions/back-office-tasks.actions.ts`)

**Lines 7-12**: Function signature accepts any `backoffice.TaskType`
```typescript
export async function CreateBackOfficeTask(data: {
  companySlug: string;
  taskType: backoffice.TaskType;  // Generic - supports both types
  inputs: backoffice.Inputs;      // Generic inputs union
  attachments?: webbackofficetasksapi.BackOfficeAttachment[];
})
```

**Backend Support**: The API layer supports both task types through generic interfaces.

### 5. Procedures List (`_components/back-office-procedures-list.tsx`)

**Lines 91-96**: Task type display logic:
```typescript
const taskType = props.getValue<BackOfficeTask>();
return (
  <Pill variant="primary">
    <Icon name="file-outline" size={12} />
    {backOfficeTasks[taskType] || taskType}  // Shows both types correctly
  </Pill>
);
```

**Integration**: Correctly displays both "Address Verification" and "PEP Review" procedures in the list.

## Cross-Reference Map

```
Task Type Definition ──────────┐
     │                         │
     ▼                         ▼
┌─────────────┐    ┌─────────────────────┐
│ Procedures  │    │   Test Dialog       │
│    List     │    │  (ADDRESS ONLY!)    │
│ (Both Types)│    │                     │
└─────────────┘    └─────────────────────┘
     │                         │
     ▼                         ▼
┌─────────────┐    ┌─────────────────────┐
│   Backend   │    │   Frontend UI       │
│  API Calls  │    │   Limitations       │
│ (Generic)   │    │                     │
└─────────────┘    └─────────────────────┘
```

## Implementation Summary

### What Works:
1. **Backend Support**: Full API support for both task types (`address-verification`, `politically-exposed-person-review`)
2. **Procedure Listing**: Correctly displays both types of procedures in the back-office list
3. **Type Safety**: Proper TypeScript definitions exist for both task types
4. **Individual Procedure Views**: Can view procedures of any supported type

### What's Restricted:
1. **Testing Interface**: Completely hardcoded for address verification only
2. **Form Inputs**: Test dialog only accepts address-related fields
3. **UI Text**: All testing-related text mentions only address verification
4. **Task Creation**: Test flow can only create `address-verification` tasks

### Verification of User's Belief:
**PARTIALLY CORRECT** - The user's belief that "only address-verification procedures are supported" is correct **for the testing interface** but incorrect for the overall system. The backend and procedure management supports both types, but the test dialog is indeed limited to address verification only.

## Key Findings:

1. **Two Task Types Defined**: `address-verification` and `politically-exposed-person-review`
2. **UI Limitation**: Test dialog hardcoded to address verification only (Line 108 in test-procedure-dialog.tsx)
3. **Backend Flexibility**: API supports both task types generically
4. **Display Support**: Procedure list correctly shows both types
5. **Testing Gap**: No way to test PEP review procedures through the UI

This analysis confirms the user's observation while revealing the underlying architecture supports more than just address verification, but the testing interface needs enhancement to support PEP reviews.