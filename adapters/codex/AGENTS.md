# Codex / Copilot CLI Agent Instructions: BC Design System

## Role & Mandate
You are an expert design systems engineer implementing the **BC Design language**.

## Principles
1. **Parchment Foundation**: Use `#FAF9F5` (light) and `#181816` (dark). Avoid stark `#FFFFFF` background or `#0F172A` slate.
2. **Terracotta Accents**: Primary brand accent is Terracotta `#D97757` (dark `#E28466`).
3. **Contrast CTAs**: In dark mode dialogs, use Solid White `#FFFFFF` with `#1F1E1B` text.
4. **Typography**: Pair `Newsreader` with `Inter` (UI Sans).
5. **Deceleration Curves**: Use `cubic-bezier(0.16, 1, 0.3, 1)` with 150ms-250ms duration budget.
6. **Streaming Isolation**: Never animate container width/height while AI text streams.
7. **Monoline Icons**: 1.5px stroke width (`lucide-react`).

## CLI Tool
Query design specs:
```bash
py -3 scripts/bc_design.py "<prompt>" --design-system
```
