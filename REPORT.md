# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question 1: "What is the agentic loop?"**

```
The agentic loop is the core iterative process that autonomous AI agents use to accomplish
tasks. It's a continuous cycle of:

The Basic Loop

 1 Perceive — Gather information from the environment (observations, user input, tool outputs,
   etc.)
 2 Think/Reason — Process the information, plan next steps, make decisions
 3 Act — Execute actions (call tools, send messages, modify files, etc.)
 4 Repeat — Observe the results and continue the loop until the goal is achieved

Why It Matters

Unlike a simple query-response model, the agentic loop enables:

 • Autonomy — Agents can work independently toward goals
 • Adaptation — Agents adjust based on feedback and changing conditions
 • Multi-step reasoning — Complex tasks are broken into sequential actions
 • Self-correction — Agents can detect errors and try alternative approaches

Example

For a task like "research and summarize recent AI news":

 1 Perceive: Understand the request
 2 Think: Plan to search for news, then summarize
 3 Act: Call web_search tool
 4 Perceive: Get search results
 5 Think: Evaluate results, plan to fetch top articles
 6 Act: Call web_fetch on selected URLs
 7 Think: Synthesize information
 8 Act: Deliver summary to user

This loop continues until the task is complete or the agent determines it cannot proceed.
```

**Question 2: "What labs are available in our LMS?"**

```
Based on the LMS (Lab Management System) in this workspace, here are the available labs:

Lab 8 — The Agent is the Interface

This is the current lab in your workspace. It focuses on building an AI agent as a
natural-language interface for an LMS system.

Required Tasks:

 1 Task 1 — Set Up the Agent (install nanobot, configure Qwen API, add MCP tools, write skill
   prompt)
 2 Task 2 — Deploy and Connect a Web Client (Dockerize nanobot, add WebSocket channel +
   Flutter chat UI)
 3 Task 3 — Give the Agent New Eyes (explore observability data, write log/trace MCP tools)
 4 Task 4 — Diagnose a Failure and Make the Agent Proactive (investigate failure, schedule
   health checks, fix a planted bug)
 5 Task 5 — (additional required task)

Optional Tasks:

 1 Task 1 — Add a Telegram Bot Client (same agent, different interface)
```

Note: The agent doesn't know about the actual LMS backend data yet — it's reading from the workspace files. This is expected for Part A (no MCP tools configured).

## Task 1B — Agent with LMS tools

**Question 1: "What labs are available?"**

```
Here are all the labs available in your LMS:

                                                        
 Lab ID  Title                                          
 ────────────────────────────────────────────────────── 
 Lab 01  Products, Architecture & Roles                 
 Lab 02  Run, Fix, and Deploy a Backend Service         
 Lab 03  Backend API: Explore, Debug, Implement, Deploy 
 Lab 04  Testing, Front-end, and AI Agents              
 Lab 05  Data Pipeline and Analytics Dashboard          
 Lab 06  Build Your Own Agent                           
 Lab 07  Build a Client with an AI Coding Agent         
 Lab 08  lab-08 (The Agent is the Interface)            
                                                        

You have 8 labs total. Lab 08 is the one currently in your workspace (/root/se-toolkit-lab-8).
```

**Question 2: "Describe the architecture of the LMS system"**

The agent provided a detailed architecture description including:

- **7 Docker containers**: Caddy (reverse proxy), FastAPI backend, PostgreSQL, pgAdmin, Nanobot, Telegram Bot
- **High-level flow**: Student → Caddy (:42002) → FastAPI (:8000) → PostgreSQL
- **AI agent flow**: User → Nanobot (WS :8765) → MCP Tools → FastAPI → PostgreSQL
- **Data model**: OBER-based with Item, Learner, and Interacts tables
- **Key design decisions**: Monolith with layered structure, Caddy reverse proxy, SQLModel ORM, async database access

**Bonus: "Which lab has the lowest pass rate?"**

```
Based on the pass rate data, Lab 02 — Run, Fix, and Deploy a Backend Service has the lowest
overall pass rate.

Pass Rate Summary by Lab

 Lab     Avg Score  Tasks              
 ───────────────────────────────────── 
 Lab 01  51.4%      8 tasks            
 Lab 02  48.3% ⚠️   6 tasks            
 Lab 03  53.6%      5 tasks            
 Lab 04  55.9%      4 tasks            
 Lab 05  67.3%      4 tasks            
 Lab 06  59.3%      3 tasks            
 Lab 07  67.3%      4 tasks            
 Lab 08  N/A        No submissions yet

Lab 02 Breakdown

The low pass rate is largely due to one particularly challenging task:

                                                                     
 Task                                            Avg Score  Attempts 
 ─────────────────────────────────────────────────────────────────── 
 Optional 2: Make your VM a proxy                0.0%       3        
 Optional 1: Implement the /outcomes endpoint    36.4%      11       
 Task 4: Deploy the web server to the VM         56.2%      84       
 Task 1: Run the web server                      67.9%      210      
 Task 2: Identify, report, and fix a bug         66.7%      216      
 Optional 3: Implement the post-order traversal  62.5%      6
```

The agent correctly called multiple MCP tools (`lms_labs`, `lms_pass_rates`) and analyzed the data to provide insights.

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

The agent now handles ambiguous queries much better. Instead of guessing or hallucinating, it:

1. First gathered comprehensive data using multiple MCP tools
2. Presented completion rates for all labs
3. Showed average scores by lab and task
4. Provided key insights

**Response excerpt:**

```
📊 LMS Lab Scores Overview

Completion Rates (Passed / Total Students)

 Lab     Title                                           Completion Rate  Passed  Total 
 ────────────────────────────────────────────────────────────────────────────────────── 
 Lab 01  Products, Architecture & Roles                  100.0% ✅        258     258   
 Lab 02  Run, Fix, and Deploy a Backend Service          89.1%            131     147   
 Lab 03  Backend API: Explore, Debug, Implement, Deploy  89.1%            156     175   
 Lab 04  Testing, Front-end, and AI Agents               96.7%            238     246   
 Lab 05  Data Pipeline and Analytics Dashboard           98.4%            246     250   
 Lab 06  Build Your Own Agent                            98.4%            241     245   
 Lab 07  Build a Client with an AI Coding Agent          99.6% ✅         236     237   
 Lab 08  The Agent is the Interface                      0.0%             0       0     

📈 Key Insights

 Metric                   Value                      
 ─────────────────────────────────────────────────── 
 Highest Completion Rate  Lab 07 (99.6%)             
 Lowest Completion Rate   Lab 02 & Lab 03 (89.1%)    
 Highest Avg Task Score   Lab 05 - Task 3 (74.1%)    
 Lowest Avg Task Score    Lab 02 - Optional 2 (0.0%) 
 Most Attempted Task      Lab 01 - Lab setup (3,149) 
```

**Skill prompt location:** `nanobot/workspace/skills/lms/SKILL.md`

The skill prompt teaches the agent:
- Which `lms_*` tools are available and when to use each
- To ask for clarification when a lab parameter is needed but not provided
- To format numeric results nicely (percentages, counts)
- To keep responses concise but informative
- To explain its current tools and limits when asked "what can you do?"

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
