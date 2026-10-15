---
title: "Delivering APIs for AI"
slug: "delivering-apis-for-ai"
cover_motif: "flow"
cover_accent: "blue"
date: 2026-07-09
categories: ["ai"]
tags: ["mcp", "api-design", "agents"]
---

The rise of AI agents and autonomous systems is fundamentally changing how we design and deliver APIs, shifting from human-centric interfaces to AI-native integration patterns that require new architectural thinking.

### The Inflection Point

Technology innovation has repeatedly transformed how we build systems. From the fourth-generation programming languages (4GL) of the 1990s that abstracted database operations to today's AI-powered code generation, each wave has forced us to rethink fundamental assumptions. We now stand at another such inflection point: the transition from human-interface (HI) APIs to agent-interface (AI) APIs.

Traditional APIs were designed as information gatherers for web pages. They returned small, digestible chunks of data that humans could consume through browser interfaces. When larger datasets were needed, we added pagination to keep response sizes manageable. This design pattern served web applications well for over two decades.

Agent-based interactions operate under entirely different constraints. AI systems don't browse web pages or click through paginated results. They need programmatic access to complete information sets, context-aware data structures, and tool definitions that enable autonomous decision-making.

### The MCP Standard: A New Integration Layer

The Model Context Protocol (MCP), introduced by Anthropic in November 2024, provides a standardized approach for connecting AI systems to data sources and tools. In December 2025, Anthropic donated MCP to the Agentic AI Foundation under the Linux Foundation, making it a vendor-neutral, community-governed standard developed through Working Groups and Spec Enhancement Proposals (SEPs). It has since been adopted by OpenAI, Google DeepMind, Microsoft, and thousands of development teams, with an ecosystem that has grown from roughly 100 servers at launch to nearly 20,000 indexed servers and on the order of 97 million monthly SDK downloads as of early 2026.

MCP addresses the traditional integration problem where connecting N systems to M systems requires N × M individual integrations. With MCP, this becomes N + M: each system needs only to implement the MCP specification once.

### Key Benefits of MCP

- Unified Integration: Systems expose capabilities through standardized tool definitions rather than custom integration code
- AI-Driven Orchestration: The AI model determines which tools to invoke based on user intent, eliminating the need for hardcoded workflow logic
- Reduced Maintenance: Changes to one system's capabilities don't require updates to all connected systems
- Composability: Tools from multiple MCP servers can be combined dynamically to solve complex tasks

### Core Protocol Primitives

The MCP specification defines three core server-side primitives:

- Resources: Data sources that AI models can read (files, database records, API responses)
- Prompts: Reusable templates that guide model behavior for specific tasks
- Tools: Functions that AI models can invoke to take actions or retrieve information

The protocol also defines client-side primitives, notably sampling (servers can request LLM completions from the client) and elicitation (servers can ask the user clarifying questions). These capabilities, along with roots (by which clients define the filesystem boundaries a server may operate within), have shifted MCP from a pure command-execution protocol toward a collaboration framework. Servers are no longer passive endpoints: they can reason via sampling, ask questions via elicitation, and coordinate multi-step background work.

### MCP in 2026: The Stateless Revision and Extensions

The protocol has evolved rapidly. The current stable specification is the 2025-11-25 revision, and a release candidate for the 2026-07-28 revision, the largest change to the protocol since launch, was published in mid-2026, with the final specification scheduled for July 28, 2026.

### The Stateless Core

The headline change is that the core protocol goes stateless. The initialize handshake and the protocol-level session are removed:

- Protocol version, client info, and client capabilities now travel with every request
- A new server/discover method lets clients fetch server capabilities on demand
- The Mcp-Session-Id header is gone
- Any MCP request can land on any server instance

This architectural shift means servers scale behind a simple round-robin load balancer with no sticky routing or shared session stores at the protocol layer. For API designers, this has a direct implication: cross-call state moves to the application layer.

Servers that need to carry state across calls do what HTTP APIs have always done: mint an explicit handle (a basket_id, a dataset_id, a browser_id) from a tool and have the model pass it back as an ordinary argument on later calls. Reference-based patterns like this are now the idiomatic approach, not an optimization.

> The stateless design creates a recurring architectural challenge: the handle is right, the store is local. I hit this firsthand building [api-ai-readiness](https://github.com/gaberger/api-ai-readiness), which runs assessments and returns a readiness://\<id\> handle pointing at the results. That's a textbook stateless explicit handle — until you run two server instances behind a load balancer, at which point the in-process state map means instance B can't resolve a handle instance A minted. For a stdio server (one process per host) it's a non-issue; for a hosted HTTP MCP server it's the exact "design for statelessness from the start" debt. The fix is always the same: back the state cache with a shared store (Redis, S3, content-addressed disk, or a database). This is the recurring lesson across MCP implementations — everyone gets the handle right and the store wrong first.

### The Extensions Framework

The 2026-07-28 revision introduces a formal extensions framework. Extensions are identified by reverse-DNS IDs, negotiated through capability maps, live in their own repositories, and version independently of the core specification. Two are official at launch:

- MCP Apps: Servers can ship interactive HTML interfaces that hosts render in sandboxed iframes. UI templates are declared ahead of time so hosts can prefetch, cache, and security-review them, and every UI-initiated action flows through the same JSON-RPC audit and consent path as a direct tool call.
- Tasks: A pattern for long-running, asynchronous work. Tasks shipped as an experimental core feature in 2025-11-25; production feedback moved it to the extensions track, where it can iterate independently.

### Governance and Stability

Governance matured alongside the protocol: every feature now has an Active → Deprecated → Removed lifecycle with a minimum twelve-month deprecation window, and Standards Track SEPs cannot be finalized until a matching scenario lands in the conformance suite. For teams building on MCP, this means the 2026-07-28 revision is designed to be a stable foundation rather than a moving target.

### Designing APIs for Agent Interaction

Traditional API design patterns break down when AI agents become the primary consumers. Several fundamental shifts are required.

### The Multi-Stage API Problem

Human developers understand that certain operations require multiple sequential API calls. For example, creating a resource might require:

1.  Calling POST /resources to create the resource
2.  Extracting the resource ID from the response
3.  Calling POST /resources/{id}/configure to set additional properties
4.  Calling GET /resources/{id}/status to verify completion

AI agents cannot inherently understand these multi-stage workflows unless they are explicitly encoded in the tool definition or agent behavior. This creates several design options:

- Consolidate Operations: Design APIs that complete full workflows in a single call
- Explicit Workflow Encoding: Provide tool definitions that describe the required sequence
- Explicit State Handles: Return handles (IDs, tokens, references) that agents pass back on subsequent calls, keeping the transport stateless while preserving workflow continuity (the pattern the MCP stateless core now assumes)
- Declarative Interfaces: Accept desired end-states rather than procedural steps
- Protocol-Level Tasks: For long-running or asynchronous workflows, the MCP Tasks extension provides a standard way for servers to run background work, report progress, and deliver results without the agent polling ad hoc endpoints

> The MCP specification allows tool definitions to include detailed descriptions and parameter schemas that can guide agent behavior, but complex multi-step workflows still require careful design.

### The Context Window Challenge

One of the most significant constraints in AI-native API design is the model's context window. When an API returns large datasets, that data must fit within the model's available context, which directly impacts:

- Cost: Most AI providers charge per token, and large responses dramatically increase inference costs
- Performance: Processing large contexts slows response times
- Accuracy: Models can lose track of information in oversized contexts (the "lost in the middle" problem)

Traditional pagination doesn't solve this problem. An AI agent that receives page 1 of 100 cannot effectively reason about the complete dataset, and fetching all 100 pages would exceed practical context limits.

The stakes here are not theoretical. Cloudflare's "Code Mode" experiment demonstrated token savings above 98% by letting agents discover and call tools dynamically instead of loading every tool definition into context up front. That's a strong signal that context efficiency is a first-order design concern, not a nice-to-have.

### Caching and Inference-Orchestrated Retrieval

The solution requires a fundamental rethinking of data retrieval patterns.

### Server-Side Filtering and Aggregation

- APIs should accept rich query parameters that allow agents to request exactly what they need
- Implement semantic search capabilities so agents can query by meaning rather than exact matches
- Provide aggregation endpoints that return summaries rather than raw data

### Intelligent Caching Strategies

- Use prompt caching to cache frequently accessed data structures (Anthropic exposes explicit cache-control breakpoints; OpenAI caches automatically, so design for both)
- Design APIs to return stable, cacheable responses when possible
- Implement cache keys that agents can reference in subsequent requests

### Streaming Responses

- For large datasets, implement streaming protocols where the API sends data incrementally
- Allow agents to signal when they have sufficient information to proceed
- Use server-sent events (SSE) or WebSocket connections for real-time data feeds

### Reference-Based Patterns

Instead of returning full datasets, return references that the agent can selectively dereference:

```json
{
  "summary": {
    "total_records": 15420,
    "matching_criteria": "status=active AND region=us-west"
  },
  "sample": ["..."],
  "data_reference": "cache://dataset-abc123",
  "query_refinement_suggestions": [
    "Filter by created_date to reduce result set",
    "Group by category for aggregated view"
  ]
}
```

With the protocol-level session removed from MCP's stateless core, this pattern does double duty: the reference is both a context-efficiency mechanism and the workflow-state handle that survives across load-balanced requests.

### MCP Implementation Patterns

The MCP community has developed patterns that address these challenges.

### Resource URIs and Lazy Loading

MCP resources use URI schemes to reference data without immediately loading it into context (the dataset:// scheme below is illustrative, not spec-defined):

```json
{
  "resources": [
    {
      "uri": "dataset://customer-records/query?status=active",
      "name": "Active Customer Records",
      "description": "Filtered dataset of active customers",
      "mimeType": "application/json"
    }
  ]
}
```

The AI model can list available resources and selectively read only those needed for the current task.

### Tool Design for Composability

Well-designed MCP tools expose atomic operations that agents can combine:

```json
{
  "name": "query_database",
  "description": "Execute a SQL query with automatic result summarization",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "SQL query to execute"
      },
      "max_rows": {
        "type": "integer",
        "description": "Maximum rows to return (default: 100)",
        "default": 100
      },
      "summarize": {
        "type": "boolean",
        "description": "Return statistical summary instead of raw rows",
        "default": false
      }
    }
  }
}
```

This tool definition allows the agent to control result size and format based on the task at hand.

### Progressive Disclosure with Explicit Handles

MCP servers can implement progressive disclosure patterns using explicit state handles:

```js
// Initial call
const metadata = await server.callTool("get_dataset_info", {
  dataset_id: "sales_2024"
});
// Returns: { total_rows: 1000000, columns: [...], sample_rows: 10 }

// Follow-up call based on analysis
const aggregated = await server.callTool("aggregate_dataset", {
  dataset_id: "sales_2024",
  group_by: ["region", "product_category"],
  aggregations: ["sum(revenue)", "count(*)"]
});
```

> Note that dataset_id here is exactly the explicit-handle pattern the stateless protocol expects: the server minted an identifier, and the agent carries it forward as an ordinary argument. One important distinction, though: sales_2024 is a natural key — any server instance can resolve it against the underlying database, so it's inherently safe behind a load balancer. The instance-affinity trap bites server-minted ephemeral handles instead: query cursors, cached result sets, pagination tokens, session-scoped browser contexts. Natural keys resolve anywhere; minted ephemeral handles need the shared store.

### Practical Design Guidelines

When building APIs for AI consumption, apply these principles.

### Design for Autonomy

- Self-Describing Responses: Include metadata that helps agents understand the data structure and semantics
- Error Recovery: Provide actionable error messages that agents can use to retry with corrected parameters
- Capability Discovery: Implement endpoints that describe what operations are available (MCP now formalizes this with server/discover, and the proposed MCP Server Cards standard aims to expose server metadata at .well-known URLs so registries and crawlers can discover capabilities without connecting)

### Optimize for Context Efficiency

- Compression: Use efficient data formats and remove unnecessary verbosity
- Selective Fields: Allow clients to specify which fields to return (similar to GraphQL field selection)
- Summary First: Return high-level summaries before detailed data

### Enable Iterative Refinement

- Query Suggestions: When queries return too much data, suggest refinements
- Progressive Queries: Support multi-stage queries where each stage narrows the result set
- Bookmarks: Provide tokens that allow agents to resume interrupted operations

### Implement Intelligent Defaults

- Sensible Limits: Default to returning manageable dataset sizes (e.g., 100 rows, not 1 million)
- Automatic Summarization: When result sets exceed thresholds, automatically switch to summary mode
- Time-Boxing: Implement timeouts that prevent runaway queries

### Design for Stateless Scale from Day One

- Shared State Stores: If your server mints handles (session IDs, dataset references, browser contexts), back them with Redis, S3, a database, or another shared store accessible to all instances
- Avoid In-Process Maps: Local caches and in-memory maps break the moment you add a second server instance
- Resist Sticky Sessions: Load-balancer session affinity is the tempting-but-wrong stopgap — it papers over the bug and reintroduces exactly the affinity the 2026-07-28 revision removed from the protocol layer
- Test Multi-Instance Scenarios Early: Deploy behind a load balancer in development to catch state-affinity bugs before production

> The stateless-handle-with-shared-store pattern is not MCP-specific. It applies to any API designed for horizontal scale. MCP's stateless core simply makes the requirement explicit and unavoidable.

### A Practical Example: api-ai-readiness

The patterns above aren't hypothetical — they came out of building and testing a real tool. The [api-ai-readiness](https://github.com/gaberger/api-ai-readiness) project (published on npm as [api-ai-readiness](https://www.npmjs.com/package/api-ai-readiness)) evaluates how ready an API surface is for agent consumption. It exercises the exact design questions this page raises: capability discovery, context-efficient responses, and explicit state handles.

The tool analyzes OpenAPI specifications across multiple dimensions — endpoint design, error handling, authentication patterns, response structure, and documentation quality — and generates a scored readiness report. It runs both as an MCP server (exposing an assess_api tool) and as a standalone CLI, making it useful for both interactive agent workflows and CI/CD pipelines.

It's also where the "handle is right, store is local" lesson in the callout above was learned firsthand. The tool returns readiness://\<id\> handles pointing at assessment results — a clean stateless-explicit-handle design that worked perfectly as a single process and immediately surfaced the shared-store requirement the moment a second instance entered the picture.

Install and run:

```bash
npx api-ai-readiness analyze https://api.example.com/openapi.json
```

### Related Work and Follow-Ups

api-ai-readiness isn't alone — API-for-agent readiness is becoming its own discipline, and several parallel efforts are worth following up on for comparison:

- Jentic API AI-Readiness Framework (JAIRF): A standards-aligned specification for scoring how interpretable, operable, and trustworthy APIs are for AI systems across six dimensions, with a CLI (@jentic/api-scorecard-cli) that scores any OpenAPI document locally
- API Evangelist's agent-readiness index: A topic collection cataloging the operational signals that make an API safely drivable by an autonomous agent — machine-negotiable auth, idempotency for agent retries, typed errors agents can branch on, explicit rate-limit signaling, and machine entrypoints like /.well-known/api-catalog (RFC 9727)
- MCP Server Cards (discussed above): The protocol-level counterpart — standardized, discoverable server metadata

These frameworks converge on the same conclusion this page argues from the design side: agent-readiness is measurable, and the gaps that break agents — ambiguous errors, prose-only auth, missing idempotency, oversized responses — are exactly the friction human developers have been papering over for years.

### The Road Ahead

The shift to AI-native APIs represents more than an incremental change in interface design. It requires rethinking fundamental assumptions about how systems communicate.

The MCP project's 2026 roadmap organizes development around four priority areas: transport scalability, agent communication, governance maturation, and enterprise readiness. Most enterprise capabilities are expected to land as opt-in extensions rather than core spec changes, keeping the base protocol lean.

### Emerging Trends

- Standardized Capability Discovery: MCP Server Cards and the extensions track are early steps toward common, machine-readable descriptions of what servers can do
- Advanced Caching Protocols: Distributed caching systems optimized for AI workloads
- Semantic APIs: Interfaces that accept natural language queries and return contextually appropriate data
- Cost-Aware Protocols: Rate limiting and cost attribution remain unsolved at the protocol level; emerging agent payment protocols such as x402 and Stripe's efforts address the payment side, but in-organization cost governance for autonomous tool use is still open ground

### Organizational Readiness

The organizations that adapt their API strategies now will be positioned to take full advantage of AI-driven automation. Those that continue designing solely for human consumption risk creating integration bottlenecks that limit their systems' participation in the emerging AI ecosystem.

> Start evaluating your existing APIs through the lens of agent consumption. Identify multi-stage workflows, oversized responses, and implicit assumptions that would confuse an AI system. And design for statelessness from the start: the protocol layer is converging on stateless transports with explicit state handles, so APIs that bake session affinity into their design are already swimming against the current. The transition to AI-native design is not a one-time migration but an ongoing evolution in how we think about system integration.

---

*Originally published on [LinkedIn](https://www.linkedin.com/pulse/delivering-apis-ai-gary-berger-5dbqc/).*
