# Aurora

A dark theme for the Claude desktop app: a green aurora curtain fading into violet over a starry night sky, behind see-through panels.

The background is a still vector drawing with no animation, so it doesn't slow the app down. It only draws in the desktop and mobile apps; the terminal and editor extensions ignore it.

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install aurora --marketplace BenItBuhner/claude-aurora
```

Answer `y` to add the marketplace, then pick a scope (Enter for user scope).

From a shell:

```bash
claude plugin install aurora --marketplace BenItBuhner/claude-aurora
```

In the desktop app, where `/plugin` doesn't run: click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `BenItBuhner/claude-aurora`, then **Add plugin**.

## Customizing

- `hooks/register.tsx` holds the theme colors and the panel tint and opacity (`glass`).
- `aurora-vector.py` generates `hooks/scene.ts`, the background drawing. Edit the curves or colors there and rerun it:
  `python aurora-vector.py aurora.svg preview.html`, then rebuild `scene.ts` from `aurora.svg`.
