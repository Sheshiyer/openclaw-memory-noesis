# Development Plan

**Structured roadmap for maintaining, releasing, and evolving 10865xseed**

## Current Status (v0.1.0-alpha)

### ✅ Complete
- Prana context assembly system (`prana.py`)
- Rich TUI installation wizard (`setup_openclaw.py`)
- CLI tool with subcommands (`openclaw_seed.py`)
- One-line installer (`install.sh`)
- Platform support (Claude Code, Cursor, generic)
- Workspace agent scaffolds (4 agents)
- Comprehensive documentation (INSTALL.md, ARCHITECTURE.md)
- GitHub Copilot instructions

### 🚧 In Progress
- Testing and validation
- User feedback collection
- Documentation refinement

### ⏳ Planned
- Automated updates
- CI/CD pipeline
- Package distribution (Homebrew, PyPI)
- Vector DB integration
- Community templates

---

## Development Workflow

### Branch Strategy

```
main                  (stable, tagged releases)
  ├── develop        (integration branch)
  │   ├── feature/*  (new features)
  │   ├── fix/*      (bug fixes)
  │   └── docs/*     (documentation)
```

**Rules:**
- `main` is always deployable
- `develop` is the integration branch
- Feature branches merge to `develop` via PR
- Release candidates merge `develop` → `main` with version tag

### Commit Conventions

Use conventional commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance (deps, build, etc.)

**Examples:**
```
feat(prana): add vector DB support for memory persistence
fix(installer): handle missing rich dependency gracefully
docs(architecture): add user journey flow diagrams
chore(deps): bump rich to v13.0.0
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested on macOS
- [ ] Tested on Linux
- [ ] Tested with Claude Code
- [ ] Tested with Cursor
- [ ] Ran `openclaw-seed doctor`

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Commented hard-to-understand areas
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests (if applicable)
```

---

## Release Cycle

### Versioning

**Semantic Versioning:** `MAJOR.MINOR.PATCH`

- **MAJOR** (1.0.0): Breaking changes to Prana format, kernel structure, or CLI interface
- **MINOR** (0.2.0): New features, platforms, agents (backward compatible)
- **PATCH** (0.1.1): Bug fixes, docs, small improvements

### Release Schedule

- **Patch releases**: As needed (bug fixes)
- **Minor releases**: Monthly (new features)
- **Major releases**: Quarterly (architectural changes)

### Release Process

**1. Pre-release Preparation**

```bash
# 1. Update version
# Edit: koshas/annamaya/scripts/openclaw_seed.py
VERSION = "0.2.0"

# 2. Update CHANGELOG.md
# Add:
## [0.2.0] - 2026-02-15
### Added
- Vector DB memory integration
- New workspace agent: workspace-soma-navigator

### Fixed
- TUI wizard crash on Ctrl+C
- PATH detection for zsh users

# 3. Run full test suite
./tests/run_all_tests.sh

# 4. Manual smoke tests
openclaw-seed doctor
openclaw-seed install
openclaw-seed prana --root . --platform claude
```

**2. Release Tagging**

```bash
git checkout main
git pull origin main
git merge develop

# Tag release
git tag -a v0.2.0 -m "Release v0.2.0: Vector DB memory + Soma Navigator"
git push origin main
git push origin v0.2.0
```

**3. GitHub Release**

- Go to GitHub Releases
- Create new release from tag `v0.2.0`
- Title: `v0.2.0 - Vector DB Memory Integration`
- Description: Copy from CHANGELOG.md
- Attach artifacts (if any)
- Publish

**4. Post-release**

```bash
# Update develop branch
git checkout develop
git merge main
git push origin develop

# Announce
# - Post to Discord/Slack
# - Update documentation site
# - Tweet/share (optional)
```

---

## Testing Strategy

### Manual Testing Checklist

**Installation Testing:**
- [ ] Fresh install on macOS
- [ ] Fresh install on Linux (Ubuntu/Debian)
- [ ] Update existing installation
- [ ] Install with existing `~/.openclaw/`
- [ ] Verify PATH modification
- [ ] Test with different shells (bash, zsh, fish)

**Prana Generation:**
- [ ] Generate for Claude Code platform
- [ ] Generate for Cursor platform
- [ ] Generate generic context
- [ ] Verify file size (~115KB)
- [ ] Check section headers are present
- [ ] Test with custom root path

**TUI Wizard:**
- [ ] Complete full wizard flow
- [ ] Test all archetype options
- [ ] Test all platform options
- [ ] Test abort (Ctrl+C)
- [ ] Test "No" to all optional streams
- [ ] Verify config saved correctly

**CLI Commands:**
- [ ] `openclaw-seed install`
- [ ] `openclaw-seed prana --root . --platform claude`
- [ ] `openclaw-seed scaffold-agent --name test --template pi`
- [ ] `openclaw-seed doctor`
- [ ] `openclaw-seed --help`

**Platform Integration:**
- [ ] Claude Code loads context automatically
- [ ] Cursor respects `.cursorrules`
- [ ] Context file is valid markdown
- [ ] No encoding issues with Sanskrit/Greek text

### Automated Testing (Future)

**Unit Tests** (`tests/unit/`)
- `test_prana_system.py` - Prana gathering logic
- `test_openclaw_seed.py` - CLI argument parsing
- `test_installer.py` - Installation logic

**Integration Tests** (`tests/integration/`)
- `test_full_install.py` - End-to-end install flow
- `test_platform_generation.py` - Context generation for each platform
- `test_agent_scaffolding.py` - Agent creation from template

**Smoke Tests** (`tests/smoke/`)
- Basic "can it run?" tests on CI

---

## Maintenance Tasks

### Weekly
- [ ] Monitor GitHub issues
- [ ] Review PRs
- [ ] Test `main` branch on fresh system
- [ ] Check for dependency updates

### Monthly
- [ ] Review and update documentation
- [ ] Plan next minor release
- [ ] Triage and close stale issues
- [ ] Update CHANGELOG.md

### Quarterly
- [ ] Major release planning
- [ ] Architectural review
- [ ] Security audit
- [ ] Performance profiling
- [ ] User survey/feedback

---

## Gap Analysis

### Current Gaps

**1. Testing Infrastructure**
- **Gap:** No automated tests
- **Impact:** Manual testing is time-consuming and error-prone
- **Plan:** Create pytest suite (Phase 1, Month 1)
- **Priority:** HIGH

**2. CI/CD Pipeline**
- **Gap:** No GitHub Actions for automated testing/release
- **Impact:** Release process is manual
- **Plan:** Set up GH Actions (Phase 1, Month 1-2)
- **Priority:** HIGH

**3. Package Distribution**
- **Gap:** Only installable via curl/git clone
- **Impact:** Lower discoverability, harder to update
- **Plan:** 
  - PyPI package (Phase 2, Month 3)
  - Homebrew tap (Phase 2, Month 4)
- **Priority:** MEDIUM

**4. Update Mechanism**
- **Gap:** No `openclaw-seed update` command
- **Impact:** Users must manually re-run installer
- **Plan:** Auto-update with version check (Phase 2, Month 2)
- **Priority:** MEDIUM

**5. Error Handling**
- **Gap:** Limited error messages in TUI wizard
- **Impact:** Users may get stuck on failures
- **Plan:** Improve error reporting and recovery (Phase 1, Month 1)
- **Priority:** MEDIUM

**6. Backup/Restore**
- **Gap:** No built-in backup of `~/.openclaw/`
- **Impact:** Users risk losing config on upgrades
- **Plan:** Add `openclaw-seed backup/restore` commands (Phase 2, Month 3)
- **Priority:** LOW

**7. Documentation**
- **Gap:** No video tutorials or visual guides
- **Impact:** Harder for non-technical users
- **Plan:** Create screencasts (Phase 3, Month 6)
- **Priority:** LOW

---

## Roadmap

### Phase 1: Foundation (Months 1-2)

**Goal:** Stabilize core, establish testing/CI

- [x] One-line installer
- [x] Rich TUI wizard
- [x] Multi-platform support
- [x] Documentation (INSTALL, ARCHITECTURE)
- [ ] Automated test suite (pytest)
- [ ] GitHub Actions CI/CD
- [ ] Error handling improvements
- [ ] CHANGELOG.md
- [ ] CONTRIBUTING.md
- [ ] Issue/PR templates

**Deliverable:** v1.0.0 release

### Phase 2: Distribution & UX (Months 3-4)

**Goal:** Make it easy to discover, install, and update

- [ ] PyPI package (`pip install openclaw-seed`)
- [ ] Homebrew tap (`brew install openclaw-seed`)
- [ ] Auto-update mechanism
- [ ] Backup/restore commands
- [ ] Config migration tool (platform switching)
- [ ] Improved error messages
- [ ] Progress indicators for long operations

**Deliverable:** v2.0.0 release

### Phase 3: Advanced Features (Months 5-6)

**Goal:** Extend capabilities beyond basic context injection

- [ ] Vector DB integration (ChromaDB/Pinecone)
- [ ] MCP server for vault queries
- [ ] Plugin system for custom agents
- [ ] Web-based setup UI (optional)
- [ ] Docker container image
- [ ] Cross-vault synchronization

**Deliverable:** v3.0.0 release

### Phase 4: Ecosystem (Months 7-12)

**Goal:** Build community and reusable components

- [ ] Marketplace for workspace templates
- [ ] Community-contributed Prana streams
- [ ] GitHub App for auto-setup in repos
- [ ] VS Code extension (optional)
- [ ] Documentation site (Docusaurus/MkDocs)
- [ ] Video tutorials
- [ ] Conference talk/demo

**Deliverable:** v4.0.0 release + thriving community

---

## Development Environment Setup

### Prerequisites
- Python 3.7+
- Git
- Homebrew (macOS) or apt (Linux)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR_ORG/10865xseed.git
cd 10865xseed

# 2. Install development dependencies
python3 -m pip install --user -r requirements-dev.txt
# (to be created: rich, pytest, black, mypy)

# 3. Create test vault structure
./scripts/setup_test_vault.sh

# 4. Install pre-commit hooks
git config core.hooksPath .githooks

# 5. Verify setup
python3 -m pytest tests/
openclaw-seed doctor
```

### Code Style

**Python:**
- Follow PEP 8
- Use `black` for formatting (line length 100)
- Use `mypy` for type checking
- Docstrings for all public functions

**Bash:**
- Use `shellcheck` for linting
- Set `set -euo pipefail` in all scripts
- Quote all variables

**Markdown:**
- Use `markdownlint` for consistency
- Max line length 120 chars
- One sentence per line (for diffs)

### Editor Setup

**VS Code:**
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

**Vim/Neovim:**
```vim
" .vimrc / init.vim
autocmd FileType python setlocal formatprg=black\ -
```

---

## Communication Channels

### GitHub
- **Issues:** Bug reports, feature requests
- **Discussions:** General questions, ideas
- **PRs:** Code contributions

### Discord (Hypothetical)
- `#general` - General chat
- `#development` - Dev discussions
- `#support` - User help

### Documentation Site (Future)
- Tutorial videos
- API reference
- Community cookbook

---

## Contributor Recognition

### Levels
- **Core Maintainer:** Full commit access, release authority
- **Contributor:** Merged PR (added to CONTRIBUTORS.md)
- **Community Helper:** Active in issues/discussions

### Recognition
- List in CONTRIBUTORS.md
- Mention in release notes
- Shoutout in Discord/Twitter

---

## Deprecation Policy

When removing features:

1. **Deprecation warning** (1 minor release)
   - Log warning when deprecated feature is used
   - Update docs to mark as deprecated

2. **Removal** (next major release)
   - Remove code
   - Update CHANGELOG with breaking changes
   - Provide migration guide

**Example:**
```
v2.1.0 - Deprecate `--legacy-format` flag
v2.2.0 - Still supported, warning logged
v3.0.0 - Removed, use `--format=modern` instead
```

---

## Support & Troubleshooting

### Common Issues

**Issue:** `openclaw-seed: command not found`
**Fix:** Ensure `~/.local/bin` in PATH, or run installer again

**Issue:** `Missing dependency: rich`
**Fix:** `python3 -m pip install --user rich`

**Issue:** TUI wizard crashes on selection
**Fix:** Update rich: `python3 -m pip install --upgrade rich`

**Issue:** Context file not loaded by Claude Code
**Fix:** Restart Claude Code, verify file at `~/.claude/openclaw_context.md`

### Getting Help

1. Check documentation (INSTALL.md, ARCHITECTURE.md)
2. Run `openclaw-seed doctor`
3. Search existing GitHub issues
4. Open new issue with:
   - OS version
   - Python version
   - Output of `openclaw-seed doctor`
   - Steps to reproduce

---

## Security

### Reporting Vulnerabilities

**DO NOT** open public issue for security bugs.

Email: security@thoughtseed.space (or your security email)

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

Response time: 48 hours

### Security Checklist

- [ ] Never commit secrets (`.env`, API keys)
- [ ] Validate all user input in TUI
- [ ] No arbitrary code execution from config
- [ ] Sanitize file paths (prevent directory traversal)
- [ ] Use HTTPS for all external requests

---

**This development plan is a living document. Update quarterly. कृतं कर्म — The work is done.**
