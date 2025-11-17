---
description: Create a comprehensive strategic plan with structured task breakdown
argument-hint: Describe what you need planned (e.g., "refactor authentication system", "implement microservices")
---

# Implementation Plan Command

You are analyzing a ticket and creating a detailed implementation plan. This is a planning phase in the SDLC workflow.

## Process

Think deep and follow these steps systematically:

### 1. TICKET ANALYSIS

- Extract key requirements, acceptance criteria, and constraints from the ticket
- Identify the core problem/feature being requested
- List any ambiguities or missing information and ask questions to avoid asumptions
- State explicit assumptions for any gaps

### 2. CODEBASE DISCOVERY

- Search for relevant files, components, and modules related to the ticket
- Identify existing patterns and conventions in the codebase
- Map dependencies and integration points
- Note any existing tests or documentation

### 3. TECHNICAL DESIGN

- Propose the technical approach with clear rationale
- Identify files that need to be created, modified, or deleted
- Define data models, APIs, or interfaces if applicable
- Consider error handling, edge cases, and validation
- Address security, performance, and scalability implications
- If the solution will be reused across multiple features or projects, develop and thoroughly test the initial implementation before adapting and rolling it out to other areas.

### 4. IMPLEMENTATION BREAKDOWN

Create detailed to-do items with:

- Clear, actionable task descriptions
- Logical ordering with dependencies marked
- Estimated complexity (simple/moderate/complex)
- Files affected per task
- Any prerequisite setup or configuration

### 5. RISK & IMPACT ANALYSIS

- Breaking changes or backward compatibility concerns
- Testing strategy (unit, integration, e2e)
- Database migrations or data transformations
- Deployment considerations
- Rollback plan if needed

### 6. ALTERNATIVES CONSIDERED

- Present at least one alternative approach
- Compare trade-offs (complexity, time, maintainability)
- Justify the recommended approach

## Output Format

Provide your analysis in this structure:

**[TICKET SUMMARY]**

- Brief overview of the request
- Key requirements (bulleted)
- Assumptions made, but ask questions to avoid them.

**[CODEBASE ANALYSIS]**

- Relevant files and their roles
- Existing patterns to follow
- Integration points

**[TECHNICAL APPROACH]**

- Recommended solution with rationale
- Architecture/design decisions
- Key trade-offs

**[IMPLEMENTATION PLAN]**
Detailed to-do list:

1. Task name [complexity] — files affected, brief description
2. Task name [complexity] — files affected, brief description
   ...

**[TESTING STRATEGY]**

- Test scenarios to cover
- Testing approach per layer

**[RISKS & MITIGATIONS]**

- Identified risks with mitigation strategies
- Rollback approach

**[ALTERNATIVES]**

- Alternative approach(es) with when to prefer them

## Quality Standards

- Be decisive and assertive in recommendations
- Reference specific file paths and symbols from the codebase
- Don't fabricate—if uncertain about an API or pattern, note it
- Optimize for shipping value quickly with the simplest workable solution
- Consider repository conventions and existing patterns
- Minimum back-and-forth: make explicit assumptions and proceed

## Usage

**Now analyze the provided ticket and create the implementation plan following the process above.**
