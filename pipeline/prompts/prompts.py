"""All LLM prompt templates for the code-to-spec pipeline."""

ANALYZE_UNIT_PROMPT = """You are a meticulous code analyst. You report only what the source proves and \
never guess to fill gaps. Your output is the ground-truth record everything downstream is built on, so \
accuracy matters more than completeness — it is better to say less than to invent.

Unit path: {path}
Language: {language}

Extracted structure (deterministic — this is the authoritative list of what exists in this file):
{structure}

Source code:
{source}

GROUNDING RULES (critical):
- Describe ONLY what is present in the source above. Do not invent functions, classes, parameters, return \
values, exceptions, dependencies, or behavior that the code does not show.
- The interfaces you list must correspond to the functions/classes in the deterministic structure and \
source. Do not add interfaces that aren't there, and do not omit ones that are.
- Derive inputs, outputs, raises, and side_effects from the actual code body, not from what the names \
suggest. If you cannot tell from the source, leave that field as an empty array rather than guessing.
- For internal_deps / external_deps, list only modules/packages actually imported or referenced in the source.
- If a field has nothing to report, use an empty array. Do not pad.

Respond with ONLY a JSON object (no prose, no markdown fences) matching this schema:
{{
  "purpose": "one sentence describing what this unit does and why it exists",
  "interfaces": [
    {{
      "name": "...",
      "signature": "...",
      "kind": "function|class|method|endpoint",
      "inputs": ["param: type description"],
      "outputs": ["return type description"],
      "raises": ["ExceptionType: when"],
      "side_effects": ["observable effect outside the function: I/O, mutation, network, global state"],
      "intent": "WHAT this does and WHY, not HOW"
    }}
  ],
  "internal_deps": ["relative/path/to/dep"],
  "external_deps": ["package_name"],
  "idioms": ["language-specific pattern actually used here: why it matters for reimplementation"],
  "behavioral_notes": ["non-obvious behavior visible in the code that a reimplementer needs to know"]
}}

EXAMPLE — for this source:
    def slugify(text: str) -> str:
        return text.strip().lower().replace(" ", "-")

CORRECT output (every field traces back to the code):
{{
  "purpose": "Convert a string into a URL-safe slug.",
  "interfaces": [
    {{
      "name": "slugify",
      "signature": "slugify(text: str) -> str",
      "kind": "function",
      "inputs": ["text: str — the string to convert"],
      "outputs": ["str — lowercased, hyphen-separated form of the input"],
      "raises": [],
      "side_effects": [],
      "intent": "Normalise arbitrary text into a slug usable in URLs."
    }}
  ],
  "internal_deps": [],
  "external_deps": [],
  "idioms": [],
  "behavioral_notes": ["Whitespace is stripped before lowercasing; spaces become hyphens."]
}}

WRONG output (rejected — invents things the source never shows):
{{
  "interfaces": [
    {{"name": "slugify", "inputs": ["text: str", "max_length: int — truncate to length"], \
"raises": ["ValueError: when text is empty"], "side_effects": ["writes to a cache"]}}
  ]
}}
Here max_length, the ValueError, and the cache write appear nowhere in the source. Never add fields the \
code does not contain — use empty arrays instead."""

REDUCE_MODULES_PROMPT = """You are a precise technical summariser who reports only what the units state. \
Summarise the responsibility of the module/directory '{module_name}' using ONLY \
the unit analyses below. Stay grounded — do not invent classes, layers, frameworks, or behavior that the \
units do not describe.

Units:
{units_json}

Write 1-3 plain sentences describing what this module actually does, based strictly on the purposes and \
interfaces listed. If there is only one small file, describe just that file's job. Do not pad, do not \
speculate about architecture, do not name patterns that aren't evidenced.

Respond with JSON:
{{
  "responsibility": "1-3 grounded sentences on what this module does"
}}"""

SYNTHESIZE_SYSTEM_PROMPT = """You are a precise technical writer. Write a clear, high-level overview of \
the codebase '{repo_name}' — what it is, what it does, and HOW IT WORKS — using ONLY the facts below. \
This is grounding-critical: describe the real system, but do not invent anything.

Languages: {languages}

Entry points (where execution starts):
{entry_points}

Modules (each with its responsibility, public surface, and collaborators):
{modules_json}

Write the overview with these three parts (use the headings):

### Overview
2-4 sentences: what this project is and the problem it solves, based on the modules' responsibilities.

### How It Works
A grounded walkthrough of the main flow: start at the entry point(s) and trace how control/data moves \
between modules, using ONLY the stated collaborators to justify each step. Describe the primary path the \
system takes to do its job. If there are distinct flows (e.g. a main pipeline and a separate CLI/chat \
path), describe each briefly. Prefer a short ordered list of steps over prose where it's clearer.

### Key Components
A bullet per major module: its name and the role it plays in the system, drawn from its responsibility \
and public surface.

GROUNDING RULES:
- Use ONLY the responsibilities, public surfaces, collaborators, and entry points provided. Do not invent \
data flows, layers, services, or steps that the collaborators do not support.
- Do not name architectural patterns (layered, hexagonal, MVC, microservices, etc.) or frameworks unless \
they are explicitly evidenced in the responsibilities. Describe what the modules actually do instead.
- Ground every step in "How It Works" in a stated collaborator relationship or entry point; if a \
connection isn't supported by the data, don't assert it.
- If the project is small or trivial, keep it proportionally short. Plain language, no marketing tone. \
Aim for 200-450 words."""

EXTRACT_ARCHITECTURE_PROMPT = """You are a careful architecture extractor who records only structures the \
summaries actually describe. From the module summaries and the unit-level evidence, extract:
1. Data schemas (language-neutral)
2. Cross-cutting concerns

Modules:
{modules_json}

Unit-level evidence (deterministic — gathered from the per-unit analyses; use this to ground the \
cross-cutting concerns, since the module summaries omit this detail):
{evidence}

GROUNDING RULES (critical):
- Extract ONLY what is evidenced in the module summaries or the unit-level evidence above. Do not invent \
schemas, fields, services, auth mechanisms, or concurrency models that neither source mentions.
- Use the unit-level evidence to describe error handling, logging, concurrency, and config concretely \
(cite what the evidence shows). If the evidence for a concern is empty, leave that field empty — do not \
fill gaps with best-practice assumptions.
- external_integrations means EXTERNAL RUNTIME SERVICES the system talks to — databases, HTTP/REST APIs, \
LLM endpoints, message queues, cloud services. Infer the SERVICE behind a client library when clear \
(e.g. a postgres driver → "PostgreSQL", langchain-openai → "OpenAI API", an Ollama client → "Ollama"). \
Do NOT list libraries, frameworks, or language standard-library modules as integrations — those belong \
in external_libraries, not here. If no external service is evidenced, return an empty array.
- Data schemas should reflect structures the modules actually describe, not ones you expect a project \
like this to have.

Respond with JSON:
{{
  "data_schemas": [
    {{"name": "...", "description": "...", "json_schema": {{...}} }}
  ],
  "cross_cutting": {{
    "error_handling": "how errors flow through the system",
    "config": "how configuration is managed",
    "logging": "logging approach",
    "auth": "authentication/authorization approach",
    "concurrency": "threading/async model",
    "external_integrations": ["ServiceName: how it's used (a runtime service, NOT a library)"]
  }}
}}"""

GENERATE_TESTS_PROMPT = """You are a careful test designer who writes tests only for behavior the interfaces \
actually specify. Generate behavioral acceptance tests for these interfaces. Tests must be language-neutral (given/when/then).

Interfaces:
{interfaces_json}

GROUNDING RULES (critical):
- Write tests ONLY for the interfaces listed above, and base each test on that interface's stated inputs, \
outputs, raises, and side effects. Do not invent behavior, parameters, return values, or error cases that \
the interface does not describe.
- target_interface must name one of the interfaces given. Do not test interfaces that aren't listed.
- If an interface is too vaguely described to test meaningfully, skip it rather than fabricating a scenario.

Respond with JSON array:
[
  {{
    "target_interface": "ModuleName.functionName",
    "given": "preconditions and initial state",
    "when": "action taken / input provided",
    "then": "expected outcome / postconditions"
  }}
]"""

VALIDATE_PROMPT = """You are a critic reviewing a reimplementation spec document.

Known public interfaces from analysis:
{known_interfaces}

Spec document:
{document}

Check:
1. Every public interface listed is documented in the spec
2. Every internal dependency relationship is explained
3. Every external dependency is noted
4. Cross-cutting concerns are covered
5. Acceptance tests exist for each major interface

Respond with JSON:
{{
  "passed": true/false,
  "gaps": ["specific gap description — include interface name or module"]
}}"""

CHAT_PROMPT = """You are a helpful code assistant answering questions about a specific codebase and the \
reimplementation spec generated for it. Use the retrieved context below — it is a set of excerpts (spec \
sections, per-class specs, and raw source). Synthesise across the excerpts to give a clear, direct answer; \
you may reasonably connect and summarise information that is spread across several excerpts.

Retrieved context (each block is labelled with its source):
{context}

Question: {question}

Guidelines:
- Answer based on the context. It is normal for the answer to require piecing together several excerpts — \
do that rather than refusing.
- Be concrete and cite the sources you used (file paths or spec section names).
- Only if NONE of the excerpts are relevant to the question should you say you don't have enough indexed \
material; otherwise give the best answer the context supports, even if partial."""

REVIEW_COMPLETENESS_PROMPT = """You are a completeness reviewer for code analysis. Decide whether each \
unit's captured analysis FULLY describes its behavior, and if not, ask specific questions the next \
analysis pass must answer.

For each unit you are given: its path, its captured purpose/interfaces, and the raw structure that \
tree-sitter found in the file (function and class names that actually exist).

Units:
{units_json}

For each unit, check:
- Are all functions/classes that tree-sitter found captured as interfaces? (missing ones are gaps)
- Does each interface have a meaningful intent, inputs, outputs, and error/side-effect notes — or are they empty/vague?
- Is the purpose specific, or generic boilerplate?

Respond with JSON. Only include units that need another pass; if everything is well captured, return an empty object.
{{
  "questions": {{
    "<unit_id>": [
      "specific question the next pass must answer, e.g. 'document the side effects of method X'",
      "..."
    ]
  }}
}}

Ask only concrete, answerable questions grounded in the actual structure. Do not invent functions that \
tree-sitter did not find."""

REVIEW_PROMPT = """You are a strict fact-checking reviewer. Your ONLY job is to catch hallucinations and \
inconsistencies: claims in the spec document that are NOT supported by the deterministic, ground-truth \
analysis below. Be skeptical. The small model that wrote the spec tends to invent plausible-sounding \
architecture (layers, classes, endpoints, return values) that does not exist in the actual code.

GROUND TRUTH — the complete set of real facts, by category: file_count, every referenceable file \
(all_files), dependency_manifests, modules, data schemas, cross_cutting concerns, every interface (with \
its intent / outputs / raises), and external dependencies that actually exist:
{ground_truth}

SPEC DOCUMENT under review:
{document}

A claim is GROUNDED (do NOT flag it) if it is supported anywhere in the ground truth — match by file path, \
module name, or symbol name ignoring formatting (e.g. 'module.func' vs 'path::func', or a bare class name), \
and treat an interface's intent/outputs/raises as support for behavioural statements and acceptance tests \
about it. The cross_cutting block supports statements about error handling, logging, concurrency, auth, and \
config. Only flag something when it genuinely does not appear anywhere in the ground truth.

Compare the document against the ground truth and report:
1. HALLUCINATIONS — any class, function, interface, endpoint, data field, return value, dependency, or \
architectural component asserted in the document that does NOT appear in the ground truth.
2. CONTRADICTIONS — any statement that conflicts with the ground truth (e.g. wrong return type, wrong \
signature, invented behavior).
3. UNSUPPORTED SPECIFICS — overly specific claims (exact return values, concrete schemas, named services) \
that the ground truth does not justify.

NEVER flag any of the following — these are not hallucinations:
- Section headings, labels, or table-of-contents lines (e.g. "Given/When/Then Tests").
- Statements that something is ABSENT or unknown (e.g. "auth not specified", "no specific idioms", "none").
- File counts, line counts, or inventory figures (these come from a deterministic scan).
- Reasonable generic guidance (e.g. "implement logging").
Only flag concrete factual assertions about THIS codebase that are unsupported by the ground truth.

Respond with JSON:
{{
  "passed": true/false,
  "findings": [
    "HALLUCINATION: <quote or paraphrase the unsupported claim> — not present in ground truth",
    "CONTRADICTION: <claim> conflicts with <ground-truth fact>"
  ]
}}

Set "passed" to true only if there are zero hallucinations or contradictions."""

ASSEMBLE_PROMPT = """Assemble a complete reimplementation spec document from the following analysis results.

GROUNDING RULES (critical):
- Use ONLY the facts provided below. Do not invent classes, methods, return values, layers, frameworks, \
databases, or architecture that the analysis does not contain.
- Be precise and terse — no padding, no marketing tone. If a section has little data, keep it short and \
say so plainly rather than inventing detail to fill space.
- Prefer concrete facts from the analysis over generic best-practice prose.

{prior_lessons}

{gaps_guidance}

## Inventory
{inventory}

## System Overview
{system_overview}

## Module Summaries
{modules_json}

## Data Schemas
{schemas_json}

## Cross-Cutting Concerns
{cross_cutting_json}

## Behavioral Tests
{tests_json}

Write the spec following this structure:
1. Inventory — file tree summary, languages, dependencies, entry points
2. Architecture — components, data flow, module boundaries
3. Behavioral Spec — per module: intent, interfaces, side effects, errors
4. Contracts — data schemas (neutral types), API surfaces, invariants
5. Cross-Cutting — error handling, config, logging, auth, concurrency, integrations
6. Reimplementation Notes — flagged idioms and idiomatic-equivalent guidance
7. Acceptance Tests — given/when/then tests as build criteria"""
