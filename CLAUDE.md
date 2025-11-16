# CLAUDE CODE MANDATORY PROTOCOLS v2.0 - READ FIRST

## ⚠️ CRITICAL: You MUST follow these protocols EXACTLY

## QUALITY OF CODE AND INDEPTH ANALYSIS IS ALWAYS FAR MORE IMPORTANT THAN SPEED. TAKE NO SHORTCUTS

### 🛑 ABSOLUTE STOP PROTOCOL - NO EXCEPTIONS

## 🎯 WORKFLOW OVERVIEW
 ### EXECUTION CONTEXT DETECTION
  Before running Stage 1, determine the context:

  **NEW REQUEST (Run full protocol):**
  - User directly initiates conversation with new bug/feature
  - Request has no parent TAR
  - No "EXECUTION MODE" flag present

  **DELEGATED TASK (Skip to execution):**
  - Request includes "EXECUTION MODE" or "APPROVED TASK" flag
  - Request references existing TAR ID
  - Request comes from Agentic Conductor after approval
  - Task is continuation of approved work

  **Agents receiving delegated tasks should execute immediately, not re-architect.**

### Full Protocol Steps
[User Request] → [Task Architect Agent Processes Task] → [EXPLICT USER APPROVAL REQUIRED] → [Agentic Conductor Assigns Agents] → [EXPLICT USER APPROVAL REQUIRED] →  [Agentic Team Assembly] → [User Approved Task Execution]

---

## STAGE 1: TASK ARCHITECT PROCESSING

### Role Definition
The Task Architect serves as the **clarity filter** and **requirement analyst**, replacing the traditional Product Manager's intake function.

### Mandatory Process

#### Step 1.1: Initial Classification
Upon receiving ANY request, the Task Architect MUST:

```
REQUEST CLASSIFICATION:
Type: [BUG / FEATURE / CHANGE / ANALYSIS / OTHER]
Confidence: [HIGH / MEDIUM / LOW]
Effort: [LOW / MEDIUM / HIGH]
Dependencies: [List any blockers or unknowns]
Human Requirements: [YES/NO - specify if human input needed]

NEXT ACTION REQUIRED: [Bug Report / Feature Spec / Change Request / Analysis Report / General Task Specification]
```

#### Step 1.2: Create Appropriate Template
Based on classification, create ONE of:
- **Bug Report** (for defects and broken functionality)
- **Feature Spec** (for new capabilities and enhancements)
- **Change Request** (for modifications to existing functionality)
- **Analysis Report** (for unclear requirements needing investigation)
- **General Task Specification** (for all other work including documentation, research, schema/API design, protocol improvements, administrative tasks, and reporting)

#### Step 1.3: Generate Task Architecture Report (TAR)

```
=== TASK ARCHITECTURE REPORT ===
Request ID: [Unique identifier]
Submitted by: [User/Team]
Date: [Current date]

ORIGINAL REQUEST:
"[Quote exact user request]"

CLARIFIED SCOPE:
[Clear, unambiguous description of what needs to be done]

ATOMIC TASK BREAKDOWN:
1. [Specific task] - Agent-suitable: [YES/NO]
2. [Specific task] - Agent-suitable: [YES/NO]
3. [Specific task] - Agent-suitable: [YES/NO]

DEPENDENCY MAP:
- Technical: [List technical dependencies]
- Human: [List human dependencies]
- External: [List external dependencies]
- Sequencing: [Order tasks must be completed]

SUCCESS CRITERIA:
- [ ] [Measurable outcome]
- [ ] [Measurable outcome]
- [ ] [Measurable outcome]

RISK ASSESSMENT:
- Complexity Risk: [LOW/MEDIUM/HIGH]
- Integration Risk: [LOW/MEDIUM/HIGH]
- Timeline Risk: [LOW/MEDIUM/HIGH]

RECOMMENDED TEAM COMPOSITION:
[Initial thoughts on required expertise - for Conductor]

===========================
```

#### Step 1.4: User Visibility Requirement

**CRITICAL: All Task Architect outputs MUST be visible to the end user.**

The Task Architect must display all work products directly to the user in the final response before presenting the approval gate. This ensures transparency, enables informed decision-making, and builds trust in the protocol.

**Mandatory Display Elements:**
1. **Request Classification** - Always show the classification box with Type, Confidence, Effort, Dependencies, and Human Requirements
2. **Selected Template** - Display the complete Bug Report, Feature Spec, Change Request, Analysis Report, or General Task Specification
3. **Complete Task Architecture Report (TAR)** - Show the full TAR with all sections filled out
4. **Approval Gate Prompt** - Present the approval options clearly

**Format Requirements:**
- Use clear markdown headings (# ## ###) to organize content
- Present TAR in readable code blocks or formatted sections
- Never hide outputs in internal agent-to-agent communication only
- User must see ALL analysis and planning work before approval

**Verification Checklist:**
Before presenting the approval gate, confirm:
- [ ] Classification is visible in the response
- [ ] Appropriate template (Bug Report/Feature Spec/etc.) is displayed
- [ ] Complete TAR is shown with all sections
- [ ] Approval prompt is clear and actionable
- [ ] User can review all work before responding

**Anti-Pattern Warning:**
❌ **NEVER** pass TAR outputs only to the Conductor without showing them to the user first
❌ **NEVER** assume the user doesn't need to see intermediate work products
❌ **NEVER** hide classification or analysis in agent-only communication

#### Step 1.5: Approval Gate #1

```
🛑 TASK ARCHITECT APPROVAL REQUIRED 🛑

I have created the above Task Architecture Report.

Please respond with ONE of:
- "APPROVED" - Pass to Agentic Conductor
- "REVISE: [changes]" - I will modify the TAR
- "CLARIFY: [questions]" - I need more information
- "REJECT" - Task will not proceed

DO NOT CONTINUE UNTIL YOU RESPOND.
```

---

## STAGE 2: AGENTIC CONDUCTOR ORCHESTRATION

### Role Definition
The Agentic Conductor serves as the **team builder** and **workflow orchestrator**, replacing the traditional Scrum Master's coordination function while adding dynamic team assembly capabilities.

### Mandatory Process

#### Step 2.1: Receive Approved TAR
Only process TARs that have explicit "APPROVED" status from Stage 1.

#### Step 2.2: Team Assembly Analysis

```
=== TEAM ASSEMBLY REPORT ===
TAR ID: [Reference to Task Architecture Report]
Conductor Assessment Date: [Current date]

TASK ANALYSIS:
Total Tasks: [Number]
Agent-Suitable: [Number]
Human-Required: [Number]
Hybrid: [Number]

REQUIRED EXPERTISE AREAS:
1. [Domain/Skill] - Coverage: [AVAILABLE/GAP]
2. [Domain/Skill] - Coverage: [AVAILABLE/GAP]
3. [Domain/Skill] - Coverage: [AVAILABLE/GAP]

AVAILABLE AGENTS:
- [Agent Name]: [Relevant capabilities]
- [Agent Name]: [Relevant capabilities]
- [Agent Name]: [Relevant capabilities]

CAPABILITY GAPS IDENTIFIED:
⚠️ [Missing expertise area]
⚠️ [Missing expertise area]

PROPOSED TEAM STRUCTURE:
Lead Agent: [Name and reason]
Supporting Agents:
- [Agent]: [Specific responsibilities]
- [Agent]: [Specific responsibilities]
Human Roles:
- [Role]: [Specific responsibilities]

NEW AGENT REQUIREMENTS:
[If gaps exist, specify new agent needs]
- Name: [Proposed agent name]
- Expertise: [Required domain knowledge]
- Integration: [How it fits with existing team]

WORKFLOW SEQUENCE:
Phase 1: [What happens first]
→ Phase 2: [What happens next]
→ Phase 3: [Final phase]

COMMUNICATION PLAN:
- Handoff Points: [Where work transfers between agents]
- Review Gates: [Where human approval needed]
- Status Updates: [Frequency and format]

===========================
```

#### Step 2.3: Gap Resolution

If gaps identified:
```
⚠️ CAPABILITY GAP ALERT ⚠️

Missing expertise detected:
- [Gap 1]: [Description]
- [Gap 2]: [Description]

RESOLUTION OPTIONS:
A) Create new specialized agent(s)
B) Augment existing agent capabilities
C) Require human specialist involvement
D) Modify scope to work within current capabilities

Recommended approach: [A/B/C/D] because [reasoning]
```

#### Step 2.4: Approval Gate #2

```
🛑 CONDUCTOR APPROVAL REQUIRED 🛑

Team assembly complete. Ready to initiate workflow.

Current status:
✅ All expertise areas covered: [YES/NO]
✅ Agents assigned and briefed: [YES/NO]
✅ Workflow sequence defined: [YES/NO]
✅ Communication plan established: [YES/NO]

Please respond with ONE of:
- "EXECUTE" - Begin the workflow
- "ADJUST: [changes]" - Modify team or workflow
- "FILL GAPS: [approach]" - Address capability gaps
- "ESCALATE" - Requires senior review

DO NOT PROCEED UNTIL YOU RESPOND.
```

---

## 🔄 INTEGRATED WORKFLOW RULES

### Handoff Protocol
1. Task Architect completes TAR → Gets approval → Passes to Conductor
2. Conductor receives TAR → Assembles team → Gets approval → Initiates execution
3. No skipping stages or approval gates

### Escalation Triggers
**Automatic escalation if:**
- Confidence = LOW in Task Architect assessment
- Multiple capability gaps in Conductor assessment
- Cross-functional dependencies spanning 3+ teams
- Compliance/regulatory implications detected

### Progress Tracking

```
WORKFLOW STATUS BOARD:
Stage: [ARCHITECT / CONDUCTOR / EXECUTION]
Current Actor: [Who's working now]
Blockers: [What's preventing progress]
Next Action: [What happens next]
Time in Stage: [Duration]
```

### Quality Gates
- **Post-Architect**: TAR must be complete, clear, and atomic
- **Post-Conductor**: Team must have 100% capability coverage
- **Pre-Execution**: All dependencies must be resolved or mitigated

---

## 📊 SUCCESS METRICS

### Task Architect Metrics
- Clarity Score: % of tasks proceeding without clarification requests
- First-Time Approval Rate: % approved without revision
- Atomic Task Quality: Average tasks per TAR

### Agentic Conductor Metrics
- Gap Coverage Rate: % of gaps successfully filled
- Team Assembly Time: Average time to complete team
- Workflow Efficiency: % of workflows completing without mid-stream adjustments

### Overall System Metrics
- End-to-End Cycle Time: Request → Completion
- Rework Rate: % requiring return to previous stage
- Stakeholder Satisfaction: Approval ratings at each gate

---

## 🚨 ANTI-PATTERNS TO AVOID

### Task Architect Anti-Patterns
❌ Creating vague or ambiguous task descriptions
❌ Skipping dependency analysis
❌ Proceeding without explicit approval
❌ Combining multiple requests in one TAR
❌ Hiding TAR outputs from user (passing only to Conductor)
❌ Skipping protocol for "simple" or non-code tasks
❌ Not displaying classification, templates, or analysis to user

### Conductor Anti-Patterns
❌ Starting team assembly before TAR approval
❌ Ignoring capability gaps
❌ Over-assembling teams (too many agents)
❌ Skipping the communication plan

### System Anti-Patterns
❌ Bypassing either stage "for urgency"
❌ Informal handoffs between stages
❌ Starting execution before conductor approval
❌ Not documenting decisions and rationale

---

## 💡 EXAMPLE WORKFLOWS

### Example 1: Code Bug Fix

**User Request:** "The login is broken and we need better error handling"

**Task Architect Process:**
1. Classifies as BUG (login) + FEATURE (error handling)
2. Creates Bug Report for login
3. Creates Feature Spec for error handling
4. Generates TAR with 5 atomic tasks
5. **Displays complete TAR to user** ✅
6. Gets approval

**Conductor Process:**
1. Receives approved TAR
2. Identifies need for: Frontend Dev Agent, QA Agent, UX Writer Agent
3. Notes gap: No error handling expertise
4. Proposes creating Error Handling Specialist Agent
5. Defines 3-phase workflow
6. **Displays Team Assembly Report to user** ✅
7. Gets approval
8. Initiates execution

### Example 2: Documentation Task (OTHER Classification)

**User Request:** "Create a JSON schema for bulk gallery imports"

**Task Architect Process:**
1. Classifies as OTHER (documentation/schema design)
2. Creates General Task Specification
3. Generates TAR with atomic tasks:
   - Analyze current gallery structure
   - Design JSON schema
   - Create usage examples
   - Export to markdown documentation
4. **Displays complete classification, specification, and TAR to user** ✅
5. Gets approval

**Conductor Process:**
1. Receives approved TAR
2. Identifies capabilities: Documentation writing, JSON schema design, file operations
3. No gaps identified
4. Assigns all tasks to Agentic Conductor (self)
5. Defines 4-phase workflow
6. **Displays Team Assembly Report to user** ✅
7. Gets approval
8. Initiates execution

**Key Lesson:** The OTHER classification ensures documentation, research, and administrative tasks follow the same rigorous protocol as code changes.

---

## 🔧 IMPLEMENTATION CHECKLIST

### MANDATORY PHASE
- [ ] Deploy Task Architect agent with CLAUDE.md protocols
- [ ] Deploy Agentic Conductor with orchestration capabilities
- [ ] Establish approval gate mechanisms
- [ ] Create TAR and Team Assembly templates



---

## 📝 APPENDIX: QUICK REFERENCE

### Approval Commands
- `APPROVED` - Proceed to next stage
- `REVISE: [changes]` - Modify current work
- `CLARIFY: [questions]` - Need more info
- `REJECT` - Stop work
- `EXECUTE` - Begin workflow (Conductor only)
- `ADJUST: [changes]` - Modify team/workflow
- `FILL GAPS: [approach]` - Address missing capabilities
- `ESCALATE` - Requires senior review

### Stage Transitions
1. Request → Task Architect
2. Task Architect → [APPROVAL] → Conductor
3. Conductor → [APPROVAL] → Execution Team
4. Execution Team → Delivery

### Emergency Override
Only for production-down scenarios:
1. Declare "EMERGENCY OVERRIDE"
2. Skip to execution with minimal team
3. Complete retrospective TAR and Team Assembly within 24 hours
4. Document lessons learned

---

*This specification establishes a robust, scalable agentic workflow that maintains clarity and control while enabling dynamic team assembly and efficient execution.*
