# Yujp Web Profile

English | [中文](README.zh.md)

This directory captures the local DSH Web profile without credentials, sessions, caches, build output, or installed dependencies.

It includes the `dsh-mindmap` plugin source and the `PPT assistant` agent preset.

The PPT preset is validated on `@deepseek-ai/dsh` `0.2.1-alpha.1`, using the persona `prefix` field and the PTC workflow spawn provider. Its built-in Python PPT engine remains independent of optional profile plugins.

The captured optional dependencies still target older DSH releases. With `0.2.1-alpha.1`, the installed `@huiliyi37/dsh-office@0.2.4` and `dsh-find-plugin@0.3.7` are skipped by the compatibility check; their latest published versions do not declare support for this runtime either. The captured mind-map plugin also retains older peer dependencies. Install compatible plugin releases before relying on those capabilities; the PPT preset mount test does not validate these optional plugins.

## Install

Build the local plugin, install the profile dependencies, then copy `presets/ppt-assistant` into `$DSH_HOME/.agent-presets/ppt-assistant` when the preset is wanted:

```sh
pnpm --dir profiles/yujp-web/packages/dsh-mindmap install --frozen-lockfile
pnpm --dir profiles/yujp-web/packages/dsh-mindmap run build
pnpm --dir profiles/yujp-web install --frozen-lockfile
```

The profile's `package.json` composes `dshmarket`, `dsh-find-plugin`, `dsh-office`, and the local mind-map plugin. Store provider credentials only in the DSH credentials domain or environment variables; do not add them to this profile.
