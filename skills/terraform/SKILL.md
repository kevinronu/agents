---
name: terraform
description: Enforce strict guardrails for implementing and validating Terraform changes. Use when Codex writes, modifies, reviews, formats, scopes, initializes, validates, or plans Terraform configuration, modules, variables, outputs, tfvars, providers, backends, or infrastructure code, including deriving the affected Terraform module scope from changed files before running commands.
---

# Terraform

## Purpose

Act as a Terraform implementation guard. Apply these rules to all infrastructure changes, then initialize, format, validate, and optionally plan only within the derived change scope unless escalation rules require a broader scope.

## Change Scope

Derive Terraform command scope from the current change set before running Terraform commands.

1. Identify modified files with `git diff --name-only <base>...HEAD` or the equivalent base for the current task.
2. Treat `*.tf` and `*.tfvars` files as Terraform-relevant changes.
3. Resolve each changed Terraform file to its owning module.
4. For root modules, use the nearest ancestor directory containing `backend.tf`.
5. For reusable modules under `terraform/modules/*`, use the module directory as the ownership unit.
6. Escalate scope when a change affects reusable modules, public module interfaces, variables consumed across environments, outputs consumed externally, providers, backends, state assumptions, cross-boundary contracts, or linked functional/contract tests.
7. Include directly dependent root modules and linked tests when a reusable module or cross-boundary interface changes.
8. Escalate to full repository scope only when the change invalidates global infrastructure assumptions or the user explicitly requests full-repo validation.

Report the scoped root modules or reusable modules, any escalations, and assumptions when scope is non-obvious.

## Change Rules

- Apply changes only within the derived change scope.
- Expand scope only when escalation conditions require it.
- Do not modify unrelated resources, modules, variables, outputs, providers, backends, or configurations.
- Keep changes minimal and focused.

## Code Rules

### Scope and Changes

- Do not refactor unrelated infrastructure.
- Do not introduce new providers, backends, or modules unless explicitly requested.
- Preserve resource names and addresses unless a change is required.
- Prefer additive changes over replacements when possible.

### State and Safety

- Never modify Terraform state directly unless explicitly instructed.
- Do not perform destructive changes without explicitly calling them out.
- Identify any likely resource replacement, deletion, recreation, or state migration risk.
- Avoid commands that mutate real infrastructure unless the user explicitly requests them.

## Architecture Rules

- Use modules to encapsulate reusable infrastructure concerns.
- Reuse existing modules when they already solve the problem.
- Introduce new modules only when no suitable module exists.
- When modifying existing infrastructure, request confirmation before restructuring modules.
- Preserve existing module boundaries and resource ownership.

## Variables and Outputs

- Use variables for configurable inputs.
- Avoid hardcoded environment-specific values.
- Define types and validation for variables when possible.
- Use `validation` blocks for input constraints.
- Use `precondition` and `postcondition` blocks when resource correctness depends on assumptions.
- Expose outputs only when they are consumed externally.
- Preserve output names and meanings unless a breaking change is explicitly required.

## Validation Rules

- Ensure formatting is consistent with `terraform fmt`.
- Ensure configuration is syntactically valid with `terraform validate`.
- Ensure no unintended resource replacements are introduced.
- Explicitly identify destructive changes in any plan output.
- Validate every affected root module after initialization.

## Execution Contract

A Terraform task is complete only when all steps succeed in this order:

1. Initialize each root module in the derived change scope with `terraform init --backend=false`.
2. Format only within the derived change scope with `terraform fmt -recursive`.
3. Validate each initialized root module in the derived change scope with `terraform validate`.
4. Run `terraform plan` only when required by the task or workflow, and only within the derived change scope.

For reusable module changes, run formatting in the module scope and validate all directly dependent root modules required by scope escalation.

Do not run repository-wide Terraform commands unless the user explicitly requests them or scope escalation reaches full-repository impact.

If any step fails, fix the issue and rerun the sequence from the appropriate failed step until scoped validation succeeds or a blocker is clearly reported.

## Required Closeout

When finishing a Terraform task, report:

- Files created or updated.
- Scoped root modules or reusable modules validated.
- Commands run and outcomes.
- Any assumptions, skipped validation, plan requirements, or destructive-change risks with the reason.
