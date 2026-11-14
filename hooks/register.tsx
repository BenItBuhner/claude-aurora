import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { SCENE } from './scene.ts'

// Deep polar night with faint green/teal/violet curtains drifting near the top.
const { theme, problems } = makeColors({
  label: 'Aurora',
  only: 'dark',
  roles: { accent: '#4fd1a5', danger: '#e0607a', success: '#6fd88a', warning: '#e0b55a', pro: '#a58cf0' },
  dark: {
    gray: {
      anchors: {
        'surface-0': '#0a131a',
        'surface-1': '#111a22',
        'surface-2': '#16212b',
        'surface-3': '#1b2733',
        'text-primary': '#e6f0f2',
        'text-secondary': '#b9c8cd',
        'text-muted': '#8fa3aa',
      },
    },
  },
})

const LOOK: ThemeSetArgs = {
  colors: theme,
  // A still picture drawn as a scene so the panels become see-through over it.
  // Nothing animates and the frosting blur is off, so there is no per-frame cost.
  backdrop: { scene: 'aurora', glass: { blur: 0, tint: '#0a131a', opacity: 0.4 } },
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const unpainted = problems.find(line => line.startsWith("Desktop won't paint"))
    if (unpainted !== undefined) $.ui.toast(unpainted)
    try {
      const set = await $.theme.set(LOOK)
      if (!set.isDrawn) $.ui.status(set.reason)
    } catch {
      // Headless sessions (claude -p, SDK) have no surface to theme.
    }
    return next(e)
  })

  on('ui.render', { component: 'Backdrop' }, ($, e, next) => {
    if (e.surface !== 'desktop' && e.surface !== 'mobile') return next(e)
    const { Svg } = $.ui.resolve(e)
    return <Svg source={SCENE} alt="A green aurora arcing across a starry night sky" />
  })
}
