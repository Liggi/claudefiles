# Address Verification Frontend Field Names Analysis

**Project**: gradient-labs web-app  
**Search Topic**: Address verification field naming mismatch  
**Date**: 2025-01-26-143830  
**Executive Summary**: Identified field naming inconsistency between frontend and backend expectations for back-office tasks

## File Tree Visualization

```
web-app/apps/web-app/
├── app/[companySlug]/back-office/
│   ├── _actions/
│   │   └── back-office-tasks.actions.ts         [API action]
│   ├── _components/
│   │   ├── test-procedure-dialog.tsx           [Main form component]
│   │   ├── back-office-task-stream.tsx
│   │   ├── back-office.tsx
│   │   ├── back-office-procedures-list.tsx
│   │   ├── procedure-view.tsx
│   │   └── testing-sidebar.tsx
│   └── _lib/
│       └── back-office-tasks.ts                [Task type definitions]
├── encore/
│   └── client.ts                              [TypeScript API types]
└── app/api/sse-streams/back-office-task/[id]/
    └── route.ts                               [SSE streaming endpoint]
```

## Code Architecture Map

```
Frontend Form (test-procedure-dialog.tsx)
    ↓ uses camelCase: "fullName"
    ↓
Server Action (back-office-tasks.actions.ts)
    ↓ converts to snake_case: "full_name"
    ↓
API Client (encore/client.ts)
    ↓ calls webbackofficetasksapi.CreateBackOfficeTask()
    ↓
Backend API (wearegradient/web-back-office-tasks-api)
    ↓ expects different field names per task type
```

## Field Name Analysis

### 1. Address Verification Task

**Frontend Form Fields** (test-procedure-dialog.tsx):
```typescript
const formSchema = z.object({
  fullName: z.string(),      // ← camelCase
  addressLines: z.string(),
  postcode: z.string(),
  countryCode: z.string(),
  evidence: z.array(z.instanceof(File))
});
```

**API Payload Sent** (line 111):
```typescript
inputs: {
  address_verification: {
    full_name: data.fullName,    // ← converted to snake_case
    address: {
      address_lines: addressLinesArray,
      postcode: data.postcode,
      country_code: data.countryCode,
    },
  },
}
```

**TypeScript Interface** (encore/client.ts:10282):
```typescript
export interface AddressVerificationInput {
  full_name: string;    // ← expects snake_case
  address: Address;
}
```

### 2. PEP Review Task (Inconsistency Found!)

**TypeScript Interface** (encore/client.ts:10287):
```typescript
export interface PoliticallyExposedPersonReviewInput {
  FullName: string;     // ← expects PascalCase!
  Address: Address;     // ← expects PascalCase!
  DateOfBirth: string;  // ← expects PascalCase!
}
```

**⚠️ CRITICAL FINDING**: The `PoliticallyExposedPersonReviewInput` interface uses **PascalCase** field names (`FullName`, `Address`, `DateOfBirth`), while `AddressVerificationInput` uses **snake_case** field names (`full_name`, `address`).

## Implementation Summary

### Current Address Verification Implementation Status
- ✅ **Form Component**: Properly implemented in `test-procedure-dialog.tsx`
- ✅ **Field Mapping**: Correctly maps `fullName` → `full_name` 
- ✅ **API Integration**: Uses correct action `CreateBackOfficeTask`
- ✅ **Type Safety**: Matches `AddressVerificationInput` interface expectations

### PEP Review Implementation Status
- ❌ **No Form Component Found**: No UI component found for PEP review tasks
- ⚠️ **Naming Inconsistency**: Would require PascalCase field names when implemented
- ❓ **Unknown Implementation**: May be implemented elsewhere or pending development

## Key File Analysis

### 1. test-procedure-dialog.tsx (Lines 38-58, 106-120)
**Purpose**: React form component for creating address verification tasks  
**Key Functions**:
- `formSchema`: Zod validation with camelCase field names
- `onSubmit`: Converts form data to API payload format
- Field mapping: `fullName` → `full_name`

**Form Fields Used**:
```typescript
fullName: string        → full_name: string
addressLines: string    → address_lines: string[]  
postcode: string        → postcode: string
countryCode: string     → country_code: string
evidence: File[]        → attachments: BackOfficeAttachment[]
```

### 2. back-office-tasks.actions.ts (Lines 7-25)
**Purpose**: Server action wrapper for API calls  
**Key Functions**:
- `CreateBackOfficeTask`: Calls encore client API
- Passes through task type, inputs, and attachments unchanged

### 3. encore/client.ts (Lines 10282-10294)
**Purpose**: Generated TypeScript client types  
**Critical Types**:
- `AddressVerificationInput`: Uses snake_case (`full_name`, `address`)
- `PoliticallyExposedPersonReviewInput`: Uses PascalCase (`FullName`, `Address`, `DateOfBirth`)

## Cross-Reference Map

```
Form Field → API Field → TypeScript Interface
───────────────────────────────────────────────
fullName → full_name → AddressVerificationInput.full_name ✅
[missing] → FullName → PoliticallyExposedPersonReviewInput.FullName ❌
```

## Recommended Actions

1. **For Address Verification**: Current implementation is correct and consistent
2. **For PEP Review**: When implementing, use PascalCase field names to match the interface:
   ```typescript
   inputs: {
     politically_exposed_person_review: {
       FullName: data.fullName,           // Note: PascalCase!
       Address: { ... },                  // Note: PascalCase!
       DateOfBirth: data.dateOfBirth,     // Note: PascalCase!
     }
   }
   ```
3. **Consider API Standardization**: The backend team should standardize field naming conventions across all task types

## Validation Error Context

If receiving validation errors about "FullName is missing", this suggests:
1. The frontend is sending a PEP review task
2. The payload structure doesn't match `PoliticallyExposedPersonReviewInput`
3. The field name should be exactly `FullName` (PascalCase), not `full_name` or `fullName`

## File Locations (Absolute Paths)

- **Main Form**: `/Users/jasonliggi/src/github.com/gradientlabs-ai/web-app/apps/web-app/app/[companySlug]/back-office/_components/test-procedure-dialog.tsx`
- **Server Action**: `/Users/jasonliggi/src/github.com/gradientlabs-ai/web-app/apps/web-app/app/[companySlug]/back-office/_actions/back-office-tasks.actions.ts`
- **TypeScript Types**: `/Users/jasonliggi/src/github.com/gradientlabs-ai/web-app/apps/web-app/encore/client.ts`
- **Task Constants**: `/Users/jasonliggi/src/github.com/gradientlabs-ai/web-app/apps/web-app/app/[companySlug]/back-office/_lib/back-office-tasks.ts`

---
*Analysis generated by Claude Code on 2025-01-26*