# dotfiles

Personal config files managed with [GNU Stow](https://www.gnu.org/software/stow/).

## Packages

| Package | Files |
|---------|-------|
| `tmux`  | `~/.tmux.conf` |
| `vim`   | `~/.vimrc` |
| `claude` | `~/.claude/commands/` |

## Usage

**Bootstrap a new machine** (after cloning the repo):
```
make install
```
Installs stow if missing, then symlinks all packages to `$HOME`.

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
