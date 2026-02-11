#!/usr/bin/env bash
# 10865xseed One-Line Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_ORG/10865xseed/main/install.sh | bash

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="${OPENCLAW_REPO:-https://github.com/YOUR_ORG/10865xseed.git}"
INSTALL_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
BIN_DIR="$HOME/.local/bin"
CLONE_DIR="$INSTALL_DIR/source"

echo_step() {
    echo -e "${MAGENTA}▸${NC} $1"
}

echo_success() {
    echo -e "${GREEN}✓${NC} $1"
}

echo_error() {
    echo -e "${RED}✗${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
check_requirements() {
    echo_step "Checking requirements..."
    
    if ! command -v python3 &> /dev/null; then
        echo_error "python3 not found. Please install Python 3.7+"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        echo_error "git not found. Please install git"
        exit 1
    fi
    
    echo_success "Requirements satisfied"
}

# Clone or update repository
install_repo() {
    echo_step "Installing repository..."
    
    if [ -d "$CLONE_DIR" ]; then
        echo_warn "Existing installation found at $CLONE_DIR"
        read -p "Update? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$CLONE_DIR"
            git pull origin main || git pull origin master
            echo_success "Repository updated"
        else
            echo_warn "Skipping repository update"
        fi
    else
        mkdir -p "$INSTALL_DIR"
        git clone "$REPO_URL" "$CLONE_DIR"
        echo_success "Repository cloned to $CLONE_DIR"
    fi
}

# Install Python dependencies
install_dependencies() {
    echo_step "Installing Python dependencies..."
    
    if python3 -m pip install --user --quiet rich; then
        echo_success "Dependencies installed (rich)"
    else
        echo_warn "Failed to install rich (may already be installed)"
    fi
}

# Create symlink to openclaw-seed command
create_symlink() {
    echo_step "Creating command-line tool..."
    
    mkdir -p "$BIN_DIR"
    
    SEED_SCRIPT="$CLONE_DIR/koshas/annamaya/scripts/openclaw_seed.py"
    SYMLINK="$BIN_DIR/openclaw-seed"
    
    if [ -f "$SEED_SCRIPT" ]; then
        chmod +x "$SEED_SCRIPT"
        ln -sf "$SEED_SCRIPT" "$SYMLINK"
        echo_success "Command installed: $SYMLINK"
    else
        echo_error "Script not found: $SEED_SCRIPT"
        exit 1
    fi
}

# Check if ~/.local/bin is in PATH
check_path() {
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo_warn "$BIN_DIR is not in your PATH"
        echo "Add this to your shell config (~/.bashrc, ~/.zshrc, etc.):"
        echo -e "${BLUE}  export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        
        # Detect shell
        SHELL_NAME=$(basename "$SHELL")
        case "$SHELL_NAME" in
            bash)
                SHELL_RC="$HOME/.bashrc"
                ;;
            zsh)
                SHELL_RC="$HOME/.zshrc"
                ;;
            *)
                SHELL_RC="$HOME/.profile"
                ;;
        esac
        
        echo
        read -p "Auto-add to $SHELL_RC? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            echo_success "Added to $SHELL_RC (restart shell or source it)"
        fi
    else
        echo_success "PATH is configured correctly"
    fi
}

# Display completion message
completion_message() {
    echo
    echo -e "${MAGENTA}════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}✨ PRANA PRATHISTAAPANA COMPLETE ✨${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════${NC}"
    echo
    echo "Installation complete! Next steps:"
    echo
    echo -e "  ${GREEN}1.${NC} Run the interactive setup:"
    echo -e "     ${BLUE}openclaw-seed install${NC}"
    echo
    echo -e "  ${GREEN}2.${NC} Or generate Prana context directly:"
    echo -e "     ${BLUE}openclaw-seed prana --root $CLONE_DIR --platform claude${NC}"
    echo
    echo -e "  ${GREEN}3.${NC} Verify installation:"
    echo -e "     ${BLUE}openclaw-seed doctor${NC}"
    echo
    echo "Documentation:"
    echo "  • Installation: $CLONE_DIR/INSTALL.md"
    echo "  • Architecture: $CLONE_DIR/ARCHITECTURE.md"
    echo "  • Copilot Guide: $CLONE_DIR/.github/copilot-instructions.md"
    echo
    echo -e "${MAGENTA}कृतं कर्म — The work is done.${NC}"
    echo
}

# Main installation flow
main() {
    echo -e "${MAGENTA}"
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║   10865xseed / OpenClaw Installation Ritual     ║"
    echo "║   Tryambakam Noesis Consciousness Architecture   ║"
    echo "╚═══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    
    check_requirements
    install_repo
    install_dependencies
    create_symlink
    check_path
    completion_message
}

# Run installer
main "$@"
