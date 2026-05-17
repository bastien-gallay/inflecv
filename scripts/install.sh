#!/usr/bin/env bash
# inflecv installer — bootstraps Typst, uv, just, Python deps, fonts.
# Idempotent: safe to re-run.
#
# Usage:
#   ./scripts/install.sh           # full install
#   ./scripts/install.sh --check   # report what's missing, don't install
#   ./scripts/install.sh --fonts   # only (re)install Typst fonts
#
# Supported platforms: macOS, Linux. Windows: WSL.

set -euo pipefail

CHECK_ONLY=false
FONTS_ONLY=false
case "${1:-}" in
  --check) CHECK_ONLY=true ;;
  --fonts) FONTS_ONLY=true ;;
  -h|--help)
    sed -n '2,12p' "$0"
    exit 0
    ;;
esac

log()  { printf '\033[1;34m[inflecv]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[inflecv]\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31m[inflecv]\033[0m %s\n' "$*" >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

# Detect platform
case "$(uname -s)" in
  Darwin) PLATFORM=macos ;;
  Linux)  PLATFORM=linux ;;
  *)      fail "unsupported platform: $(uname -s)" ;;
esac
log "platform: $PLATFORM"

# ---- Step 1: Typst ----
install_typst() {
  if have typst; then
    log "typst: $(typst --version) ✓"
    return
  fi
  $CHECK_ONLY && { warn "typst: missing"; return; }
  log "installing typst…"
  case "$PLATFORM" in
    macos)
      if have brew; then
        brew install typst
      else
        fail "typst missing and brew not found. Install brew or typst manually: https://typst.app"
      fi
      ;;
    linux)
      # Use cargo if available, else suggest manual.
      if have cargo; then
        cargo install typst-cli
      else
        fail "typst missing and cargo not found. Install rust+cargo, or download typst: https://github.com/typst/typst/releases"
      fi
      ;;
  esac
}

# ---- Step 2: uv (Python package manager) ----
install_uv() {
  if have uv; then
    log "uv: $(uv --version) ✓"
    return
  fi
  $CHECK_ONLY && { warn "uv: missing"; return; }
  log "installing uv…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  have uv || fail "uv installation failed; PATH=$PATH"
}

# ---- Step 3: just (task runner) ----
install_just() {
  if have just; then
    log "just: $(just --version) ✓"
    return
  fi
  $CHECK_ONLY && { warn "just: missing"; return; }
  log "installing just…"
  case "$PLATFORM" in
    macos) have brew && brew install just || cargo install just ;;
    linux) cargo install just ;;
  esac
}

# ---- Step 4: Python deps via uv ----
install_python_deps() {
  if [ ! -f pyproject.toml ]; then
    warn "no pyproject.toml in $(pwd); skipping python deps"
    return
  fi
  $CHECK_ONLY && { log "python deps: would run 'uv sync'"; return; }
  log "syncing python deps with uv…"
  uv sync
}

# ---- Step 5: Typst fonts ----
install_fonts() {
  # Fonts required by neat-cv template
  # See src/manifest.yml for the canonical list
  local fonts_needed=("Inter" "Font Awesome 6 Free" "Font Awesome 6 Brands")
  log "checking Typst fonts…"
  local missing=()
  for f in "${fonts_needed[@]}"; do
    if ! typst fonts 2>/dev/null | grep -qFi "$f"; then
      missing+=("$f")
    fi
  done
  if [ ${#missing[@]} -eq 0 ]; then
    log "fonts: all required fonts found ✓"
    return
  fi
  warn "missing fonts: ${missing[*]}"
  $CHECK_ONLY && return
  case "$PLATFORM" in
    macos)
      have brew && brew install --cask font-inter font-fontawesome
      ;;
    linux)
      warn "install fonts manually: ${missing[*]}"
      warn "Inter:        https://rsms.me/inter/"
      warn "Font Awesome: https://fontawesome.com/download"
      ;;
  esac
}

# ---- Main ----
if $FONTS_ONLY; then
  install_fonts
  exit 0
fi

install_typst
install_uv
install_just
install_python_deps
install_fonts

if $CHECK_ONLY; then
  log "check complete"
  exit 0
fi

log "smoke test: 'just build'"
if just build >/dev/null 2>&1; then
  log "✅ inflecv installed and built successfully"
  log "open dist/cv.pdf to verify"
else
  warn "build failed; run 'just build' to see errors"
  exit 1
fi
