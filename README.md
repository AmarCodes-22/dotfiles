# dotfiles

Personal config files managed with [GNU Stow](https://www.gnu.org/software/stow/).

## Packages

| Package | Files |
|---------|-------|
| `tmux`  | `~/.tmux.conf` |
| `vim`   | `~/.vimrc` |
| `claude` | `~/.claude/commands/`, `~/.claude/settings.json` |

## Usage

**Bootstrap a new machine** (after cloning the repo):
```
make install
```
Installs stow if missing, then symlinks all packages to `$HOME`.

> **Note (claude package):** stow can't manage `~/.claude` directly since it contains Claude's runtime data. After `make install`, manually symlink the claude configs:
> ```bash
> mkdir -p ~/.claude
> ln -sf $(PWD)/claude/.claude/commands ~/.claude/commands
> ln -sf $(PWD)/claude/.claude/settings.json ~/.claude/settings.json
> ```

**Sync changes to GitHub:**
```
make sync
```
Stages everything, commits with a timestamp, and pushes.

## Adding a new package

```bash
mkdir ~/dev/dotfiles/<package>
mv ~/.<config> ~/dev/dotfiles/<package>/.<config>
# add <package> to PACKAGES in Makefile
make sync
```
