# Yujp Web Profile

This directory captures the local DSH Web profile without credentials, sessions, caches, build output, or installed dependencies.

It includes the `dsh-mindmap` plugin source and the `PPT assistant` agent preset.

The profile was captured from a local `@deepseek-ai/dsh` `0.1.0-rc.8` installation. The root harness source may be newer, so update and validate the profile dependencies before using it with a different DSH release.

## Install

Build the local plugin, install the profile dependencies, then copy `presets/ppt-assistant` into `$DSH_HOME/.agent-presets/ppt-assistant` when the preset is wanted:

```sh
pnpm --dir profiles/yujp-web/packages/dsh-mindmap install --frozen-lockfile
pnpm --dir profiles/yujp-web/packages/dsh-mindmap run build
pnpm --dir profiles/yujp-web install --frozen-lockfile
```

The profile's `package.json` composes `dshmarket`, `dsh-find-plugin`, `dsh-office`, and the local mind-map plugin. Store provider credentials only in the DSH credentials domain or environment variables; do not add them to this profile.
