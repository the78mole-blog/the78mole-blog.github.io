#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Patch missing / sparse tags and categories in all blog posts.
Run once: uv run --script scripts/patch-taxonomy.py
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent

# -----------------------------------------------------------------------
# Mapping: relative path → {"tags": [...], "categories": [...]}
# Only NEW items – already-present ones are skipped automatically.
# -----------------------------------------------------------------------
PATCHES: dict[str, dict[str, list[str]]] = {
    # ── 2018 ──────────────────────────────────────────────────────────
    "content/blog/2018/digging.md": {
        "tags": ["intro", "mole", "blog"],
        "categories": [],
    },
    "content/blog/2018/getting-started-embedded-part-i-the-toolchain.md": {
        "tags": ["embedded", "toolchain", "gcc", "arm", "microcontroller"],
        "categories": ["Embedded", "Dev"],
    },
    "content/blog/2018/getting-started-embedded-part-ii-the-embeded-project.md": {
        "tags": ["embedded", "toolchain", "gcc", "arm", "microcontroller"],
        "categories": ["Embedded", "Dev"],
    },
    "content/blog/2018/google-chromecasts-smartphone-independance-day.md": {
        "tags": ["chromecast", "android", "streaming", "diy"],
        "categories": ["DIY"],
    },
    "content/blog/2018/windows-was-just-a-pain.md": {
        "tags": ["linux", "windows", "migration"],
        "categories": ["Tools"],
    },
    "content/blog/2018/orangepi-2g-iot-android-sdk.md": {
        "tags": ["orangepi", "android", "arm", "iot", "hardware"],
        "categories": ["Hardware"],
    },
    "content/blog/2018/orangepi-4g-iot-android-8-1-sdk.md": {
        "tags": ["orangepi", "android", "arm", "iot", "hardware"],
        "categories": ["Hardware"],
    },
    # ── 2019 ──────────────────────────────────────────────────────────
    "content/blog/2019/compile-ceph-mimic-on-arm-32-bit.md": {
        "tags": ["arm", "compilation", "linux", "build", "cpp"],
        "categories": [],
    },
    "content/blog/2019/compiling-software-on-ram-limited-multi-core-systems.md": {
        "tags": ["compilation", "build", "arm", "embedded", "linux", "optimization"],
        "categories": ["Dev", "Tools"],
    },
    "content/blog/2019/headless-rescue-system-over-ssh.md": {
        "tags": ["linux", "backup", "rescue", "system-recovery"],
        "categories": ["Tools"],
    },
    "content/blog/2019/how-to-build-a-private-storage-cluster-with-ceph.md": {
        "tags": ["storage", "diy", "odroid", "arm", "linux", "distributed-storage"],
        "categories": [],
    },
    "content/blog/2019/how-to-build-a-smart-home.md": {
        "tags": ["iobroker", "home-assistant", "linux", "arm", "odroid", "smart-home", "diy"],
        "categories": [],
    },
    "content/blog/2019/integrating-wmbus-devices-into-iobroker.md": {
        "tags": ["home-automation", "mqtt", "smart-home", "energy", "metering"],
        "categories": [],
    },
    "content/blog/2019/merging-the-contents-of-two-influxdbs.md": {
        "tags": ["timeseries", "data-migration", "influxdb"],
        "categories": ["Tools"],
    },
    "content/blog/2019/orangepi-4g-iot-complete-pack.md": {
        "tags": ["orangepi", "android", "arm", "iot", "hardware"],
        "categories": ["Hardware", "DIY"],
    },
    "content/blog/2019/stm32-bldc-motor-control.md": {
        "tags": ["stm32", "arm", "embedded", "hardware", "pwm", "motor"],
        "categories": ["Embedded", "Hardware"],
    },
    "content/blog/2019/stm32-uart-continuous-receive-with-interrupt.md": {
        "tags": ["uart", "interrupt", "embedded", "microcontroller", "arm", "stm32cubemx"],
        "categories": ["Embedded"],
    },
    # ── 2020 ──────────────────────────────────────────────────────────
    "content/blog/2020/doxygen-tips-and-tricks.md": {
        "tags": ["documentation", "cpp", "c", "code-generation"],
        "categories": ["Dev"],
    },
    "content/blog/2020/esp32-evb-and-platform-io-yet-another-esp32-tutorial.md": {
        "tags": ["esp-idf", "platformio", "iot", "microcontroller"],
        "categories": ["Embedded", "DIY"],
    },
    "content/blog/2020/freertos-debugging-on-stm32-cpu-usage.md": {
        "tags": ["rtos", "debugging", "embedded", "stm32", "microcontroller"],
        "categories": ["Embedded"],
    },
    "content/blog/2020/how-to-debug-hardware-faults-on-your-dedicated-server.md": {
        "tags": ["linux", "hardware", "diagnostics", "server"],
        "categories": ["Tools"],
    },
    "content/blog/2020/installing-bigbluebutton-on-your-dedicated-server.md": {
        "tags": ["videoconferencing", "open-source", "ubuntu", "server"],
        "categories": ["Tools"],
    },
    "content/blog/2020/just-another-hobby-3d-printing.md": {
        "tags": ["3d-printing", "fdm", "maker"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2020/penmount-pci-touch-controllers-and-i2c-lost-in-space.md": {
        "tags": ["i2c", "uart", "stm32", "embedded"],
        "categories": ["Embedded", "Hardware"],
    },
    "content/blog/2020/schools-out-how-to-tame-your-children.md": {
        "tags": ["moodle", "online-learning", "videoconference"],
        "categories": ["Tools"],
    },
    "content/blog/2020/stm32cubemx-and-sdram.md": {
        "tags": ["fmc", "memory", "embedded", "microcontroller"],
        "categories": ["Embedded"],
    },
    "content/blog/2020/stm32-freertos-and-printf-with-floats.md": {
        "tags": ["freertos", "stm32", "printf", "debugging", "embedded", "float", "arm"],
        "categories": ["Embedded"],
    },
    "content/blog/2020/stm32-usb-dfu.md": {
        "tags": ["stm32", "microcontroller", "embedded", "firmware", "usb"],
        "categories": ["Embedded", "DIY"],
    },
    # ── 2021 ──────────────────────────────────────────────────────────
    "content/blog/2021/angular-web-app-on-esp32.md": {
        "tags": ["web", "iot", "microcontroller"],
        "categories": ["Embedded", "Dev"],
    },
    "content/blog/2021/eex-epex-spot-and-the-real-net-intransparency.md": {
        "tags": ["energy", "electricity", "pricing", "market-data"],
        "categories": [],
    },
    "content/blog/2021/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial.md": {
        "tags": ["esp-idf", "iot", "microcontroller", "freertos"],
        "categories": ["Embedded", "DIY"],
    },
    "content/blog/2021/get-the-hell-out-of-my-wall-box-or-how-to-make-cheap-type-2-adapter-cables-not-so-sticky.md": {
        "tags": ["ev", "charging", "wallbox", "hardware"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2021/get-your-personal-oil-well-level-integrating-oilfox-into-home-assistant-using-node-red.md": {
        "tags": ["iot", "mqtt", "smart-home", "energy"],
        "categories": [],
    },
    "content/blog/2021/how-to-open-your-zipper-use-fuse-to-browse-archives.md": {
        "tags": ["linux", "filesystem", "archive", "fuse", "compression"],
        "categories": ["Tools"],
    },
    "content/blog/2021/how-to-wire-up-an-ev-wall-box.md": {
        "tags": ["ev", "charging", "wallbox", "electrical"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2021/just-do-it-how-to-create-your-own-home-assistant-add-on-part-1.md": {
        "tags": ["home-assistant", "docker", "addon", "automation"],
        "categories": ["Dev"],
    },
    "content/blog/2021/kathrein-exip-418-getting-it-back-to-work-on-ubiquity-networks.md": {
        "tags": ["networking", "satip", "unifi", "ubiquity"],
        "categories": ["Tools", "DIY"],
    },
    "content/blog/2021/limiting-ev-charge-soc-with-go-echarger-and-home-assistant.md": {
        "tags": ["ev", "charging", "automation", "smart-home"],
        "categories": ["Smart Home", "DIY"],
    },
    "content/blog/2021/reverse-engineering-the-buderus-km217.md": {
        "tags": ["esp32", "heating", "esphome", "reverse-engineering", "iot"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2021/sorting-your-digital-mess-how-to-easily-set-up-a-private-search-engine.md": {
        "tags": ["search", "indexing", "server", "open-source"],
        "categories": [],
    },
    "content/blog/2021/taking-your-m-bus-online-with-mqtt.md": {
        "tags": ["m-bus", "mqtt", "metering", "smart-home", "networking", "iot"],
        "categories": [],
    },
    "content/blog/2021/the-magic-of-absolute-humidity.md": {
        "tags": ["esp32", "esphome", "sensor", "humidity", "home-assistant", "iot"],
        "categories": ["DIY"],
    },
    "content/blog/2021/think-sustainable-thnk-city-reanimated-work-in-progress.md": {
        "tags": ["ev", "battery", "lifepo4", "restoration"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2021/ultrasound-distance-module-overview.md": {
        "tags": ["sensor", "distance-measurement"],
        "categories": ["Hardware", "DIY"],
    },
    "content/blog/2021/wmbus-meters-and-how-to-get-it-into-home-assistant.md": {
        "tags": ["wmbus", "metering", "mqtt", "home-assistant", "smart-home", "iot"],
        "categories": [],
    },
    # ── 2022 ──────────────────────────────────────────────────────────
    "content/blog/2022/moles-heating-system.md": {
        "tags": ["heating", "heat-pump", "solar", "battery", "energy"],
        "categories": ["DIY", "Smart Home"],
    },
    "content/blog/2022/onewire-immersed.md": {
        "tags": ["sensor", "temperature", "esp32", "iot", "heating"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2022/pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible.md": {
        "tags": ["riot-os", "rtos", "embedded", "windows", "arm", "cross-compilation"],
        "categories": ["Dev"],
    },
    "content/blog/2022/some-thoughs-on-the-m-bus.md": {
        "tags": ["metering", "protocol", "rs485", "iot", "networking"],
        "categories": [],
    },
    "content/blog/2022/the-remote-serial-debugging-nightmare.md": {
        "tags": ["debugging", "serial", "networking", "terminal"],
        "categories": ["Tools", "Dev"],
    },
    # ── 2023 ──────────────────────────────────────────────────────────
    "content/blog/2023/code-red-on-fire-or-heat-metering-with-node-red.md": {
        "tags": ["m-bus", "node-red", "automation", "energy", "metering", "iot"],
        "categories": ["DIY"],
    },
    "content/blog/2023/crying-on-open-waters-a-piece-of-hw-for-ahoydtu-and-reading-the-hoymiles-inverters.md": {
        "tags": ["solar", "inverter", "energy", "monitoring"],
        "categories": ["Hardware", "DIY"],
    },
    "content/blog/2023/doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data.md": {
        "tags": ["tibber", "sml", "protocol", "smart-meter", "energy", "decoding"],
        "categories": ["Dev", "Tools"],
    },
    "content/blog/2023/mbus-application-layer.md": {
        "tags": ["m-bus", "protocol", "metering", "specification", "networking"],
        "categories": [],
    },
    "content/blog/2023/modbus-rj45-breakout.md": {
        "tags": ["modbus", "rs485", "networking", "metering"],
        "categories": ["Hardware", "DIY"],
    },
    "content/blog/2023/reading-a-meter-speaking-mbus.md": {
        "tags": ["m-bus", "metering", "protocol", "iot", "smart-meter", "networking"],
        "categories": [],
    },
    "content/blog/2023/smart-home-controlled-joy-it-lab-power-supply.md": {
        "tags": ["modbus", "esphome", "laboratory", "automation"],
        "categories": ["Dev"],
    },
    "content/blog/2023/taming-the-cephodian-octopus-or-quincy.md": {
        "tags": ["storage", "linux", "arm", "distributed-storage"],
        "categories": [],
    },
    # ── 2024 ──────────────────────────────────────────────────────────
    "content/blog/2024/getting-rid-of-nasty-underground-neighbours-iot-mouse-trap.md": {
        "tags": ["iot", "sensor", "3d-printing", "home-assistant"],
        "categories": ["DIY", "Hardware"],
    },
    # ── 2025 ──────────────────────────────────────────────────────────
    "content/blog/2025/fresh-air-for-mole-holes-dyson-floor-nozzle-revived.md": {
        "tags": ["repair", "3d-printing", "diy", "hardware", "maker"],
        "categories": ["DIY", "Hardware"],
    },
    "content/blog/2025/the-great-flood-how-i-turned-my-living-room-into-a-high-tech-sump-pit.md": {
        "tags": ["sensor", "iot", "home-assistant", "diy"],
        "categories": ["Smart Home", "DIY"],
    },
    # ── 2026 ──────────────────────────────────────────────────────────
    "content/blog/2026/devc-open-devcontainer-from-shell.md": {
        "tags": ["dev-container", "vscode", "docker", "bash", "developer-tools", "automation"],
        "categories": [],
    },
    "content/blog/2026/hw-398-usb-c-pd-trigger-board.md": {
        "tags": ["usb-c", "power-delivery", "hardware", "diy"],
        "categories": [],
    },
    "content/blog/2026/ptouch-webapp-browser-label-printing.md": {
        "tags": ["web-serial", "javascript", "vite", "label-printer", "hardware"],
        "categories": [],
    },
    "content/blog/2026/publishing-on-github-pages-with-nuxt.md": {
        "tags": ["nuxt", "github-pages", "ssg", "blog", "static-site", "deployment"],
        "categories": [],
    },
    "content/blog/2026/teaching-the-ai-mole-github-copilot-skills.md": {
        "tags": ["copilot", "ai", "github", "skills", "automation", "nuxt"],
        "categories": ["Tools"],
    },
}

# -----------------------------------------------------------------------
# Frontmatter parser / writer
# -----------------------------------------------------------------------
FM_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)


def patch_file(path: Path, new_tags: list[str], new_cats: list[str]) -> bool:
    """Return True if the file was actually modified."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        print(f"  SKIP (no frontmatter): {path.relative_to(ROOT)}")
        return False

    fm_raw = m.group(1)
    body = text[m.end():]
    fm = yaml.safe_load(fm_raw) or {}

    changed = False

    # ── tags ──────────────────────────────────────────────────────────
    if new_tags:
        existing = [str(t) for t in (fm.get("tags") or [])]
        existing_lower = {t.lower() for t in existing}
        to_add = [t for t in new_tags if t.lower() not in existing_lower]
        if to_add:
            fm["tags"] = existing + to_add
            changed = True

    # ── categories ────────────────────────────────────────────────────
    if new_cats:
        existing = [str(c) for c in (fm.get("categories") or [])]
        existing_lower = {c.lower() for c in existing}
        to_add = [c for c in new_cats if c.lower() not in existing_lower]
        if to_add:
            fm["categories"] = existing + to_add
            changed = True

    if not changed:
        return False

    # Serialise back – keep lists in block style
    new_fm = yaml.dump(
        fm,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    path.write_text(f"---\n{new_fm}---\n{body}", encoding="utf-8")
    return True


# -----------------------------------------------------------------------
def main() -> None:
    modified = 0
    skipped = 0
    for rel, patch in PATCHES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"  MISSING: {rel}")
            skipped += 1
            continue
        if patch_file(path, patch.get("tags", []), patch.get("categories", [])):
            print(f"  patched : {rel}")
            modified += 1
        else:
            skipped += 1

    print(f"\nDone. {modified} files patched, {skipped} unchanged/skipped.")


if __name__ == "__main__":
    main()
