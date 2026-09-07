/**
 * BC Design System - Tailwind CSS Configuration Preset
 * Usage: Paste into tailwind.config.js `theme.extend`
 */

module.exports = {
  theme: {
    extend: {
      colors: {
        bc: {
          bg: 'var(--bc-bg, #FAF9F5)',
          'bg-subtle': 'var(--bc-bg-subtle, #F4F3EE)',
          'bg-muted': 'var(--bc-bg-muted, #ECEAE2)',
          surface: 'var(--bc-surface, #FFFFFF)',
          'surface-hover': 'var(--bc-surface-hover, #FDFCF9)',
          
          /* Accent Terracotta */
          accent: 'var(--bc-accent, #D97757)',
          'accent-hover': 'var(--bc-accent-hover, #C15F3E)',
          'accent-active': 'var(--bc-accent-active, #AA4F32)',
          'accent-subtle': 'var(--bc-accent-subtle, #FDF3EE)',
          'accent-border': 'var(--bc-accent-border, #F4D3C5)',
          
          /* Secondary */
          amber: 'var(--bc-amber, #E09F3E)',
          olive: 'var(--bc-olive, #7D8A68)',

          /* Ink & Text */
          text: 'var(--bc-text-primary, #1F1E1B)',
          muted: 'var(--bc-text-secondary, #6B6760)',
          subtle: 'var(--bc-text-tertiary, #99948B)',
          
          /* Border */
          border: 'var(--bc-border, rgba(31, 30, 27, 0.08))',
          'border-strong': 'var(--bc-border-strong, rgba(31, 30, 27, 0.16))',
        }
      },
      fontFamily: {
        serif: [
          'var(--font-serif)',
          'Newsreader',
          'Georgia',
          'serif',
        ],
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'Fira Code',
          'ui-monospace',
          'monospace',
        ],
      },
      borderRadius: {
        'bc-sm': '6px',
        'bc-md': '10px',
        'bc-lg': '14px',
        'bc-xl': '20px',
      },
      boxShadow: {
        'bc-sm': '0 1px 2px rgba(31, 30, 27, 0.04)',
        'bc-md': '0 4px 16px -2px rgba(31, 30, 27, 0.06), 0 2px 6px -1px rgba(31, 30, 27, 0.03)',
        'bc-lg': '0 12px 32px -4px rgba(31, 30, 27, 0.08), 0 4px 12px -2px rgba(31, 30, 27, 0.04)',
        'bc-float': '0 20px 48px -8px rgba(31, 30, 27, 0.12)',
      },
      transitionTimingFunction: {
        'bc-ease': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'bc-bounce': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      animation: {
        'bc-fade-up': 'bcFadeUp 250ms cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'bc-drawer-in': 'bcDrawerIn 400ms cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'bc-thinking': 'bcThinkingPulse var(--bc-duration-shimmer) infinite var(--bc-ease-in-out)',
        'bc-scale-in': 'bcScaleIn 150ms cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
    }
  }
};
