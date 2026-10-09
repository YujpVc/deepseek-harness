# Yujp Web Profile

[English](README.md) | 中文

本目录保存本地 DSH Web profile，不包含凭据、会话、缓存、构建产物或已安装依赖。

包含 `dsh-mindmap` 插件源码和 `PPT assistant` agent（智能体）预设。

PPT 预设已在 `@deepseek-ai/dsh` `0.2.1-alpha.1` 上验证，使用人设 `prefix` 字段和 PTC workflow spawn provider。内置 Python PPT 引擎独立于 profile 的可选插件。

收录的可选依赖仍面向较旧的 DSH 版本。在 `0.2.1-alpha.1` 下，已安装的 `@huiliyi37/dsh-office@0.2.4` 和 `dsh-find-plugin@0.3.7` 会被兼容检查跳过，其最新发布版本也未声明支持此运行时。收录的思维导图插件同样保留旧版 peer dependencies。使用这些能力前需安装兼容的插件版本；PPT 预设加载测试不验证这些可选插件。

## 安装

构建本地插件、安装 profile 依赖，需要该预设时将 `presets/ppt-assistant` 复制到 `$DSH_HOME/.agent-presets/ppt-assistant`：

```sh
pnpm --dir profiles/yujp-web/packages/dsh-mindmap install --frozen-lockfile
pnpm --dir profiles/yujp-web/packages/dsh-mindmap run build
pnpm --dir profiles/yujp-web install --frozen-lockfile
```

profile 的 `package.json` 组合了 `dshmarket`、`dsh-find-plugin`、`dsh-office` 和本地思维导图插件。provider 凭据只保存在 DSH credentials domain 或环境变量中，不加入此 profile。
