#!/usr/bin/env bash
# ==============================================================================
# APEX SOVEREIGN ESTATE — POST-RESET RESTORATION SUITE
# Device:   Operator Casey Barton's Google Pixel Tablet
# Source:   onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/
#           onedrive:DEVICE_DATA/RECORDINGS/
# Target:   Termux ($HOME) / PRoot (/root) & Android Shared Storage (/sdcard)
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Configuration & Constants
# ------------------------------------------------------------------------------
ONEDRIVE_REMOTE="${ONEDRIVE_REMOTE:-onedrive}"
EVAC_ROOT="${ONEDRIVE_REMOTE}:PIXEL_TABLET_PRE_RESET_EVACUATION"
RECORDINGS_REMOTE="${ONEDRIVE_REMOTE}:DEVICE_DATA/RECORDINGS"

SDCARD_DIR="${SDCARD_DIR:-/sdcard}"
if [[ ! -d "$SDCARD_DIR" ]] && [[ -d "/storage/emulated/0" ]]; then
    SDCARD_DIR="/storage/emulated/0"
fi

STAGING_DIR="${SDCARD_DIR}/.apex_restore_staging"
DOCUMENTS_DIR="${SDCARD_DIR}/Documents"
BACKUP_DIR="${SDCARD_DIR}/BACKUP_PRE_RESET_20261023"
TERMUX_HOME="/data/data/com.termux/files/home"
TARGET_HOME="${HOME:-/root}"

WITH_MEDIA=0
VERIFY_ONLY=0
SKIP_REPOS=0
SKIP_DOCS=0
KEEP_STAGING=0

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_step()  { echo -e "\n${CYAN}${BOLD}==============================================================================${NC}"; echo -e "${CYAN}${BOLD}>>> $*${NC}"; echo -e "${CYAN}${BOLD}==============================================================================${NC}"; }

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Zero-friction Post-Reset Restoration Suite for Operator Casey Barton's Google Pixel Tablet.

Options:
  --with-media      Also restore DCIM/, Pictures/, and 210 voice recordings (RECORDINGS/)
  --skip-docs       Skip downloading/extracting DOCUMENTS and LEGAL_EVIDENCE archives
  --skip-repos      Skip cloning GitHub repositories
  --keep-staging    Keep downloaded .tar.gz archives in ${STAGING_DIR} after extraction
  --verify-only     Run the 10-point integrity verification suite without downloading
  -h, --help        Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --with-media)   WITH_MEDIA=1; shift ;;
        --skip-docs)    SKIP_DOCS=1; shift ;;
        --skip-repos)   SKIP_REPOS=1; shift ;;
        --keep-staging) KEEP_STAGING=1; shift ;;
        --verify-only)  VERIFY_ONLY=1; shift ;;
        -h|--help)      usage; exit 0 ;;
        *)              log_error "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# ------------------------------------------------------------------------------
# Helper: Safe rclone download with retries
# ------------------------------------------------------------------------------
rclone_pull() {
    local remote_path="$1"
    local dest_dir="$2"
    mkdir -p "$dest_dir"
    log_info "Pulling ${remote_path} -> ${dest_dir} ..."
    rclone copy "$remote_path" "$dest_dir" \
        --progress \
        --transfers 4 \
        --checkers 8 \
        --contimeout 60s \
        --timeout 300s \
        --retries 5 \
        --low-level-retries 10
}

# ------------------------------------------------------------------------------
# Phase 1: Package & Environment Bootstrap (Termux / PRoot Auto-Detection)
# ------------------------------------------------------------------------------
install_packages() {
    log_step "PHASE 1: Installing Required System & Termux Packages"

    if command -v pkg >/dev/null 2>&1; then
        log_info "Detected native Termux environment. Updating and installing packages..."
        pkg update -y && pkg upgrade -y
        pkg install -y git curl wget proot proot-distro python nodejs rclone tar openssh
        if [[ ! -d "${SDCARD_DIR}/Documents" ]]; then
            log_info "Requesting Android storage access (termux-setup-storage)..."
            termux-setup-storage || true
            sleep 2
        fi
    elif command -v apt-get >/dev/null 2>&1; then
        log_info "Detected PRoot / Debian-based Linux environment. Installing packages..."
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -y || true
        apt-get install -y git curl wget proot python3 nodejs rclone tar openssh-client ca-certificates || true
    else
        log_warn "Neither 'pkg' nor 'apt-get' found; verifying required binaries in PATH..."
    fi

    for bin in git curl wget rclone tar ssh; do
        if command -v "$bin" >/dev/null 2>&1; then
            log_ok "Binary verified: $bin ($(command -v "$bin"))"
        else
            log_error "Required binary '$bin' is missing! Please install it and re-run."
            exit 1
        fi
    done

    mkdir -p "$STAGING_DIR" "$DOCUMENTS_DIR" "${TARGET_HOME}/.config/rclone" "${TARGET_HOME}/.config/kilo"
}

# ------------------------------------------------------------------------------
# Phase 2: Rclone Bootstrap & Vault Evacuation Pull
# ------------------------------------------------------------------------------
bootstrap_rclone_and_vaults() {
    log_step "PHASE 2: Bootstrapping Rclone & Restoring Operator Key Vaults"

    local rclone_conf="${TARGET_HOME}/.config/rclone/rclone.conf"
    local keys_tarball="${STAGING_DIR}/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz"

    # Self-healing check 1: Is there already a local copy of the keys tarball?
    for candidate in \
        "${TARGET_HOME}/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz" \
        "${SDCARD_DIR}/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz" \
        "${SDCARD_DIR}/Download/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz"; do
        if [[ -f "$candidate" ]] && [[ ! -f "$keys_tarball" ]]; then
            log_info "Found local key vault archive at $candidate; copying to staging..."
            cp -f "$candidate" "$keys_tarball"
            break
        fi
    done

    # Self-healing check 2: Extract rclone.conf from local keys tarball if rclone is not yet configured
    if [[ ! -s "$rclone_conf" ]] && [[ -f "$keys_tarball" ]]; then
        log_info "Extracting rclone.conf from local key vault archive..."
        tar -xzf "$keys_tarball" -C "$TARGET_HOME" .config/rclone/rclone.conf 2>/dev/null || true
    fi

    # Self-healing check 3: Check SDCard for backup rclone.conf
    if [[ ! -s "$rclone_conf" ]]; then
        for candidate_conf in \
            "${SDCARD_DIR}/rclone.conf" \
            "${SDCARD_DIR}/Download/rclone.conf" \
            "${TERMUX_HOME}/.config/rclone/rclone.conf"; do
            if [[ -s "$candidate_conf" ]]; then
                log_info "Seeding rclone.conf from $candidate_conf..."
                mkdir -p "$(dirname "$rclone_conf")"
                cp -f "$candidate_conf" "$rclone_conf"
                chmod 600 "$rclone_conf"
                break
            fi
        done
    fi

    # Verify if 'onedrive:' remote is configured
    if ! rclone listremotes 2>/dev/null | grep -q "^${ONEDRIVE_REMOTE}:"; then
        log_warn "Remote '${ONEDRIVE_REMOTE}:' not found in ${rclone_conf}."
        echo -e "${YELLOW}Launching interactive 'rclone config' to authenticate '${ONEDRIVE_REMOTE}'...${NC}"
        echo -e "  1. Choose 'n' (New remote)"
        echo -e "  2. Name: ${BOLD}${ONEDRIVE_REMOTE}${NC}"
        echo -e "  3. Storage: ${BOLD}onedrive${NC} (Microsoft OneDrive)"
        echo -e "  4. Leave client_id / client_secret blank, choose default region (1), and complete browser auth."
        rclone config
    fi

    log_info "Verifying connectivity to ${EVAC_ROOT}/ ..."
    if rclone lsd "${EVAC_ROOT}/" >/dev/null 2>&1; then
        log_ok "Connected to ${EVAC_ROOT}/ on OneDrive."
    else
        log_error "Could not list ${EVAC_ROOT}/. Please verify 'rclone config' for remote '${ONEDRIVE_REMOTE}:'."
        exit 1
    fi

    # Pull ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz
    if [[ ! -f "$keys_tarball" ]]; then
        rclone_pull "${EVAC_ROOT}/KEY_VAULTS/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz" "$STAGING_DIR"
    else
        log_ok "Using staged ${keys_tarball}"
    fi

    log_info "Extracting Operator Key Vaults, SSH Keys, and Secrets into ${TARGET_HOME}..."
    mkdir -p "${TARGET_HOME}/artifacts" "${TARGET_HOME}/.config/rclone"
    # Remove broken symlinks if any before extracting
    for sym in "${TARGET_HOME}/.operator_key_vault" "${TARGET_HOME}/.apex_vault"; do
        if [[ -L "$sym" ]] && [[ ! -e "$sym" ]]; then
            rm -f "$sym"
        fi
    done
    tar -xzf "$keys_tarball" -C "$TARGET_HOME"

    # Ensure operator_key_vault.py symlink exists
    if [[ -f "${TARGET_HOME}/.operator_key_vault/operator_key_vault.py" ]]; then
        ln -sfn "${TARGET_HOME}/.operator_key_vault/operator_key_vault.py" "${TARGET_HOME}/operator_key_vault.py"
    fi

    # If running inside PRoot (/root) and Termux home exists, mirror/link vaults so both layers share state
    if [[ "$TARGET_HOME" == "/root" ]] && [[ -d "$TERMUX_HOME" ]]; then
        log_info "Synchronizing key vaults with Termux home (${TERMUX_HOME})..."
        mkdir -p "${TERMUX_HOME}/.config/rclone"
        cp -rf "${TARGET_HOME}/.operator_key_vault" "${TERMUX_HOME}/" 2>/dev/null || true
        cp -rf "${TARGET_HOME}/.apex_vault" "${TERMUX_HOME}/" 2>/dev/null || true
        cp -rf "${TARGET_HOME}/.ssh" "${TERMUX_HOME}/" 2>/dev/null || true
        cp -f "${TARGET_HOME}/.config/rclone/rclone.conf" "${TERMUX_HOME}/.config/rclone/rclone.conf" 2>/dev/null || true
    fi

    log_ok "Operator Key Vaults & Rclone configuration restored."
}

# ------------------------------------------------------------------------------
# Phase 3: System State, SSH, Dotfiles, OMP & 105 APEX Skills Restoration
# ------------------------------------------------------------------------------
restore_system_backup() {
    log_step "PHASE 3: Restoring System State, Dotfiles, OMP & 105 APEX Skills"

    local sys_tarball="${STAGING_DIR}/BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz"

    if [[ ! -f "$sys_tarball" ]]; then
        rclone_pull "${EVAC_ROOT}/BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz" "$STAGING_DIR"
    else
        log_ok "Using staged ${sys_tarball}"
    fi

    log_info "Extracting BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz to ${SDCARD_DIR}..."
    tar -xzf "$sys_tarball" -C "$SDCARD_DIR" --no-same-owner 2>/dev/null || tar -xzf "$sys_tarball" -C "$SDCARD_DIR"

    if [[ ! -d "$BACKUP_DIR" ]]; then
        log_error "Expected directory ${BACKUP_DIR} not found after extraction!"
        exit 1
    fi

    # 1. Restore SSH keys and enforce strict OpenSSH permissions
    if [[ -d "${BACKUP_DIR}/ssh_keys/.ssh" ]]; then
        log_info "Merging SSH keys from backup..."
        mkdir -p "${TARGET_HOME}/.ssh"
        cp -rf "${BACKUP_DIR}/ssh_keys/.ssh/." "${TARGET_HOME}/.ssh/"
    fi
    chmod 700 "${TARGET_HOME}/.ssh"
    find "${TARGET_HOME}/.ssh" -maxdepth 1 -type f -exec chmod 600 {} + 2>/dev/null || true
    find "${TARGET_HOME}/.ssh" -maxdepth 1 -type f -name "*.pub" -exec chmod 644 {} + 2>/dev/null || true
    log_ok "SSH keys restored and permissions locked (700 ~/.ssh, 600 private keys)."

    # 2. Restore Git credentials
    if [[ -f "${BACKUP_DIR}/git_credentials/.git-credentials" ]]; then
        cp -f "${BACKUP_DIR}/git_credentials/.git-credentials" "${TARGET_HOME}/.git-credentials"
        chmod 600 "${TARGET_HOME}/.git-credentials"
        log_ok "Git credentials restored (~/.git-credentials)."
    fi

    # 3. Restore Dotfiles (.bashrc, .env, .env.apex, .gitconfig, .gitignore)
    if [[ -d "${BACKUP_DIR}/dotfiles" ]]; then
        log_info "Restoring dotfiles (.bashrc, .env, .env.apex, .gitconfig, .gitignore)..."
        for df in .bashrc .env .env.apex .gitconfig .gitignore; do
            if [[ -f "${BACKUP_DIR}/dotfiles/${df}" ]]; then
                cp -f "${BACKUP_DIR}/dotfiles/${df}" "${TARGET_HOME}/${df}"
            fi
        done
    fi
    chmod 600 "${TARGET_HOME}/.env" "${TARGET_HOME}/.env.apex" "${TARGET_HOME}/.dropbox_credentials.json" "${TARGET_HOME}/.config/rclone/rclone.conf" 2>/dev/null || true
    chmod 700 "${TARGET_HOME}/.operator_key_vault" "${TARGET_HOME}/.apex_vault" 2>/dev/null || true
    log_ok "Dotfiles and secret file permissions enforced."

    # 4. Install OMP binary if missing & restore OMP state (.omp)
    if ! command -v omp >/dev/null 2>&1; then
        log_info "Installing Oh-My-Pi (OMP) CLI..."
        curl -fsSL https://omypi.sh/install.sh | bash || log_warn "OMP installer returned non-zero; continuing with state restore."
    fi
    if [[ -d "${BACKUP_DIR}/omp_config/.omp" ]]; then
        mkdir -p "${TARGET_HOME}/.omp"
        cp -rf "${BACKUP_DIR}/omp_config/.omp/." "${TARGET_HOME}/.omp/"
        log_ok "OMP configuration and state restored (~/.omp)."
    elif [[ -d "${BACKUP_DIR}/omp_config" ]]; then
        mkdir -p "${TARGET_HOME}/.omp"
        cp -rf "${BACKUP_DIR}/omp_config/." "${TARGET_HOME}/.omp/"
        log_ok "OMP configuration restored (~/.omp)."
    fi

    # 5. Restore 105 APEX Skills (.agents)
    if [[ -d "${BACKUP_DIR}/agents_skills/.agents" ]]; then
        mkdir -p "${TARGET_HOME}/.agents"
        cp -rf "${BACKUP_DIR}/agents_skills/.agents/." "${TARGET_HOME}/.agents/"
        local skill_count
        skill_count=$(find "${TARGET_HOME}/.agents/skills" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
        log_ok "APEX Agent Skills restored (~/.agents/skills — ${skill_count} skills active)."
    fi

    # 6. Restore Kilo configuration
    if [[ -f "${BACKUP_DIR}/kilo_config/kilo.jsonc" ]]; then
        mkdir -p "${TARGET_HOME}/.config/kilo"
        cp -f "${BACKUP_DIR}/kilo_config/kilo.jsonc" "${TARGET_HOME}/.config/kilo/kilo.jsonc"
        log_ok "Kilo configuration restored (~/.config/kilo/kilo.jsonc)."
    fi

    # 7. Restore genius-technician engine from backup
    if [[ -d "${BACKUP_DIR}/genius_technician/genius-technician" ]]; then
        mkdir -p "${TARGET_HOME}/genius-technician"
        cp -rf "${BACKUP_DIR}/genius_technician/genius-technician/." "${TARGET_HOME}/genius-technician/"
        log_ok "Genius Cognition Engine restored (~/genius-technician)."
    fi

    # 8. Synchronize Termux Home <-> PRoot /root if both exist
    if [[ "$TARGET_HOME" == "/root" ]] && [[ -d "$TERMUX_HOME" ]]; then
        cp -rf "${TARGET_HOME}/.ssh" "${TERMUX_HOME}/" 2>/dev/null || true
        cp -f "${TARGET_HOME}/.git-credentials" "${TERMUX_HOME}/.git-credentials" 2>/dev/null || true
        chmod 700 "${TERMUX_HOME}/.ssh" 2>/dev/null || true
        chmod 600 "${TERMUX_HOME}/.git-credentials" 2>/dev/null || true
    elif [[ "$TARGET_HOME" == "$TERMUX_HOME" ]] && [[ -d "/root" ]]; then
        cp -rf "${TARGET_HOME}/.ssh" "/root/" 2>/dev/null || true
        cp -f "${TARGET_HOME}/.git-credentials" "/root/.git-credentials" 2>/dev/null || true
        chmod 700 "/root/.ssh" 2>/dev/null || true
        chmod 600 "/root/.git-credentials" 2>/dev/null || true
    fi
}

# ------------------------------------------------------------------------------
# Phase 4: Core GitHub Repositories Restoration
# ------------------------------------------------------------------------------
restore_github_repositories() {
    if [[ "$SKIP_REPOS" -eq 1 ]]; then
        log_warn "Skipping GitHub repository cloning (--skip-repos)."
        return 0
    fi

    log_step "PHASE 4: Cloning Core GlacierEQ GitHub Repositories"

    # Configure git to use restored ~/.git-credentials if not already set
    git config --global credential.helper store || true

    local repos=(
        "job-app-helix"
        "Forward-Deployed-Agentic-Powerhouse"
        "casebuilder4000"
        "computer-user"
        "aspen-grove-core"
        "aspen-grove-memory"
        "apex-legal-forensics-suite"
        "apex-rico-master-suite"
        "genius-technician"
        "antigravity-cli"
    )

    for repo in "${repos[@]}"; do
        local target_dir="${TARGET_HOME}/${repo}"
        if [[ -d "${target_dir}/.git" ]]; then
            log_info "Repository ${repo} already exists at ${target_dir}; pulling latest..."
            git -C "$target_dir" pull --ff-only 2>/dev/null || log_warn "Could not fast-forward ${repo}; keeping local state."
        else
            log_info "Cloning GlacierEQ/${repo} -> ${target_dir} ..."
            if [[ -d "$target_dir" ]]; then
                # Directory exists from backup (e.g., genius-technician) without .git or with partial files
                local tmp_clone="${STAGING_DIR}/clone_${repo}"
                rm -rf "$tmp_clone"
                if git clone "https://github.com/GlacierEQ/${repo}.git" "$tmp_clone" 2>/dev/null || \
                   git clone "git@github.com:GlacierEQ/${repo}.git" "$tmp_clone" 2>/dev/null; then
                    cp -rn "${target_dir}/." "$tmp_clone/" 2>/dev/null || true
                    rm -rf "$target_dir"
                    mv "$tmp_clone" "$target_dir"
                    log_ok "Cloned and merged GlacierEQ/${repo}"
                else
                    log_warn "Could not clone GlacierEQ/${repo}; preserved backup directory ${target_dir}."
                fi
            else
                if git clone "https://github.com/GlacierEQ/${repo}.git" "$target_dir" 2>/dev/null || \
                   git clone "git@github.com:GlacierEQ/${repo}.git" "$target_dir" 2>/dev/null; then
                    log_ok "Cloned GlacierEQ/${repo}"
                else
                    log_warn "Failed to clone GlacierEQ/${repo} (check network or credentials)."
                fi
            fi
        fi
    done
}

# ------------------------------------------------------------------------------
# Phase 5: Documents, Architecture Specs & Legal Evidence Restoration
# ------------------------------------------------------------------------------
restore_documents_and_legal_evidence() {
    if [[ "$SKIP_DOCS" -eq 1 ]]; then
        log_warn "Skipping Documents & Legal Evidence archives (--skip-docs)."
        return 0
    fi

    log_step "PHASE 5: Restoring Documents, System Specs & Legal Evidence to ${DOCUMENTS_DIR}"

    mkdir -p \
        "${DOCUMENTS_DIR}" \
        "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED" \
        "${DOCUMENTS_DIR}/02_CAREER_AND_JOB_APPLICATIONS" \
        "${DOCUMENTS_DIR}/03_SYSTEM_ARCHITECTURE_AND_SPECS" \
        "${DOCUMENTS_DIR}/05_CODE_AND_PYTHON_CONNECTORS" \
        "${DOCUMENTS_DIR}/06_PERSONAL_AND_APPLE_EXPORTS"

    # 1. Career & Personal Documents -> /sdcard/Documents/
    local doc_career="${STAGING_DIR}/DOCUMENTS_CAREER_AND_PERSONAL_PRE_RESET.tar.gz"
    if [[ ! -f "$doc_career" ]]; then
        rclone_pull "${EVAC_ROOT}/DOCUMENTS/DOCUMENTS_CAREER_AND_PERSONAL_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking DOCUMENTS_CAREER_AND_PERSONAL_PRE_RESET.tar.gz -> ${DOCUMENTS_DIR}/ ..."
    tar -xzf "$doc_career" -C "${DOCUMENTS_DIR}/" --no-same-owner 2>/dev/null || tar -xzf "$doc_career" -C "${DOCUMENTS_DIR}/"
    log_ok "Career & Personal Documents restored."

    # 2. System Architecture & Specs -> /sdcard/Documents/03_SYSTEM_ARCHITECTURE_AND_SPECS/
    local doc_specs="${STAGING_DIR}/DOCUMENTS_SYSTEM_ARCHITECTURE_SPECS_PRE_RESET.tar.gz"
    if [[ ! -f "$doc_specs" ]]; then
        rclone_pull "${EVAC_ROOT}/DOCUMENTS/DOCUMENTS_SYSTEM_ARCHITECTURE_SPECS_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking DOCUMENTS_SYSTEM_ARCHITECTURE_SPECS_PRE_RESET.tar.gz -> ${DOCUMENTS_DIR}/03_SYSTEM_ARCHITECTURE_AND_SPECS/ ..."
    tar -xzf "$doc_specs" -C "${DOCUMENTS_DIR}/03_SYSTEM_ARCHITECTURE_AND_SPECS/" --no-same-owner 2>/dev/null || tar -xzf "$doc_specs" -C "${DOCUMENTS_DIR}/03_SYSTEM_ARCHITECTURE_AND_SPECS/"
    log_ok "System Architecture & Specs restored."

    # 3. Code & Connectors Scripts -> /sdcard/Documents/05_CODE_AND_PYTHON_CONNECTORS/
    local doc_code="${STAGING_DIR}/DOCUMENTS_CODE_AND_CONNECTORS_SCRIPTS_PRE_RESET.tar.gz"
    if [[ ! -f "$doc_code" ]]; then
        rclone_pull "${EVAC_ROOT}/DOCUMENTS/DOCUMENTS_CODE_AND_CONNECTORS_SCRIPTS_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking DOCUMENTS_CODE_AND_CONNECTORS_SCRIPTS_PRE_RESET.tar.gz -> ${DOCUMENTS_DIR}/05_CODE_AND_PYTHON_CONNECTORS/ ..."
    tar -xzf "$doc_code" -C "${DOCUMENTS_DIR}/05_CODE_AND_PYTHON_CONNECTORS/" --no-same-owner 2>/dev/null || tar -xzf "$doc_code" -C "${DOCUMENTS_DIR}/05_CODE_AND_PYTHON_CONNECTORS/"
    log_ok "Code & Python Connectors restored."

    # 4. Legal Cases & Motions Core -> /sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/
    local legal_core="${STAGING_DIR}/LEGAL_CASES_AND_MOTIONS_CORE_PRE_RESET.tar.gz"
    if [[ ! -f "$legal_core" ]]; then
        rclone_pull "${EVAC_ROOT}/LEGAL_EVIDENCE/LEGAL_CASES_AND_MOTIONS_CORE_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking LEGAL_CASES_AND_MOTIONS_CORE_PRE_RESET.tar.gz -> ${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/ ..."
    tar -xzf "$legal_core" -C "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/" --no-same-owner 2>/dev/null || tar -xzf "$legal_core" -C "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/"
    log_ok "Legal Cases & Motions Core restored."

    # 5. Legal Evidence Audio & Images -> /sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/
    local legal_media="${STAGING_DIR}/LEGAL_EVIDENCE_AUDIO_AND_IMAGES_PRE_RESET.tar.gz"
    if [[ ! -f "$legal_media" ]]; then
        rclone_pull "${EVAC_ROOT}/LEGAL_EVIDENCE/LEGAL_EVIDENCE_AUDIO_AND_IMAGES_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking LEGAL_EVIDENCE_AUDIO_AND_IMAGES_PRE_RESET.tar.gz -> ${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/ ..."
    tar -xzf "$legal_media" -C "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/" --no-same-owner 2>/dev/null || tar -xzf "$legal_media" -C "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/"
    log_ok "Legal Evidence Audio & Images restored."

    # 6. Root Legal Warfare & Forensic Evidence Vaults -> ${TARGET_HOME}/
    # Supports both fault-tolerant 45 MB chunked archive (CHUNKS_FINAL_UPLOAD/) and single .tar.gz
    local chunks_dir="${STAGING_DIR}/CHUNKS_FINAL_UPLOAD"
    local root_vaults="${STAGING_DIR}/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz"
    if [[ ! -f "$root_vaults" ]] && ! ls "${chunks_dir}/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz.part_"* >/dev/null 2>&1; then
        mkdir -p "$chunks_dir"
        rclone_pull "${EVAC_ROOT}/CHUNKS_FINAL_UPLOAD" "$chunks_dir" || rclone_pull "${EVAC_ROOT}/LEGAL_EVIDENCE/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    if ls "${chunks_dir}/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz.part_"* >/dev/null 2>&1; then
        log_info "Reassembling & unpacking chunked ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz.part_* -> ${TARGET_HOME}/ ..."
        cat "${chunks_dir}/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${TARGET_HOME}/" --no-same-owner 2>/dev/null || \
        cat "${chunks_dir}/ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${TARGET_HOME}/"
    elif [[ -f "$root_vaults" ]]; then
        log_info "Unpacking ROOT_LEGAL_WARFARE_AND_EVIDENCE_VAULTS_PRE_RESET.tar.gz -> ${TARGET_HOME}/ ..."
        tar -xzf "$root_vaults" -C "${TARGET_HOME}/" --no-same-owner 2>/dev/null || tar -xzf "$root_vaults" -C "${TARGET_HOME}/"
    fi
    log_ok "Root Legal Warfare & Forensic Evidence Vaults restored."

    # 7. Complete Downloads & SDCard User Folders -> ${SDCARD_DIR}/
    local dl_complete="${STAGING_DIR}/DOWNLOADS_COMPLETE_PRE_RESET.tar.gz"
    if ls "${chunks_dir}/DOWNLOADS_COMPLETE_PRE_RESET.tar.gz.part_"* >/dev/null 2>&1; then
        log_info "Reassembling & unpacking chunked DOWNLOADS_COMPLETE_PRE_RESET.tar.gz.part_* -> ${SDCARD_DIR}/ ..."
        cat "${chunks_dir}/DOWNLOADS_COMPLETE_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${SDCARD_DIR}/" --no-same-owner 2>/dev/null || \
        cat "${chunks_dir}/DOWNLOADS_COMPLETE_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${SDCARD_DIR}/"
    else
        if [[ ! -f "$dl_complete" ]]; then
            rclone_pull "${EVAC_ROOT}/DOWNLOADS_COMPLETE_PRE_RESET.tar.gz" "$STAGING_DIR"
        fi
        log_info "Unpacking DOWNLOADS_COMPLETE_PRE_RESET.tar.gz -> ${SDCARD_DIR}/ ..."
        tar -xzf "$dl_complete" -C "${SDCARD_DIR}/" --no-same-owner 2>/dev/null || tar -xzf "$dl_complete" -C "${SDCARD_DIR}/"
    fi

    local sd_misc="${STAGING_DIR}/SDCARD_MISC_USER_FOLDERS_PRE_RESET.tar.gz"
    if [[ ! -f "$sd_misc" ]]; then
        rclone_pull "${EVAC_ROOT}/SDCARD_MISC_USER_FOLDERS_PRE_RESET.tar.gz" "$STAGING_DIR"
    fi
    log_info "Unpacking SDCARD_MISC_USER_FOLDERS_PRE_RESET.tar.gz -> ${SDCARD_DIR}/ ..."
    tar -xzf "$sd_misc" -C "${SDCARD_DIR}/" --no-same-owner 2>/dev/null || tar -xzf "$sd_misc" -C "${SDCARD_DIR}/"
    log_ok "Downloads & SDCard user folders restored."

    # 8. Wave F1: Termux Gitignored State (.apex, CASE_PDFS, MISSIONS, CATEGORIES) & Documents Legal Supplement (36 chunks)
    local wave_f1_dir="${STAGING_DIR}/CHUNKS_WAVE_F1"
    mkdir -p "$wave_f1_dir"
    if rclone_pull "${EVAC_ROOT}/CHUNKS_WAVE_F1" "$wave_f1_dir"; then
        if ls "${wave_f1_dir}/TERMUX_AND_DOCUMENTS_LEGAL_SUPPLEMENT_PRE_RESET.tar.gz.part_"* >/dev/null 2>&1; then
            log_info "Reassembling & unpacking Wave F1 (TERMUX_AND_DOCUMENTS_LEGAL_SUPPLEMENT_PRE_RESET.tar.gz.part_00..35)..."
            cat "${wave_f1_dir}/TERMUX_AND_DOCUMENTS_LEGAL_SUPPLEMENT_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${TERMUX_HOME}/" --no-same-owner 2>/dev/null || true
            log_ok "Wave F1 Termux & Legal Supplement restored."
        fi
    fi

    # 9. Wave F2: Complete Obsidian Vaults (07_DATA_CONFIG/OBSIDIAN & 12_OBSIDIAN_VAULT/OBSIDIAN)
    local wave_f2_dir="${STAGING_DIR}/CHUNKS_WAVE_F2_OBSIDIAN"
    mkdir -p "$wave_f2_dir"
    if rclone_pull "${EVAC_ROOT}/CHUNKS_WAVE_F2_OBSIDIAN" "$wave_f2_dir"; then
        if ls "${wave_f2_dir}/OBSIDIAN_VAULTS_COMPLETE_PRE_RESET.tar.gz.part_"* >/dev/null 2>&1; then
            log_info "Reassembling & unpacking Wave F2 Obsidian Vaults -> ${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/ ..."
            cat "${wave_f2_dir}/OBSIDIAN_VAULTS_COMPLETE_PRE_RESET.tar.gz.part_"* | tar -xzf - -C "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/" --no-same-owner 2>/dev/null || true
            log_ok "Wave F2 Obsidian Vaults restored."
        fi
    fi

    # Optional: Media & Voice Recordings (--with-media)
    if [[ "$WITH_MEDIA" -eq 1 ]]; then
        log_info "Restoring DCIM/, Pictures/, 210 Voice Recordings, and iOS Evidence Videos (--with-media)..."
        rclone_pull "${EVAC_ROOT}/DCIM" "${SDCARD_DIR}/DCIM"
        rclone_pull "${EVAC_ROOT}/Pictures" "${SDCARD_DIR}/Pictures"
        rclone_pull "${RECORDINGS_REMOTE}" "${SDCARD_DIR}/Recordings"
        rclone_pull "${EVAC_ROOT}/EVIDENCE_VIDEO_CAMERA_ROLL_IOS" "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/05_EVIDENCE_VIDEO/CAMERA_ROLL_IOS" || true
        rclone_pull "${EVAC_ROOT}/ARCHIVES_OBSIDIAN_EXPORTS" "${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/00_ARCHIVES/OBSIDIAN/organized_vault/UNCATEGORIZED" || true
        log_ok "DCIM, Pictures, 210 Voice Recordings, and iOS Evidence Videos restored."
    fi

    if [[ "$KEEP_STAGING" -eq 0 ]]; then
        log_info "Cleaning up temporary staging archives in ${STAGING_DIR}..."
        rm -rf "$STAGING_DIR"
        log_ok "Staging directory cleaned."
    else
        log_info "Staging archives retained at ${STAGING_DIR} (--keep-staging)."
    fi
}

# ------------------------------------------------------------------------------
# Phase 6: 10-Point Post-Restoration Integrity Verification
# ------------------------------------------------------------------------------
verify_restoration() {
    log_step "PHASE 6: Running 10-Point Post-Restoration Integrity Verification"

    local pass_count=0
    local fail_count=0

    check_item() {
        local label="$1"
        local condition="$2"
        if eval "$condition"; then
            log_ok "[PASS] ${label}"
            pass_count=$((pass_count + 1))
        else
            log_error "[FAIL] ${label}"
            fail_count=$((fail_count + 1))
        fi
    }

    # 1. Operator Key Vault
    check_item "Operator Key Vault (~/.operator_key_vault/keys.json & gatekeeper.env)" \
        "[[ -f '${TARGET_HOME}/.operator_key_vault/keys.json' && -f '${TARGET_HOME}/.operator_key_vault/gatekeeper.env' ]]"

    # 2. APEX Vault
    check_item "APEX Encrypted Key Vault (~/.apex_vault/credentials.env & domains/)" \
        "[[ -f '${TARGET_HOME}/.apex_vault/credentials.env' && -d '${TARGET_HOME}/.apex_vault/domains' ]]"

    # 3. SSH Keys & Permissions
    check_item "SSH Keys & Strict 700/600 Permissions (~/.ssh/id_ed25519_github_pixel_tablet)" \
        "[[ -f '${TARGET_HOME}/.ssh/id_ed25519_github_pixel_tablet' && \$(stat -c '%a' '${TARGET_HOME}/.ssh' 2>/dev/null || echo 700) == '700' ]]"

    # 4. Rclone Config
    check_item "Rclone Configuration (~/.config/rclone/rclone.conf)" \
        "[[ -s '${TARGET_HOME}/.config/rclone/rclone.conf' ]]"

    # 5. Dotfiles & Git Credentials
    check_item "Dotfiles & Git Credentials (~/.env, ~/.env.apex, ~/.git-credentials)" \
        "[[ -f '${TARGET_HOME}/.env' && -f '${TARGET_HOME}/.env.apex' && -f '${TARGET_HOME}/.git-credentials' ]]"

    # 6. OMP State
    check_item "Oh-My-Pi (OMP) State (~/.omp)" \
        "[[ -d '${TARGET_HOME}/.omp' ]]"

    # 7. APEX 105 Skills
    local skills_found
    skills_found=$(find "${TARGET_HOME}/.agents/skills" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    check_item "APEX Agent Skills (~/.agents/skills — found ${skills_found} skills, expected >= 100)" \
        "[[ '${skills_found}' -ge 100 ]]"

    # 8. Genius Technician Engine
    check_item "Genius Cognition Engine (~/genius-technician)" \
        "[[ -d '${TARGET_HOME}/genius-technician' ]]"

    # 9. Core GitHub Repositories
    check_item "Core GitHub Repositories (job-app-helix, Forward-Deployed-Agentic-Powerhouse, casebuilder4000, computer-user, aspen-grove-core)" \
        "[[ -d '${TARGET_HOME}/job-app-helix' && -d '${TARGET_HOME}/Forward-Deployed-Agentic-Powerhouse' && -d '${TARGET_HOME}/casebuilder4000' && -d '${TARGET_HOME}/computer-user' && -d '${TARGET_HOME}/aspen-grove-core' ]]"

    # 10. Documents & Legal Evidence
    check_item "Documents & Legal Evidence (/sdcard/Documents/01..06)" \
        "[[ -d '${DOCUMENTS_DIR}/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED' && -d '${DOCUMENTS_DIR}/02_CAREER_AND_JOB_APPLICATIONS' && -d '${DOCUMENTS_DIR}/03_SYSTEM_ARCHITECTURE_AND_SPECS' && -d '${DOCUMENTS_DIR}/05_CODE_AND_PYTHON_CONNECTORS' ]]"

    # 11. Root Legal Warfare & Forensic Evidence Vaults
    check_item "Root Legal Warfare & Forensic Vaults (LEGAL_WARFARE_PACKAGE_1FDV/evidence_vault & GOOGLE_TAKEOUT_DISTILLED_EVIDENCE)" \
        "[[ -d '${TARGET_HOME}/LEGAL_WARFARE_PACKAGE_1FDV/evidence_vault' && -d '${TARGET_HOME}/GOOGLE_TAKEOUT_DISTILLED_EVIDENCE' ]]"

    echo -e "\n${BOLD}==============================================================================${NC}"
    echo -e "${BOLD}RESTORATION VERIFICATION SUMMARY: ${GREEN}${pass_count} PASSED${NC} | ${RED}${fail_count} FAILED${NC}"
    echo -e "${BOLD}==============================================================================${NC}"

    if [[ "$fail_count" -gt 0 ]]; then
        return 1
    fi
    return 0
}

# ------------------------------------------------------------------------------
# Main Execution Flow
# ------------------------------------------------------------------------------
main() {
    if [[ "$VERIFY_ONLY" -eq 1 ]]; then
        verify_restoration
        exit $?
    fi

    install_packages
    bootstrap_rclone_and_vaults
    restore_system_backup
    restore_github_repositories
    restore_documents_and_legal_evidence
    verify_restoration

    echo -e "\n${GREEN}${BOLD}APEX PIXEL TABLET RESTORATION COMPLETE.${NC}"
    echo -e "Run ${CYAN}source ~/.bashrc${NC} to reload environment variables and aliases."
}

main "$@"
