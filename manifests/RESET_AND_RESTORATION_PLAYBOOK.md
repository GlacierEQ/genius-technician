# Google Pixel Tablet — Cloud-Backed Factory Reset & Restoration Playbook

**Operator:** Casey Barton (`GlacierEQ`)  
**Target Device:** Google Pixel Tablet (Android / Termux / PRoot Linux)  
**Primary Cloud Evacuation Vault:** `onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/`  
**Secondary Voice Archive:** `onedrive:DEVICE_DATA/RECORDINGS/` (210 Voice Recordings)  
**Automated Restoration Script:** `/root/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh` (mirrored at `/sdcard/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh` and `onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/`)

---

## 1. Cloud Evacuation Manifest (`onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/`)

All critical keys, system configurations, AI skills, legal evidence, and career documents have been packaged and evacuated to Microsoft OneDrive:

| Cloud Archive Path | Unpacked Destination | Contents Summary |
| :--- | :--- | :--- |
| `KEY_VAULTS/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz` | `~/` (`/root` & Termux `$HOME`) | `.operator_key_vault/`, `.apex_vault/`, `.ssh/`, `.env`, `.env.apex`, `.dropbox_credentials.json`, `artifacts/apex_vault_bundle_ENCRYPTED.bin`, `.config/rclone/rclone.conf` |
| `BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz` | `/sdcard/BACKUP_PRE_RESET_20261023/` -> `~/` | `ssh_keys/.ssh`, `git_credentials/.git-credentials`, `dotfiles/`, `omp_config/.omp`, `agents_skills/.agents` (105 skills), `kilo_config/kilo.jsonc`, `genius_technician/genius-technician`, `legal_warfare`, `legal_mesh`, `dhhi_omnibus`, `google_takeout`, `higuy_vids`, `onedrive_case`, `onedrive_forensics`, `manifests` |
| `DOCUMENTS/DOCUMENTS_CAREER_AND_PERSONAL_PRE_RESET.tar.gz` | `/sdcard/Documents/` | `02_CAREER_AND_JOB_APPLICATIONS/`, `06_PERSONAL_AND_APPLE_EXPORTS/`, `moshi-sync.json` |
| `DOCUMENTS/DOCUMENTS_SYSTEM_ARCHITECTURE_SPECS_PRE_RESET.tar.gz` | `/sdcard/Documents/03_SYSTEM_ARCHITECTURE_AND_SPECS/` | System prompts, Aionic Tree, APEX Mission Control, Sigma Federation specs |
| `DOCUMENTS/DOCUMENTS_CODE_AND_CONNECTORS_SCRIPTS_PRE_RESET.tar.gz` | `/sdcard/Documents/05_CODE_AND_PYTHON_CONNECTORS/` | `CONFIGS/`, `SCRIPTS/`, `SETUP/`, `connectors.py`, `glaciereq_hourly_agent_v3.py`, `load-mimocode.sh` |
| `LEGAL_EVIDENCE/LEGAL_CASES_AND_MOTIONS_CORE_PRE_RESET.tar.gz` | `/sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/` | `02_LEGAL_CASES/` (`1FDV-23-0001009` motions, filings, proof matrices, Obsidian vault, spreadsheets) |
| `LEGAL_EVIDENCE/LEGAL_EVIDENCE_AUDIO_AND_IMAGES_PRE_RESET.tar.gz` | `/sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/` | `03_EVIDENCE_IMAGES/`, `04_EVIDENCE_AUDIO/`, `04_EVIDENCE_AUDIO_TRANSCRIPTS_BATCH/`, `05_EVIDENCE_VIDEO/` |
| `DCIM/` & `Pictures/` | `/sdcard/DCIM/` & `/sdcard/Pictures/` | Camera roll, screenshots, and visual evidence captures |
| `onedrive:DEVICE_DATA/RECORDINGS/` | `/sdcard/Recordings/` | 210 forensic and operational voice recordings |

---

## 2. Phase 1: Execute Android Factory Reset

1. Verify that all active `rclone` evacuation transfers have completed (`100%`).
2. On the Google Pixel Tablet, open **Settings > System > Reset options > Erase all data (factory reset)**.
3. Confirm erasure and allow the device to wipe and reboot.
4. Complete initial Android setup (connect to Wi-Fi, sign into Google account).

---

## 3. Phase 2: One-Command Automated Cloud Restoration (Recommended)

After the factory reset, install **Termux** (from F-Droid or GitHub Releases), open a terminal session, and run:

```bash
# 1. Bootstrap core packages & storage permissions in Termux
pkg update -y && pkg upgrade -y
pkg install -y git curl wget proot proot-distro python nodejs rclone tar openssh
termux-setup-storage

# 2. Authenticate rclone with OneDrive (skip if copying saved rclone.conf)
rclone config
# -> Choose 'n' (New remote) -> Name: onedrive -> Storage: onedrive -> Complete browser auth

# 3. Pull the Restoration Suite from OneDrive and execute it
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh ~/
chmod +x ~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh
~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh
```

### Supported Script Flags
- `~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh` — Full restoration of vaults, SSH keys, dotfiles, OMP, 105 APEX skills, `genius-technician`, core GitHub repos, and all `DOCUMENTS` + `LEGAL_EVIDENCE` archives, followed by 10-point verification.
- `~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh --with-media` — Also pulls `DCIM/`, `Pictures/`, and `onedrive:DEVICE_DATA/RECORDINGS/` (210 voice recordings).
- `~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh --verify-only` — Runs the 10-point Post-Restoration Integrity Verification Suite without downloading.
- `~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh --keep-staging` — Retains the downloaded `.tar.gz` archives in `/sdcard/.apex_restore_staging/`.

---

## 4. Phase 3: Manual Step-by-Step Restoration Reference

If executing any restoration stage manually, use the exact commands below:

### Step 3.1: Pull & Extract Key Vaults and Rclone Config
```bash
mkdir -p /sdcard/.apex_restore_staging ~/.config/rclone ~/artifacts
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/KEY_VAULTS/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz /sdcard/.apex_restore_staging/ --progress
tar -xzf /sdcard/.apex_restore_staging/ROOT_OPERATOR_KEYS_AND_SECRETS_PRE_RESET.tar.gz -C ~/
ln -sfn ~/.operator_key_vault/operator_key_vault.py ~/operator_key_vault.py
chmod 700 ~/.operator_key_vault ~/.apex_vault ~/.ssh
chmod 600 ~/.ssh/* ~/.env ~/.env.apex ~/.dropbox_credentials.json ~/.config/rclone/rclone.conf 2>/dev/null || true
chmod 644 ~/.ssh/*.pub 2>/dev/null || true
```

### Step 3.2: Pull & Extract System State, OMP, and 105 APEX Skills
```bash
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz /sdcard/.apex_restore_staging/ --progress
tar -xzf /sdcard/.apex_restore_staging/BACKUP_PRE_RESET_20261023_PERMISSIONS_PRESERVED.tar.gz -C /sdcard/ --no-same-owner

# Restore SSH keys, Git credentials, and dotfiles
cp -rf /sdcard/BACKUP_PRE_RESET_20261023/ssh_keys/.ssh/. ~/.ssh/
chmod 700 ~/.ssh && chmod 600 ~/.ssh/* && chmod 644 ~/.ssh/*.pub 2>/dev/null || true
cp -f /sdcard/BACKUP_PRE_RESET_20261023/git_credentials/.git-credentials ~/.git-credentials
chmod 600 ~/.git-credentials
cp -f /sdcard/BACKUP_PRE_RESET_20261023/dotfiles/.bashrc ~/
cp -f /sdcard/BACKUP_PRE_RESET_20261023/dotfiles/.env ~/
cp -f /sdcard/BACKUP_PRE_RESET_20261023/dotfiles/.env.apex ~/
cp -f /sdcard/BACKUP_PRE_RESET_20261023/dotfiles/.gitconfig ~/
cp -f /sdcard/BACKUP_PRE_RESET_20261023/dotfiles/.gitignore ~/

# Install OMP and restore OMP state, 105 APEX skills, Kilo config, and Genius Technician
curl -fsSL https://omypi.sh/install.sh | bash
mkdir -p ~/.omp ~/.agents ~/.config/kilo ~/genius-technician
cp -rf /sdcard/BACKUP_PRE_RESET_20261023/omp_config/.omp/. ~/.omp/
cp -rf /sdcard/BACKUP_PRE_RESET_20261023/agents_skills/.agents/. ~/.agents/
cp -f /sdcard/BACKUP_PRE_RESET_20261023/kilo_config/kilo.jsonc ~/.config/kilo/kilo.jsonc
cp -rf /sdcard/BACKUP_PRE_RESET_20261023/genius_technician/genius-technician/. ~/genius-technician/
```

### Step 3.3: Clone Core GitHub Repositories (`GlacierEQ/*`)
```bash
git config --global credential.helper store
for repo in \
  job-app-helix \
  Forward-Deployed-Agentic-Powerhouse \
  casebuilder4000 \
  computer-user \
  aspen-grove-core \
  aspen-grove-memory \
  apex-legal-forensics-suite \
  apex-rico-master-suite \
  genius-technician \
  antigravity-cli; do
  git clone "https://github.com/GlacierEQ/${repo}.git" ~/"${repo}" || true
done
```

### Step 3.4: Pull & Unpack Documents and Legal Evidence into `/sdcard/Documents/`
```bash
mkdir -p \
  /sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED \
  /sdcard/Documents/02_CAREER_AND_JOB_APPLICATIONS \
  /sdcard/Documents/03_SYSTEM_ARCHITECTURE_AND_SPECS \
  /sdcard/Documents/05_CODE_AND_PYTHON_CONNECTORS \
  /sdcard/Documents/06_PERSONAL_AND_APPLE_EXPORTS

# Pull DOCUMENTS & LEGAL_EVIDENCE archives
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/DOCUMENTS/ /sdcard/.apex_restore_staging/ --progress
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/LEGAL_EVIDENCE/ /sdcard/.apex_restore_staging/ --progress

# Unpack into exact target directories
tar -xzf /sdcard/.apex_restore_staging/DOCUMENTS_CAREER_AND_PERSONAL_PRE_RESET.tar.gz -C /sdcard/Documents/ --no-same-owner
tar -xzf /sdcard/.apex_restore_staging/DOCUMENTS_SYSTEM_ARCHITECTURE_SPECS_PRE_RESET.tar.gz -C /sdcard/Documents/03_SYSTEM_ARCHITECTURE_AND_SPECS/ --no-same-owner
tar -xzf /sdcard/.apex_restore_staging/DOCUMENTS_CODE_AND_CONNECTORS_SCRIPTS_PRE_RESET.tar.gz -C /sdcard/Documents/05_CODE_AND_PYTHON_CONNECTORS/ --no-same-owner
tar -xzf /sdcard/.apex_restore_staging/LEGAL_CASES_AND_MOTIONS_CORE_PRE_RESET.tar.gz -C /sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/ --no-same-owner
tar -xzf /sdcard/.apex_restore_staging/LEGAL_EVIDENCE_AUDIO_AND_IMAGES_PRE_RESET.tar.gz -C /sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED/ --no-same-owner
```

### Step 3.5: Optional Media & Voice Recordings Restoration
```bash
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/DCIM /sdcard/DCIM --progress
rclone copy onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/Pictures /sdcard/Pictures --progress
rclone copy onedrive:DEVICE_DATA/RECORDINGS /sdcard/Recordings --progress
```

---

## 5. Phase 4: Post-Restoration Verification Checklist

Run `~/RESTORE_APEX_TABLET_FROM_ONEDRIVE.sh --verify-only` to automatically validate all 10 checkpoints:

1. **Operator Key Vault:** `~/.operator_key_vault/keys.json` & `~/.operator_key_vault/gatekeeper.env` present.
2. **APEX Vault:** `~/.apex_vault/credentials.env` & `~/.apex_vault/domains/` present.
3. **SSH Keys:** `~/.ssh/id_ed25519_github_pixel_tablet` present with `700` directory / `600` key permissions.
4. **Rclone Config:** `~/.config/rclone/rclone.conf` active and authenticated.
5. **Dotfiles & Git Auth:** `~/.env`, `~/.env.apex`, `~/.bashrc`, `~/.gitconfig`, and `~/.git-credentials` restored.
6. **OMP Runtime:** `~/.omp` state directory restored.
7. **APEX Skills:** `find ~/.agents/skills -maxdepth 2 -name "SKILL.md" | wc -l` returns `105`.
8. **Genius Cognition Engine:** `~/genius-technician` directory intact.
9. **Core GitHub Repositories:** `job-app-helix`, `Forward-Deployed-Agentic-Powerhouse`, `casebuilder4000`, `computer-user`, and `aspen-grove-core` cloned in `~/`.
10. **Documents & Legal Evidence:** `/sdcard/Documents/01_LEGAL_AND_CASE_EVIDENCE/_ORGANIZED`, `02_CAREER_AND_JOB_APPLICATIONS`, `03_SYSTEM_ARCHITECTURE_AND_SPECS`, and `05_CODE_AND_PYTHON_CONNECTORS` populated.
