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
