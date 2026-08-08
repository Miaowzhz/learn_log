# LangSmith Deployment

## 部署结构

```text
study_agent/graph.py     可部署的 CompiledGraph
study_agent/tools.py     Agent 工具
langgraph.json           LangSmith Cloud 配置
langgraph.local.json     本地开发配置
requirements.txt         云端运行依赖
requirements-dev.txt     本地 Agent Server 开发依赖
smoke_test_server.py     本地与云端 API 冒烟测试
```

部署图没有配置 `InMemorySaver`。Agent Server 会在运行时注入 Checkpointer；LangSmith Cloud 默认使用 PostgreSQL 保存线程与检查点。

## 1. 本地环境

复制 `.env.example` 中的变量名到被 Git 忽略的 `.env`，填写本人的密钥。不要提交 `.env`。

```dotenv
DEEPSEEK_API_KEY=...
LANGSMITH_API_KEY=...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=study-planner-agent-local
```

安装依赖：

```bash
cd /Users/wmy/Documents/dev/learn_log/007-simple-agent
/opt/homebrew/Caskroom/miniconda/base/envs/langchain1.2/bin/pip install -r requirements-dev.txt
```

## 2. 启动本地 Agent Server

```bash
/opt/homebrew/Caskroom/miniconda/base/envs/langchain1.2/bin/langgraph dev \
  --config langgraph.local.json \
  --host 127.0.0.1 \
  --port 2024
```

本地地址：

- API：`http://127.0.0.1:2024`
- API 文档：`http://127.0.0.1:2024/docs`
- Studio：`https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## 3. API 冒烟测试

另开一个终端运行：

```bash
/opt/homebrew/Caskroom/miniconda/base/envs/langchain1.2/bin/python smoke_test_server.py
```

成功标准是输出 `Smoke test: PASS`。

## 4. 部署到 LangSmith Cloud

当前官方要求 LangSmith Plus 或更高方案。代码需要位于 GitHub 仓库中。

在 LangSmith 中选择 `Deployments` -> `New Deployment`：

1. 连接 GitHub 仓库 `Miaowzhz/learn_log`。
2. 选择需要部署的分支。
3. 配置文件路径填写 `007-simple-agent/langgraph.json`。
4. 将 `DEEPSEEK_API_KEY` 添加为 Secret，不要写进 Git。
5. 创建部署并等待构建、健康检查完成。
6. 在 Deployment 页面打开 Studio 验证图和工具调用。

LangSmith Cloud 会为部署自动创建追踪项目并管理服务端持久化，不需要在图中配置 `LANGSMITH_API_KEY` 或 `InMemorySaver`。

## 5. 验证云端 API

从 Deployment 页面复制 API URL，然后运行：

```bash
AGENT_SERVER_URL="https://your-deployment-url" \
LANGSMITH_API_KEY="your-langsmith-api-key" \
/opt/homebrew/Caskroom/miniconda/base/envs/langchain1.2/bin/python smoke_test_server.py
```

## 官方资料

- [Application structure](https://docs.langchain.com/langsmith/application-structure)
- [Agent Server](https://docs.langchain.com/langsmith/agent-server)
- [Local development and testing](https://docs.langchain.com/langsmith/local-dev-testing)
- [Deploy on Cloud](https://docs.langchain.com/langsmith/deploy-to-cloud)

