PACKAGES := tmux vim claude

.PHONY: sync install

sync:
	git add .
	git diff --cached --quiet || git commit -m "sync: $(shell date '+%Y-%m-%d %H:%M')"
	git push

install:
	@command -v stow >/dev/null 2>&1 || { \
		if [ "$$(uname)" = "Darwin" ]; then brew install stow; \
		else sudo apt-get install -y stow; fi; \
	}
	stow --target=$(HOME) $(PACKAGES)
	# TODO: stow can't handle claude individually since ~/.claude has runtime data.
	# Manually symlink after install:
	#   mkdir -p ~/.claude
	#   ln -sf $(PWD)/claude/.claude/commands ~/.claude/commands
	#   ln -sf $(PWD)/claude/.claude/settings.json ~/.claude/settings.json
