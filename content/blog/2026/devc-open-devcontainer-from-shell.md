---
title: "devc – Open a VS Code Dev Container Directly from the Shell"
date: '2026-05-06'
description: 'A tiny bash script that saves you from clicking through VS Code every time you want to open a project in a Dev Container – just type devc and go.'
image: /images/blog/2026/05/devc-cover.jpeg
categories:
  - Dev
  - Tools
---

Moles are creatures of habit. We navigate our tunnels by feel, taking the same shortcuts every day without thinking about them. Until one day you realise you've been clicking through the same three VS Code menus every single time you want to open a project in a Dev Container – and it starts to feel like digging through concrete instead of soft earth.

The fix? A two-second shell command. That's all it takes.

## The Problem

[VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) are fantastic. You define your full development environment in a `.devcontainer/devcontainer.json`, commit it to the repo, and anyone – including your future self after a full OS reinstall – gets the exact same toolchain, extensions, and settings.

The friction? Every time you want to *open* a project in its container, you have to:

1. Open VS Code (or switch to it)
2. Hit `F1` → "Dev Containers: Open Folder in Container..." or press the appearing button in the bottom-right corner
3. Wait

If you live in the terminal (subways have terminals, tunnels are something alike) – and most moles do – this feels like a wrong turn every time.

## The Solution: `devc`

[`devc`](https://gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc) is a small bash script that collapses all of that into a single command:

```bash
# Open current directory in its Dev Container
devc .

# Open a specific project by path
devc ~/projects/my-project

# Show help
devc --help
```

The container starts, and VS Code opens connected to it. If the directory doesn't contain a `.devcontainer` config, the script warns you but continues – useful if you want to open any folder using the global devcontainer defaults.

## How It Works

The script is deliberately simple – no dependencies beyond `bash`, `python3` (for JSON parsing), and the [devcontainer CLI](https://github.com/devcontainers/cli). It locates the `devcontainer.json` in your project, reads the `workspaceFolder` from it (stripping `// comments` first, since strict JSON parsers reject them), starts the container via `devcontainer up`, and finally opens VS Code with the correct `vscode-remote://` URI built from the hex-encoded local path.

The full source is [on GitHub Gist](https://gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc).

## Prerequisites

Before `devc` can do its job, three things need to be in place: VS Code with the Dev Containers extension, Node.js (for the devcontainer CLI), and the CLI itself.

### 1. VS Code + Dev Containers Extension

Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) from the VS Code Marketplace. It provides the `vscode-remote://dev-container+...` protocol handler that `devc` relies on to open VS Code connected to the container.

### 2. Node.js via NVM

The devcontainer CLI is an npm package, so you need Node.js. The cleanest way to manage Node.js versions on Linux and macOS is [NVM (Node Version Manager)](https://github.com/nvm-sh/nvm):

```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# Reload your shell, then install the latest LTS release
nvm install --lts
nvm use --lts

# Verify
node --version
npm --version
```

NVM installs Node into `~/.nvm/` and doesn't require `sudo`. You can switch between Node versions per-project using `.nvmrc` files – handy when different projects need different runtimes.

### 3. devcontainer CLI

With Node.js in place, install the official [Dev Containers CLI](https://github.com/devcontainers/cli) globally:

```bash
npm install -g @devcontainers/cli

# Verify
devcontainer --version
```

The CLI handles everything container-related: building the image, starting the container, and forwarding the workspace mount. `devc` just calls `devcontainer up` and then hands off to VS Code.

### Summary

| What | How |
| --- | --- |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com/) |
| Dev Containers extension | `code --install-extension ms-vscode-remote.remote-containers` |
| NVM | `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh \| bash` |
| Node.js LTS | `nvm install --lts` |
| devcontainer CLI | `npm install -g @devcontainers/cli` |
| `python3` + `xxd` | Pre-installed on virtually all Linux/macOS systems |

## Installation

```bash
# Download the script
curl -fsSL https://gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc/raw/devc \
  -o /usr/local/bin/devc

# Make it executable
chmod +x /usr/local/bin/devc
```

Or grab the [raw file from the Gist](https://gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc) and drop it anywhere on your `$PATH`.

## Why Not Just Use the VS Code Command?

You could. But `devc` fits into shell workflows. You can wrap it in aliases, call it from scripts, add it to a project's `Makefile`, or use it with `fzf` to fuzzy-pick a project and open it in one keystroke:

```bash
# Fuzzy-open any project in its Dev Container
alias dv='devc "$(find ~/projects -maxdepth 2 -name devcontainer.json \
  | sed "s|/.devcontainer/devcontainer.json||;s|/.devcontainer.json||" \
  | fzf)"'
```

## The Gist

The script lives at: [gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc](https://gist.github.com/the78mole/02fc17c20a81113a28d26392d58218dc) – intentionally a single file, no installer, no package, no configuration. The tunnel is open.
