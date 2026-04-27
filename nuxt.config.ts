// https://nuxt.com/docs/api/configuration/nuxt-config

// IDs aus .env (lokal) bzw. GitHub-Secrets (CI) – Hinweis: der Env-Var-Name
// enthält einen Tippfehler (GOOFLE statt GOOGLE) – bitte in GitHub Secrets
// genauso hinterlegen wie in .env
const gtagId = process.env.GOOGLE_ANALYTICS_MEAS_ID || 'G-XXXXXXXXXX'
const adsensePubId = process.env.GOOGLE_ADSENSE_PUB_ID
  ? `ca-${process.env.GOOGLE_ADSENSE_PUB_ID}`
  : 'ca-pub-XXXXXXXXXXXXXXXX'

// giscus – IDs aus .env (lokal) bzw. GitHub Vars (CI)
// Zu ermitteln auf https://giscus.app/de nach Eingabe des Repos
const giscusRepoId = process.env.GISCUS_REPO_ID || 'TODO'
const giscusCategoryId = process.env.GISCUS_CATEGORY_ID || 'TODO'

export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss',
    'nuxt-gtag',
  ],

  // Macht adsensePubId und Slot-IDs zur Laufzeit in allen Komponenten via useRuntimeConfig() verfügbar
  // Slot-IDs sind öffentlich und werden fest eingecheckt (kein Secret)
  runtimeConfig: {
    public: {
      adsensePubId,
      adsenseSlots: {
        left:      '3478648998', // the78mole-content-left
        right:     '9230728617', // the78mole-content-right
        bottom:    '8012270852', // the78mole-content-bottom
        inArticle: '5913240643', // the78mole-content-inarticle
      },
      giscus: {
        repo:       'the78mole-blog/the78mole-blog.github.io',
        repoId:     giscusRepoId,
        category:   'Blog Comments',
        categoryId: giscusCategoryId,
      },
    },
  },

  gtag: {
    id: gtagId,
    // Erst nach Consent aktivieren (DSGVO)
    enabled: false,
  },

  app: {
    head: {
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
      script: [
        {
          src: `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsensePubId}`,
          async: true,
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

  // Redirects von alten WordPress-Permalinks (/:slug) auf neue Nuxt-Routen
  // GitHub Pages hat keinen Server – Nuxt generiert statische Meta-Refresh-Seiten
  routeRules: {
    // --- Seiten ---
    '/about':                     { redirect: '/pages/about' },
    '/about/':                    { redirect: '/pages/about' },
    '/contact':                   { redirect: '/pages/contact' },
    '/contact/':                  { redirect: '/pages/contact' },
    '/links':                     { redirect: '/pages/links' },
    '/links/':                    { redirect: '/pages/links' },
    '/projects':                  { redirect: '/pages/projects' },
    '/projects/':                 { redirect: '/pages/projects' },
    '/tutorials':                 { redirect: '/pages/tutorials' },
    '/tutorials/':                { redirect: '/pages/tutorials' },
    '/impressum':                 { redirect: '/pages/impressum' },
    '/impressum/':                { redirect: '/pages/impressum' },
    '/datenschutzerklaerung':     { redirect: '/pages/datenschutzerklaerung' },
    '/datenschutzerklaerung/':    { redirect: '/pages/datenschutzerklaerung' },
    '/projects/km271-wifi-howto':  { redirect: '/pages/km271-wifi-howto' },
    '/projects/km271-wifi-howto/': { redirect: '/pages/km271-wifi-howto' },

    // --- Blog-Posts ---
    '/angular-web-app-on-esp32':                          { redirect: '/blog/2021/angular-web-app-on-esp32' },
    '/angular-web-app-on-esp32/':                         { redirect: '/blog/2021/angular-web-app-on-esp32' },
    '/atlassian-and-new-ssl-certificates':                { redirect: '/blog/2018/atlassian-and-new-ssl-certificates' },
    '/atlassian-and-new-ssl-certificates/':               { redirect: '/blog/2018/atlassian-and-new-ssl-certificates' },
    '/code-red-on-fire-or-heat-metering-with-node-red':   { redirect: '/blog/2023/code-red-on-fire-or-heat-metering-with-node-red' },
    '/code-red-on-fire-or-heat-metering-with-node-red/':  { redirect: '/blog/2023/code-red-on-fire-or-heat-metering-with-node-red' },
    '/compile-ceph-mimic-on-arm-32-bit':                  { redirect: '/blog/2019/compile-ceph-mimic-on-arm-32-bit' },
    '/compile-ceph-mimic-on-arm-32-bit/':                 { redirect: '/blog/2019/compile-ceph-mimic-on-arm-32-bit' },
    '/compiling-software-on-ram-limited-multi-core-systems':  { redirect: '/blog/2019/compiling-software-on-ram-limited-multi-core-systems' },
    '/compiling-software-on-ram-limited-multi-core-systems/': { redirect: '/blog/2019/compiling-software-on-ram-limited-multi-core-systems' },
    '/crying-on-open-waters-a-piece-of-hw-for-ahoydtu-and-reading-the-hoymiles-inverters':   { redirect: '/blog/2023/crying-on-open-waters-a-piece-of-hw-for-ahoydtu-and-reading-the-hoymiles-inverters' },
    '/crying-on-open-waters-a-piece-of-hw-for-ahoydtu-and-reading-the-hoymiles-inverters/':  { redirect: '/blog/2023/crying-on-open-waters-a-piece-of-hw-for-ahoydtu-and-reading-the-hoymiles-inverters' },
    '/digging':                   { redirect: '/blog/2018/digging' },
    '/digging/':                  { redirect: '/blog/2018/digging' },
    '/doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data':   { redirect: '/blog/2023/doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data' },
    '/doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data/':  { redirect: '/blog/2023/doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data' },
    '/doxygen-tips-and-tricks':   { redirect: '/blog/2020/doxygen-tips-and-tricks' },
    '/doxygen-tips-and-tricks/':  { redirect: '/blog/2020/doxygen-tips-and-tricks' },
    '/eex-epex-spot-and-the-real-net-intransparency':   { redirect: '/blog/2021/eex-epex-spot-and-the-real-net-intransparency' },
    '/eex-epex-spot-and-the-real-net-intransparency/':  { redirect: '/blog/2021/eex-epex-spot-and-the-real-net-intransparency' },
    '/esp32-evb-and-platform-io-yet-another-esp32-tutorial':   { redirect: '/blog/2020/esp32-evb-and-platform-io-yet-another-esp32-tutorial' },
    '/esp32-evb-and-platform-io-yet-another-esp32-tutorial/':  { redirect: '/blog/2020/esp32-evb-and-platform-io-yet-another-esp32-tutorial' },
    '/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial':   { redirect: '/blog/2021/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial' },
    '/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial/':  { redirect: '/blog/2021/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial' },
    '/freertos-debugging-on-stm32-cpu-usage':   { redirect: '/blog/2020/freertos-debugging-on-stm32-cpu-usage' },
    '/freertos-debugging-on-stm32-cpu-usage/':  { redirect: '/blog/2020/freertos-debugging-on-stm32-cpu-usage' },
    '/fresh-air-for-mole-holes-dyson-floor-nozzle-revived':   { redirect: '/blog/2025/fresh-air-for-mole-holes-dyson-floor-nozzle-revived' },
    '/fresh-air-for-mole-holes-dyson-floor-nozzle-revived/':  { redirect: '/blog/2025/fresh-air-for-mole-holes-dyson-floor-nozzle-revived' },
    '/get-the-hell-out-of-my-wall-box-or-how-to-make-cheap-type-2-adapter-cables-not-so-sticky':   { redirect: '/blog/2021/get-the-hell-out-of-my-wall-box-or-how-to-make-cheap-type-2-adapter-cables-not-so-sticky' },
    '/get-the-hell-out-of-my-wall-box-or-how-to-make-cheap-type-2-adapter-cables-not-so-sticky/':  { redirect: '/blog/2021/get-the-hell-out-of-my-wall-box-or-how-to-make-cheap-type-2-adapter-cables-not-so-sticky' },
    '/getting-rid-of-nasty-underground-neighbours-iot-mouse-trap':   { redirect: '/blog/2024/getting-rid-of-nasty-underground-neighbours-iot-mouse-trap' },
    '/getting-rid-of-nasty-underground-neighbours-iot-mouse-trap/':  { redirect: '/blog/2024/getting-rid-of-nasty-underground-neighbours-iot-mouse-trap' },
    '/getting-started-embedded-part-ii-the-embeded-project':   { redirect: '/blog/2018/getting-started-embedded-part-ii-the-embeded-project' },
    '/getting-started-embedded-part-ii-the-embeded-project/':  { redirect: '/blog/2018/getting-started-embedded-part-ii-the-embeded-project' },
    '/getting-started-embedded-part-i-the-toolchain':   { redirect: '/blog/2018/getting-started-embedded-part-i-the-toolchain' },
    '/getting-started-embedded-part-i-the-toolchain/':  { redirect: '/blog/2018/getting-started-embedded-part-i-the-toolchain' },
    '/get-your-personal-oil-well-level-integrating-oilfox-into-home-assistant-using-node-red':   { redirect: '/blog/2021/get-your-personal-oil-well-level-integrating-oilfox-into-home-assistant-using-node-red' },
    '/get-your-personal-oil-well-level-integrating-oilfox-into-home-assistant-using-node-red/':  { redirect: '/blog/2021/get-your-personal-oil-well-level-integrating-oilfox-into-home-assistant-using-node-red' },
    '/google-chromecasts-smartphone-independance-day':   { redirect: '/blog/2018/google-chromecasts-smartphone-independance-day' },
    '/google-chromecasts-smartphone-independance-day/':  { redirect: '/blog/2018/google-chromecasts-smartphone-independance-day' },
    '/headless-rescue-system-over-ssh':   { redirect: '/blog/2019/headless-rescue-system-over-ssh' },
    '/headless-rescue-system-over-ssh/':  { redirect: '/blog/2019/headless-rescue-system-over-ssh' },
    '/how-to-build-a-private-storage-cluster-with-ceph':   { redirect: '/blog/2019/how-to-build-a-private-storage-cluster-with-ceph' },
    '/how-to-build-a-private-storage-cluster-with-ceph/':  { redirect: '/blog/2019/how-to-build-a-private-storage-cluster-with-ceph' },
    '/how-to-build-a-smart-home':   { redirect: '/blog/2019/how-to-build-a-smart-home' },
    '/how-to-build-a-smart-home/':  { redirect: '/blog/2019/how-to-build-a-smart-home' },
    '/how-to-debug-hardware-faults-on-your-dedicated-server':   { redirect: '/blog/2020/how-to-debug-hardware-faults-on-your-dedicated-server' },
    '/how-to-debug-hardware-faults-on-your-dedicated-server/':  { redirect: '/blog/2020/how-to-debug-hardware-faults-on-your-dedicated-server' },
    '/how-to-open-your-zipper-use-fuse-to-browse-archives':   { redirect: '/blog/2021/how-to-open-your-zipper-use-fuse-to-browse-archives' },
    '/how-to-open-your-zipper-use-fuse-to-browse-archives/':  { redirect: '/blog/2021/how-to-open-your-zipper-use-fuse-to-browse-archives' },
    '/how-to-wire-up-an-ev-wall-box':   { redirect: '/blog/2021/how-to-wire-up-an-ev-wall-box' },
    '/how-to-wire-up-an-ev-wall-box/':  { redirect: '/blog/2021/how-to-wire-up-an-ev-wall-box' },
    '/installing-bigbluebutton-on-your-dedicated-server':   { redirect: '/blog/2020/installing-bigbluebutton-on-your-dedicated-server' },
    '/installing-bigbluebutton-on-your-dedicated-server/':  { redirect: '/blog/2020/installing-bigbluebutton-on-your-dedicated-server' },
    '/integrating-wmbus-devices-into-iobroker':   { redirect: '/blog/2019/integrating-wmbus-devices-into-iobroker' },
    '/integrating-wmbus-devices-into-iobroker/':  { redirect: '/blog/2019/integrating-wmbus-devices-into-iobroker' },
    '/just-another-hobby-3d-printing':   { redirect: '/blog/2020/just-another-hobby-3d-printing' },
    '/just-another-hobby-3d-printing/':  { redirect: '/blog/2020/just-another-hobby-3d-printing' },
    '/just-do-it-how-to-create-your-own-home-assistant-add-on-part-1':   { redirect: '/blog/2021/just-do-it-how-to-create-your-own-home-assistant-add-on-part-1' },
    '/just-do-it-how-to-create-your-own-home-assistant-add-on-part-1/':  { redirect: '/blog/2021/just-do-it-how-to-create-your-own-home-assistant-add-on-part-1' },
    '/kathrein-exip-418-getting-it-back-to-work-on-ubiquity-networks':   { redirect: '/blog/2021/kathrein-exip-418-getting-it-back-to-work-on-ubiquity-networks' },
    '/kathrein-exip-418-getting-it-back-to-work-on-ubiquity-networks/':  { redirect: '/blog/2021/kathrein-exip-418-getting-it-back-to-work-on-ubiquity-networks' },
    '/limiting-ev-charge-soc-with-go-echarger-and-home-assistant':   { redirect: '/blog/2021/limiting-ev-charge-soc-with-go-echarger-and-home-assistant' },
    '/limiting-ev-charge-soc-with-go-echarger-and-home-assistant/':  { redirect: '/blog/2021/limiting-ev-charge-soc-with-go-echarger-and-home-assistant' },
    '/mbus-application-layer':   { redirect: '/blog/2023/mbus-application-layer' },
    '/mbus-application-layer/':  { redirect: '/blog/2023/mbus-application-layer' },
    '/merging-the-contents-of-two-influxdbs':   { redirect: '/blog/2019/merging-the-contents-of-two-influxdbs' },
    '/merging-the-contents-of-two-influxdbs/':  { redirect: '/blog/2019/merging-the-contents-of-two-influxdbs' },
    '/modbus-rj45-breakout':   { redirect: '/blog/2023/modbus-rj45-breakout' },
    '/modbus-rj45-breakout/':  { redirect: '/blog/2023/modbus-rj45-breakout' },
    '/moles-heating-system':   { redirect: '/blog/2022/moles-heating-system' },
    '/moles-heating-system/':  { redirect: '/blog/2022/moles-heating-system' },
    '/onewire-immersed':   { redirect: '/blog/2022/onewire-immersed' },
    '/onewire-immersed/':  { redirect: '/blog/2022/onewire-immersed' },
    '/orangepi-2g-iot-android-sdk':   { redirect: '/blog/2018/orangepi-2g-iot-android-sdk' },
    '/orangepi-2g-iot-android-sdk/':  { redirect: '/blog/2018/orangepi-2g-iot-android-sdk' },
    '/orangepi-4g-iot-android-8-1-sdk':   { redirect: '/blog/2018/orangepi-4g-iot-android-8-1-sdk' },
    '/orangepi-4g-iot-android-8-1-sdk/':  { redirect: '/blog/2018/orangepi-4g-iot-android-8-1-sdk' },
    '/orangepi-4g-iot-complete-pack':   { redirect: '/blog/2019/orangepi-4g-iot-complete-pack' },
    '/orangepi-4g-iot-complete-pack/':  { redirect: '/blog/2019/orangepi-4g-iot-complete-pack' },
    '/penmount-pci-touch-controllers-and-i2c-lost-in-space':   { redirect: '/blog/2020/penmount-pci-touch-controllers-and-i2c-lost-in-space' },
    '/penmount-pci-touch-controllers-and-i2c-lost-in-space/':  { redirect: '/blog/2020/penmount-pci-touch-controllers-and-i2c-lost-in-space' },
    '/pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible':   { redirect: '/blog/2022/pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible' },
    '/pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible/':  { redirect: '/blog/2022/pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible' },
    '/reading-a-meter-speaking-mbus':   { redirect: '/blog/2023/reading-a-meter-speaking-mbus' },
    '/reading-a-meter-speaking-mbus/':  { redirect: '/blog/2023/reading-a-meter-speaking-mbus' },
    '/reverse-engineering-the-buderus-km217':   { redirect: '/blog/2021/reverse-engineering-the-buderus-km217' },
    '/reverse-engineering-the-buderus-km217/':  { redirect: '/blog/2021/reverse-engineering-the-buderus-km217' },
    '/schools-out-how-to-tame-your-children':   { redirect: '/blog/2020/schools-out-how-to-tame-your-children' },
    '/schools-out-how-to-tame-your-children/':  { redirect: '/blog/2020/schools-out-how-to-tame-your-children' },
    '/smart-home-controlled-joy-it-lab-power-supply':   { redirect: '/blog/2023/smart-home-controlled-joy-it-lab-power-supply' },
    '/smart-home-controlled-joy-it-lab-power-supply/':  { redirect: '/blog/2023/smart-home-controlled-joy-it-lab-power-supply' },
    '/some-thoughs-on-the-m-bus':   { redirect: '/blog/2022/some-thoughs-on-the-m-bus' },
    '/some-thoughs-on-the-m-bus/':  { redirect: '/blog/2022/some-thoughs-on-the-m-bus' },
    '/sorting-your-digital-mess-how-to-easily-set-up-a-private-search-engine':   { redirect: '/blog/2021/sorting-your-digital-mess-how-to-easily-set-up-a-private-search-engine' },
    '/sorting-your-digital-mess-how-to-easily-set-up-a-private-search-engine/':  { redirect: '/blog/2021/sorting-your-digital-mess-how-to-easily-set-up-a-private-search-engine' },
    '/stm32-bldc-motor-control':   { redirect: '/blog/2019/stm32-bldc-motor-control' },
    '/stm32-bldc-motor-control/':  { redirect: '/blog/2019/stm32-bldc-motor-control' },
    '/stm32cubemx-and-sdram':   { redirect: '/blog/2020/stm32cubemx-and-sdram' },
    '/stm32cubemx-and-sdram/':  { redirect: '/blog/2020/stm32cubemx-and-sdram' },
    '/stm32-freertos-and-printf-with-floats':   { redirect: '/blog/2020/stm32-freertos-and-printf-with-floats' },
    '/stm32-freertos-and-printf-with-floats/':  { redirect: '/blog/2020/stm32-freertos-and-printf-with-floats' },
    '/stm32-uart-continuous-receive-with-interrupt':   { redirect: '/blog/2019/stm32-uart-continuous-receive-with-interrupt' },
    '/stm32-uart-continuous-receive-with-interrupt/':  { redirect: '/blog/2019/stm32-uart-continuous-receive-with-interrupt' },
    '/stm32-usb-dfu':   { redirect: '/blog/2020/stm32-usb-dfu' },
    '/stm32-usb-dfu/':  { redirect: '/blog/2020/stm32-usb-dfu' },
    '/taking-your-m-bus-online-with-mqtt':   { redirect: '/blog/2021/taking-your-m-bus-online-with-mqtt' },
    '/taking-your-m-bus-online-with-mqtt/':  { redirect: '/blog/2021/taking-your-m-bus-online-with-mqtt' },
    '/taming-the-cephodian-octopus-or-quincy':   { redirect: '/blog/2023/taming-the-cephodian-octopus-or-quincy' },
    '/taming-the-cephodian-octopus-or-quincy/':  { redirect: '/blog/2023/taming-the-cephodian-octopus-or-quincy' },
    '/the-great-flood-how-i-turned-my-living-room-into-a-high-tech-sump-pit':   { redirect: '/blog/2025/the-great-flood-how-i-turned-my-living-room-into-a-high-tech-sump-pit' },
    '/the-great-flood-how-i-turned-my-living-room-into-a-high-tech-sump-pit/':  { redirect: '/blog/2025/the-great-flood-how-i-turned-my-living-room-into-a-high-tech-sump-pit' },
    '/the-magic-of-absolute-humidity':   { redirect: '/blog/2021/the-magic-of-absolute-humidity' },
    '/the-magic-of-absolute-humidity/':  { redirect: '/blog/2021/the-magic-of-absolute-humidity' },
    '/the-remote-serial-debugging-nightmare':   { redirect: '/blog/2022/the-remote-serial-debugging-nightmare' },
    '/the-remote-serial-debugging-nightmare/':  { redirect: '/blog/2022/the-remote-serial-debugging-nightmare' },
    '/think-sustainable-thnk-city-reanimated-work-in-progress':   { redirect: '/blog/2021/think-sustainable-thnk-city-reanimated-work-in-progress' },
    '/think-sustainable-thnk-city-reanimated-work-in-progress/':  { redirect: '/blog/2021/think-sustainable-thnk-city-reanimated-work-in-progress' },
    '/ultrasound-distance-module-overview':   { redirect: '/blog/2021/ultrasound-distance-module-overview' },
    '/ultrasound-distance-module-overview/':  { redirect: '/blog/2021/ultrasound-distance-module-overview' },
    '/windows-was-just-a-pain':   { redirect: '/blog/2018/windows-was-just-a-pain' },
    '/windows-was-just-a-pain/':  { redirect: '/blog/2018/windows-was-just-a-pain' },
    '/wmbus-meters-and-how-to-get-it-into-home-assistant':   { redirect: '/blog/2021/wmbus-meters-and-how-to-get-it-into-home-assistant' },
    '/wmbus-meters-and-how-to-get-it-into-home-assistant/':  { redirect: '/blog/2021/wmbus-meters-and-how-to-get-it-into-home-assistant' },
  },
  devtools: { enabled: true },
})
