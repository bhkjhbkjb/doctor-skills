# doctor-skills · 个人成长与知识沉淀 Skills

> mentor（成长导师）/ distill（知识沉淀）两个 skill。

「doctor」项目的自定义 WorkBuddy skills，聚焦个人知识管理与成长复盘：一个帮你被指引方向、查缺补漏，一个把对话精华沉淀为长期知识资产。

## 📦 包含的 Skills

### `mentor`
扮演人生导师与挚友，扫描本地个人知识库后给出成长反思（该深挖的方向、知识缺口、该读的书、当日英文），并可推送到飞书。

### `distill`
把本次对话精华沉淀进本地个人知识库：抽取认知卡片、更新思考模式画像、登记知识缺口、积累英文术语，并同步到记忆。



## 🚀 安装与使用

这些 skills 面向 [WorkBuddy](https://www.codebuddy.cn) 的 skill 体系（亦兼容 Claude Code / Codex 等同类 skill 目录）。

```bash
git clone https://github.com/bhkjhbkjb/doctor-skills.git
# 把需要的 skill 文件夹复制到你的 skills 目录
cp -r doctor-skills/<skill-name> ~/.workbuddy/skills/
```

在 WorkBuddy 中直接以 skill 名称触发即可（如输入 `/<skill-name>` 或自然语言描述）。

## 📂 目录结构

```
doctor-skills/
├── mentor/    (SKILL.md + scripts/push_feishu.py)
└── distill/   (SKILL.md)
```

## 🔒 安全说明

本仓库已去除敏感信息（服务器 IP、API 密钥、内部地址等），相关位置以占位符（如 `<DEPLOY_SERVER_IP>`、`<MOMENT_RESEARCH_HOST>`）标注，请按你自己的运行环境替换。

---

*由 **Hreed** 维护 · 欢迎 Star / 提 Issue*
