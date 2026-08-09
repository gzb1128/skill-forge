# Makefile for skill-forge
#
# Skills in this repo live in plugins/<plugin-name>/skills/<name>/, following
# the Claude Code plugin directory layout.
# OpenCode subagents only discover skills from ~/.agents/skills/.
#
# To make this repo's skills discoverable by OpenCode subagents without
# copying files, we bridge them via symlinks to ~/.agents/skills/.
# See docs/verify/README.md for details.

PLUGIN_DIRS := $(wildcard $(CURDIR)/plugins/*)
SKILLS_SRC_DIRS := $(wildcard $(CURDIR)/plugins/*/skills)
SKILLS_DST := $(HOME)/.agents/skills
SKILL_VALIDATOR := $(CURDIR)/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py

.PHONY: help validate check-skills check-references sync-references test-skills-link test-skills-unlink test-skills-status

help:
	@echo "Targets:"
	@echo "  validate              run 'claude plugin validate' on marketplace + all plugins"
	@echo "  check-skills          validate every SKILL.md, including the description budget"
	@echo "  sync-references       fan plugin-level references/ into consuming skill dirs"
	@echo "  check-references      fail on reference fan-out drift (chained into validate)"
	@echo "  test-skills-link      symlink every skill into ~/.agents/skills/ (for GREEN tests)"
	@echo "  test-skills-unlink    remove those symlinks"
	@echo "  test-skills-status    show which symlinks currently exist"

validate: check-skills check-references
	claude plugin validate .
	@for plugin in $(PLUGIN_DIRS); do \
		if [ -d "$$plugin/.claude-plugin" ]; then \
			claude plugin validate "$$plugin" || exit $$?; \
		fi; \
	done

check-skills:
	@status=0; \
	for skills_dir in $(SKILLS_SRC_DIRS); do \
		for skill_dir in "$$skills_dir"/*/; do \
			[ -f "$$skill_dir/SKILL.md" ] || continue; \
			python3 "$(SKILL_VALIDATOR)" "$$skill_dir" --max-description-chars 300 || status=1; \
		done; \
	done; \
	exit $$status

# Fan the plugin-level shared references/ directory out into every skill that
# links references/<file> from its SKILL.md. Skills must be self-contained:
# installed skills are exposed one directory at a time (~/.agents/skills/<skill>,
# standalone .skill packages), and ../../ links do not survive that exposure.
# plugins/<plugin>/references/ stays the single editable source; commit the
# fanned-out copies together with the source edit.
sync-references:
	@for plugin in $(PLUGIN_DIRS); do \
		refs="$$plugin/references"; \
		[ -d "$$refs" ] || continue; \
		for skill_dir in "$$plugin"/skills/*/; do \
			[ -f "$$skill_dir/SKILL.md" ] || continue; \
			for ref in "$$refs"/*; do \
				[ -f "$$ref" ] || continue; \
				name=$$(basename "$$ref"); \
				grep -q "references/$$name" "$$skill_dir/SKILL.md" || continue; \
				mkdir -p "$$skill_dir/references" || exit 1; \
				cmp -s "$$ref" "$$skill_dir/references/$$name" && continue; \
				cp "$$ref" "$$skill_dir/references/$$name" || exit 1; \
				echo "SYNC $$skill_dir/references/$$name"; \
			done; \
		done; \
	done

# Drift gate for the fan-out above. Fails when a SKILL.md links a shared
# reference that has not been synced into that skill directory, when a synced
# copy differs from its plugin-level source, when a skill references/ copy
# has no plugin-level source anymore, or when a SKILL.md percent-encodes a
# references/ link (fan-out matches literal filenames). Never deletes
# anything; run make sync-references to re-copy, and remove orphans manually.
check-references:
	@status=0; \
	for plugin in $(PLUGIN_DIRS); do \
		refs="$$plugin/references"; \
		[ -d "$$refs" ] || continue; \
		for skill_dir in "$$plugin"/skills/*/; do \
			[ -f "$$skill_dir/SKILL.md" ] || continue; \
			if grep -qE '\]\(references/[^)]*%' "$$skill_dir/SKILL.md"; then \
				echo "BADLINK $$skill_dir/SKILL.md: percent-encoded references/ link; fan-out matches literal filenames"; \
				status=1; \
			fi; \
			for ref in "$$refs"/*; do \
				[ -f "$$ref" ] || continue; \
				name=$$(basename "$$ref"); \
				if grep -q "references/$$name" "$$skill_dir/SKILL.md" && [ ! -f "$$skill_dir/references/$$name" ]; then \
					echo "MISSING $$skill_dir/references/$$name (run make sync-references)"; \
					status=1; \
				fi; \
			done; \
			[ -d "$$skill_dir/references" ] || continue; \
			for copy in "$$skill_dir"/references/*; do \
				[ -f "$$copy" ] || continue; \
				name=$$(basename "$$copy"); \
				if [ ! -f "$$refs/$$name" ]; then \
					echo "ORPHAN  $$copy (no source at $$refs/$$name)"; \
					status=1; \
				elif ! cmp -s "$$refs/$$name" "$$copy"; then \
					echo "DRIFT   $$copy differs from $$refs/$$name (run make sync-references)"; \
					status=1; \
				fi; \
			done; \
		done; \
	done; \
	exit $$status

# Create symlinks at ~/.agents/skills/<name> for each plugin's skills/<name>/.
# The source is always the repo directory, so SKILL.md edits are immediately testable.
#
# Important: opencode's parent session skills registry is built at startup.
# After creating new symlinks, you must restart opencode (or start a new session)
# before subagents can see the new skills in <available_skills>.
# See docs/verify/README.md "Critical Timing Constraint" section.
test-skills-link:
	@mkdir -p $(SKILLS_DST)
	@for src_dir in $(SKILLS_SRC_DIRS); do \
		for name in $$(ls "$$src_dir" 2>/dev/null); do \
			src="$$src_dir/$$name"; \
			dst="$(SKILLS_DST)/$$name"; \
			if [ -e "$$dst" ] && [ ! -L "$$dst" ]; then \
				echo "SKIP $$name: $$dst exists and is NOT a symlink (refusing to overwrite real content)"; \
				continue; \
			fi; \
			ln -sfn "$$src" "$$dst"; \
			echo "LINK $$name -> $$src"; \
		done; \
	done
	@echo ""
	@echo "Next: restart opencode (or start a fresh session) so the skill"
	@echo "registry picks up the new entries before dispatching test subagents."

test-skills-unlink:
	@for src_dir in $(SKILLS_SRC_DIRS); do \
		for name in $$(ls "$$src_dir" 2>/dev/null); do \
			dst="$(SKILLS_DST)/$$name"; \
			if [ -L "$$dst" ]; then \
				rm "$$dst" && echo "UNLINK $$name"; \
			fi; \
		done; \
	done

test-skills-status:
	@for src_dir in $(SKILLS_SRC_DIRS); do \
		for name in $$(ls "$$src_dir" 2>/dev/null); do \
			dst="$(SKILLS_DST)/$$name"; \
			if [ -L "$$dst" ]; then \
				target=$$(readlink "$$dst"); \
				if [ "$$target" = "$$src_dir/$$name" ]; then \
					echo "OK    $$name -> $$target"; \
				else \
					echo "STALE $$name -> $$target (expected $$src_dir/$$name)"; \
				fi; \
			elif [ -e "$$dst" ]; then \
				echo "REAL  $$name (not a symlink — manual install?)"; \
			else \
				echo "MISS  $$name (run 'make test-skills-link')"; \
			fi; \
		done; \
	done
