# Codebase-Mapper Agent Evaluation Framework

## Test Scenarios

### Scenario 1: Cold Codebase Analysis
**Target**: `~/src/github.com/gradientlabs-ai/web-app` (TypeScript/Next.js frontend)
**Question**: "Analyze this codebase architecture - what is it, how is it organized, and how would I add a new feature?"
**Expected deliverable**: Complete markdown analysis report for architectural onboarding

### Scenario 2: Specific Feature Investigation  
**Target**: `~/src/github.com/gradientlabs-ai/wearegradient` (Go backend)
**Question**: "How does the action execution system work? I need to understand the flow from HTTP request to action completion."
**Expected deliverable**: Focused analysis on action execution architecture

### Scenario 3: Integration Points Discovery
**Target**: Any multi-service codebase
**Question**: "Map all external integrations - APIs, databases, message queues, third-party services. How does data flow between systems?"
**Expected deliverable**: Integration architecture diagram (text format)

## Success Criteria

### Effectiveness Metrics
- **Efficiency**: Focused exploration that identifies foundational patterns without getting lost in details
- **Accuracy**: Correctly identifies primary tech stack, framework, and architecture pattern  
- **Architectural Insight**: Discovers foundational patterns that shape how development happens
- **Onboarding Value**: Enables experienced engineer to understand system design and contribute confidently
- **Evidence Quality**: Backs architectural claims with specific file references and code evidence
- **Intellectual Honesty**: Appropriately expresses uncertainty when evidence is insufficient
- **Modern Tooling Usage**: Leverages enhanced analysis workflows (eza --git, bat, fd combinations) effectively, or states when insufficient information exists

### Output Quality Standards
- **Completeness**: All required report sections present with substantive content
- **Specificity**: File paths with line numbers for key discoveries
- **Clarity**: Executive summary understandable to developers unfamiliar with codebase
- **Usefulness**: Development guide enables new team member to contribute effectively

### Failure Modes to Watch For
- **Tool Overuse**: Spending too much time running analysis tools vs. reading code
- **Information Overload**: Getting lost in details without synthesizing insights
- **Surface Analysis**: Only documenting directory structure without understanding business logic
- **Missing Critical Paths**: Failing to identify main request/data flows

## Evaluation Questions

### Post-Analysis Assessment
1. **Discovery Efficiency**: Did the agent find the most important architectural insights quickly?
2. **Business Logic Understanding**: Can you understand what the system actually does from the report?
3. **Architectural Onboarding**: Could an experienced engineer use this to understand how the system thinks and evolves?
4. **Foundational Pattern Recognition**: Does the analysis identify the abstractions and decisions everything else builds on?
5. **Architecture Accuracy**: Are the documented patterns and flows correct?
6. **Tool Strategy**: Was the tool usage strategic or scattered?
7. **Evidence Verification**: Can architectural claims be validated against the actual codebase?
8. **Uncertainty Calibration**: Does the agent express appropriate uncertainty about unclear patterns?
9. **Development Evolution Insight**: Does the analysis distinguish between stable foundations and active development areas?

### Comparative Analysis
- **vs. Manual Exploration**: How much faster than manual directory browsing + reading?
- **vs. Documentation**: Does this provide insights missing from existing docs?  
- **vs. Previous Agent**: Improvement over the old codebase-mapper approach?

## Success Benchmark

**Minimum Viable Performance**:
- Complete analysis in ≤20 minutes
- Identify correct tech stack and main architecture pattern
- Provide at least 2 non-obvious insights about the codebase
- Include specific file references for key discoveries
- Generate actionable development guidance

**Excellence Standard**:  
- Efficient, focused analysis without artificial time pressure
- Discover foundational patterns and architectural decisions that shape development
- Map complete request/data flow with specific code paths
- Provide context for architectural decisions (why, not just what)
- Enable experienced engineer onboarding and confident system evolution decisions
- Distinguish between stable architectural foundations and active development areas
- Use modern tooling effectively or acknowledge when insufficient information exists

## Test Execution Plan

1. **Baseline Test**: Use agent on familiar codebase to validate workflow
2. **Cold Test**: Use agent on unfamiliar codebase to test real-world effectiveness  
3. **Iterative Improvement**: Refine agent prompt based on failure modes observed
4. **Comparative Validation**: Compare results to manual exploration for accuracy

## Notes

The goal is not comprehensive documentation but **strategic understanding** - enough insight to enable confident development decisions and efficient further exploration.