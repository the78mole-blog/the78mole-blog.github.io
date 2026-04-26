// https://nuxt.com/docs/api/configuration/nuxt-config

// IDs aus .env (lokal) bzw. GitHub-Secrets (CI) – Hinweis: der Env-Var-Name
// enthält einen Tippfehler (GOOFLE statt GOOGLE) – bitte in GitHub Secrets
// genauso hinterlegen wie in .env
const gtagId = process.env.GOOGLE_ANALYTICS_MEAS_ID || 'G-XXXXXXXXXX'
const adsensePubId = process.env.GOOGLE_ADSENSE_PUB_ID
  ? `ca-${process.env.GOOGLE_ADSENSE_PUB_ID}`
  : 'ca-pub-XXXXXXXXXXXXXXXX'

export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss',
    'nuxt-gtag',
  ],

  // Macht adsensePubId zur Laufzeit in allen Komponenten via useRuntimeConfig() verfügbar
  runtimeConfig: {
    public: {
      adsensePubId,
    },
  },

  gtag: {
    id: gtagId,
    // Erst nach Consent aktivieren (DSGVO)
    enabled: false,
  },

  app: {
    head: {
      script: [
        {
          src: `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsensePubId}`,
          async: true,
          crossorigin: 'anonymous',
        },
      ],
    },
  },

  tailwindcss: {
    // Prevents the HMR loop caused by Tailwind watching its own output
    viewer: false,
  },

  content: {
    highlight: {
      theme: 'github-dark',
      langs: [
        'bash', 'c', 'cpp', 'css', 'dockerfile', 'go', 'html',
        'java', 'javascript', 'json', 'makefile', 'markdown',
        'python', 'rust', 'shell', 'sql', 'toml', 'typescript',
        'vim', 'xml', 'yaml',
      ],
    },
  },

  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
})
