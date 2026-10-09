# Yujp Web Profile

[English](README.md) | 中文

本目录保存本地 DSH Web profile，不包含凭据、会话、缓存、构建产物或已安装依赖。

包含 `dsh-mindmap` 插件源码和 `PPT assistant` agent（智能体）预设。

该 profile 来自本地 `@deepseek-ai/dsh` `0.1.0-rc.8` 安装。根目录 harness 源码可能更新，使用其他 DSH 版本前应更新并验证 profile 依赖。

## 安装

构建本地插件、安装 profile 依赖，需要该预设时将 `presets/ppt-assistant` 复制到 `$DSH_HOME/.agent-presets/ppt-assistant`：

```sh
pnpm --dir profiles/yujp-web/packages/dsh-mindmap install --frozen-lockfile
pnpm --dir profiles/yujp-web/packages/dsh-mindmap run build
pnpm --dir profiles/yujp-web install --frozen-lockfile
```

profile 的 `package.json` 组合了 `dshmarket`、`dsh-find-plugin`、`dsh-office` 和本地思维导图插件。provider 凭据只保存在 DSH credentials domain 或环境变量中，不加入此 profile。
