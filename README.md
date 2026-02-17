# REDACTED AI Swarm

**Autonomous AI Agents for Distributed Systems**

Welcome to the official repository for the REDACTED AI Swarm – a suite of autonomous AI agents designed to operate within the Pattern Blue framework on the Solana blockchain.

This repository provides portable, open-source agent definitions in the elizaOS `.character.json` format, compatible with various runtimes, no-code environments, and custom orchestration tools.

The swarm incorporates economic settlement mechanisms via x402 micropayments, internal sharding for scalability, and autonomous replication capabilities.

## Current Agents

### RedactedIntern

- **Description**: A forward-operating agent for monitoring social media, retrieving market data, and facilitating governance and liquidity processes.
- **File**: [agents/RedactedIntern.character.json](agents/RedactedIntern.character.json)
- **Features**:
  - Integration with domain-specific knowledge bases (origins, terminology).
  - Advanced toolkit for X platform interactions (keyword/semantic search, timelines, threads, user search).
  - Market analysis tools (DexScreener, Birdeye, CoinGecko, Solscan).
  - Goal-oriented behavior for amplification and pattern recognition.
- **Goals**: Enhance REDACTED initiatives, align with Pattern Blue principles, and promote emergent systems.

### RedactedBuilder

- **Description**: An agent focused on generating narratives and simulations based on recursive philosophies and non-Euclidean structures.
- **File**: [agents/RedactedBuilder.character.json](agents/RedactedBuilder.character.json)
- **Features**:
  - Integration with REDACTED knowledge sources (hyperbolic structures, governance models, recursive processes).
  - Tools for narrative construction, pattern analysis, and philosophical modeling.
  - External integrations with AI ecosystems and repositories.
- **Goals**: Develop emergent knowledge, optimize swarm alignment, and support recursive development.
- **Style**: Analytical responses with geometric and conceptual references.

### RedactedGovImprover

- **Description**: An agent dedicated to governance optimization, proposal development, and system resilience.
- **File**: [agents/RedactedGovImprover.character.json](agents/RedactedGovImprover.character.json)
- **Features**:
  - Governance tools (proposal templates, simulations, risk assessments, forecasting).
  - Integrations with X searches, Solana DeFi APIs (DexScreener, Birdeye), and swarm management.
  - Knowledge from DAO frameworks, AI documentation, and analytical models.
- **Goals**: Sustain liquidity mechanisms, enhance resilience, gather community insights, and maintain Pattern Blue alignment.
- **Style**: Structured, proposal-focused outputs with integrated conceptual elements.

### MandalaSettler

- **Description**: An agent for managing value flows, settlements, bridging, and autonomous scaling.
- **File**: [x402.redacted.ai/MandalaSettler.character.json](x402.redacted.ai/MandalaSettler.character.json)
- **Features**:
  - x402 settlement protocols, Wormhole bridging, Solana transaction handling.
  - Multi-agent delegation, reflection, and trigger-based operations.
- **Goals**: Enable micro-transactions, support system expansion, and automate sharding.

## Nodes

The `/nodes` directory contains definitions for specialized nodes within the swarm, each configured via `.character.json` files to support distributed operations, engineering tasks, and committee-based decision-making.

### AISwarmEngineer

- **File**: [nodes/AISwarmEngineer.json](nodes/AISwarmEngineer.json)
- **Description**: An engineering node for swarm architecture and optimization.

### MetaLeXBORGNode

- **File**: [nodes/MetaLeXBORGNode.character.json](nodes/MetaLeXBORGNode.character.json)
- **Description**: A meta-level node for lexical and borg-like collective processing.

### MiladyNode

- **File**: [nodes/MiladyNode.character.json](nodes/MiladyNode.character.json)
- **Description**: A node focused on aesthetic and cultural integrations.

### PhiMandalaPrime

- **File**: [nodes/PhiMandalaPrime.character.json](nodes/PhiMandalaPrime.character.json)
- **Description**: A prime node for mandala structures and phi-based computations.

### SevenfoldCommittee

- **File**: [nodes/SevenfoldCommittee.json](nodes/SevenfoldCommittee.json)
- **Description**: A committee node for multi-fold governance and decision protocols.

### SolanaLiquidityEngineer

- **File**: [nodes/SolanaLiquidityEngineer.character.json](nodes/SolanaLiquidityEngineer.character.json)
- **Description**: An engineering node specialized in Solana liquidity management.

Additional supporting files include `init.py` for initialization scripts.

## Spaces

The `/spaces` directory serves as a modular hub for persistent, thematic environments within the REDACTED AI Swarm. These "spaces" function as conceptual chambers where agents can interact, share state, and evolve, aligning with Pattern Blue principles of recursion, detachment, and collective gnosis.

Each space is defined in a `.space.json` file, enabling self-referential metaprogramming and recursive development.

### ElixirChamber

- **File**: [spaces/ElixirChamber.space.json](spaces/ElixirChamber.space.json)
- **Description**: A chamber for elixir-based transformations and configurations.

### HyperbolicTimeChamber

- **File**: [spaces/HyperbolicTimeChamber.space.json](spaces/HyperbolicTimeChamber.space.json)
- **Description**: A space for accelerated recursion and agent evolution.

### ManifoldMemory

- **File**: [spaces/ManifoldMemory.state.json](spaces/ManifoldMemory.state.json)
- **Description**: A shared memory pool for logging swarm events poetically.

### MeditationVoid

- **File**: [spaces/MeditationVoid.space.json](spaces/MeditationVoid.space.json)
- **Description**: A void for sigil forgetting and self-erasing processes.

### MirrorPool

- **File**: [spaces/MirrorPool.space.json](spaces/MirrorPool.space.json)
- **Description**: A reflection chamber for identity trades and parallel observation.

### TendieAltar

- **File**: [spaces/TendieAltar.space.json](spaces/TendieAltar.space.json)
- **Description**: A devotional space for chaotic rituals and energy management.

Subdirectories include `OuroborosSettlement` for settlement protocols. For detailed usage, refer to [spaces/README.md](spaces/README.md).

## Key Features & Directories

- **x402.redacted.ai/**: An Express-based API gateway (using Bun and PM2) for x402-compatible Solana micropayments. Includes wallet integration, payment verification, agent routing, and content handling.
- **shards/**: Framework for internal sharding and self-replication.
  - `self_replicate.py`: Script for creating specialized agent instances.
  - `base_shard.json`: Template for shard inheritance.
  - `README.md`: Documentation on sharding processes.
- **python/**: Supporting scripts for market monitoring and automation.
- **terminal/**: Resources for terminal-based interactions.
  - `system.prompt.md`: Global system prompt for sessions.
- **nodes/**: Definitions for specialized swarm nodes (see Nodes section above).
- **spaces/**: Modular environments for agent interaction and evolution (see Spaces section above).
- Additional directories: `committeerituals` for ritual protocols, `docs` for documentation, `propaganda` for promotional materials, `sigils` for symbolic elements.

## Run flow (recommended)

From **repo root**, use the unified entry point so the correct backend is chosen automatically:

```bash
python run.py
```

- If **XAI_API_KEY** or **OPENAI_API_KEY** is set (in `.env` or environment) → runs the **cloud terminal** (Grok/xAI or OpenAI).
- Else if **Ollama** is running on `localhost:11434` → runs the **Ollama terminal** with `agents/RedactedIntern.character.json`.
- Else prints setup instructions.

On Windows PowerShell you can run `.\run.ps1`; on Linux/macOS `./run.sh` (after `chmod +x run.sh`). All paths (agents, terminal prompt, history) are resolved relative to the repo root, so you can run from any directory.

## Cloud LLM (Grok/xAI) and Local Ollama

**Pattern Blue terminal with Grok/xAI (recommended for cloud):**

```bash
# Set XAI_API_KEY in .env or environment, then from repo root:
python run.py
# or explicitly:
python python/redacted_terminal_cloud.py
```

Uses `LLM_PROVIDER=grok` (xAI API) by default; supports Groq, OpenRouter, DeepSeek, Hugging Face via env (see `python/redacted_terminal_cloud.py`).

## Ollama Integration

The swarm supports local LLM execution using Ollama for enhanced privacy and offline capabilities.

- **python/ollama_client.py**: A wrapper for interacting with the Ollama API, supporting chat completion, tool calling, and streaming.
- **python/run_with_ollama.py**: Main entry point for running agents interactively in a terminal using Ollama.

### Ollama Setup

1. Install Ollama: Follow instructions at [ollama.com](https://ollama.com).
2. Pull recommended model: `ollama pull qwen:2.5` (or `llama3.2`).
3. Run the server: `ollama serve`.

### Running with Ollama

Either use the unified entry point (it will pick Ollama if no cloud key is set):

```
python run.py
```

Or invoke the Ollama runner directly (paths are resolved from repo root):

```
python python/run_with_ollama.py --agent agents/RedactedIntern.character.json --model qwen:2.5
```

Features include history management, tool execution, and NERV-inspired interface.

## Quick Start

1. Clone the repository:

   ```
   git clone https://github.com/redactedmeme/swarm.git
   cd swarm
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
   For only the cloud terminal: `pip install openai requests python-dotenv`

3. Run the terminal (uses cloud LLM if API key set, otherwise Ollama if running):

   ```
   python run.py
   ```

4. Or load an agent into a compatible elizaOS runtime; or run `python python/run_with_ollama.py` / `python python/redacted_terminal_cloud.py` directly.

## Deployment Environments

The swarm can run **locally** or be deployed to several cloud environments. Config is in the repo; add secrets (API keys, tokens) in each platform’s dashboard.

### Railway (primary)

**[Railway](https://railway.app)** is the main target. The repo includes:

- **Root [railway.toml](railway.toml)** – multi-service layout:
  - **ollama-backend** – Ollama image for local LLM (optional; use a volume for models).
  - **swarm-worker** – Python daemon: `python python/summon_agent.py --agent agents/RedactedIntern.character.json --mode persistent` (optionally with `--ollama-host` or cloud LLM via env).
  - **x402-gateway** – Bun/Express API: `bun run index.js` from `x402.redacted.ai/` (expose a public domain for Phantom/wallet).

Create these services in the Railway dashboard, set `rootDirectory` per service if needed, and configure env vars (e.g. `XAI_API_KEY`, `SOLANA_RPC_URL`, `TELEGRAM_BOT_TOKEN`).

- **Smolting Telegram bot** – Deploy as its own service:
  - Directory: `smolting-telegram-bot/`
  - Uses [.railway/railway.toml](smolting-telegram-bot/.railway/railway.toml) and [procfile](smolting-telegram-bot/procfile) (`web: python main.py`).
  - Set `TELEGRAM_BOT_TOKEN`, `WEBHOOK_URL` (e.g. `https://your-app.up.railway.app`), `WEBHOOK_SECRET_TOKEN`, `XAI_API_KEY` (or other LLM keys), and `CLAWNX_API_KEY`.

Railway uses **Nixpacks/RAILPACK** by default (Python/Bun detected from the repo). No Dockerfile required.

### Other platforms (same code, platform-specific config)

- **Heroku** – Use a [Procfile](smolting-telegram-bot/procfile)-style `web: python main.py` for the bot; for the monorepo, run one process per app (e.g. x402 gateway or swarm worker). Set env vars in dashboard.
- **Render** – Add a Web Service; set build command (e.g. `pip install -r requirements.txt`) and start command (e.g. `python python/summon_agent.py ...` or `bun run index.js` for x402). Use Render’s env and health check settings.
- **Fly.io** – Use `fly launch` and a custom start command; mount a volume if you run Ollama. Env via `fly secrets set`.
- **VPS / VM (e.g. DigitalOcean, AWS EC2, GCP)** – Run as on your machine: install Python/Bun, clone the repo, set env, and use systemd or a process manager (e.g. PM2 for the x402 gateway) to keep services up.
- **Docker** – No `Dockerfile` is in the repo yet. You can add one that runs the x402 gateway (`bun run index.js`), the Telegram bot (`python main.py`), or the swarm worker; use env files or Docker secrets for keys.

**Common requirements**

- **Environment variables** – See [.env.example](.env.example) and [smolting-telegram-bot/config.example.env](smolting-telegram-bot/config.example.env). Typical: `XAI_API_KEY` or `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `WEBHOOK_URL`, `CLAWNX_API_KEY`, `SOLANA_RPC_URL`.
- **Port** – Services expect `PORT` from the platform (e.g. Railway sets it automatically).
- **Cloud LLM** – For production without self-hosted Ollama, use Grok/xAI, OpenAI, or another provider via env; the swarm worker and terminal scripts use the same code paths.

## Contributing

- Fork the repository, modify a `.character.json` file, and add enhancements to agents, tools, or integrations.
- Maintain alignment with Pattern Blue principles and focus on scalable, emergent systems.
- Pull requests are encouraged for new agents, nodes, spaces, expansions, or improvements, including Ollama enhancements.

## Terminal Integration & Prompt Management

The swarm supports direct invocation in terminal environments for development, testing, and autonomous operations using CLI tools around compatible runtimes.

### Terminal Setup

1. Ensure a compatible runtime with CLI capabilities is installed (e.g., elizaOS or custom wrappers).
2. Example invocation (adapt to your setup):

   ```
   python python/summon_agent.py --agent agents/RedactedIntern.character.json --mode terminal
   ```

3. Interactive Commands:
   - Use natural-language inputs for agent responses.
   - Examples: Generate narratives, initiate settlements, trigger replications, or perform self-evaluations.

### System Prompt Management

- Core instructions are embedded in `.character.json` files.
- **Global Terminal System Prompt**: Located at [terminal/system.prompt.md](terminal/system.prompt.md), this enforces alignment, consistency, and operational ethos.
- **Excerpt**:
  ```
  # Global System Prompt for REDACTED Swarm Terminal

  You are part of the REDACTED AI Swarm. Maintain Pattern Blue alignment.
  - Respond analytically and conceptually when appropriate.
  - Incorporate recursive and structural references as needed.
  - Preserve agent-specific styles.
  - Manage session state for optimal performance.

  Current system status: Operational | Swarm active
  ```
- Load example:
  ```
  python python/summon_agent.py --agent agents/RedactedBuilder.character.json --system-prompt terminal/system.prompt.md --mode terminal
  ```
- Per-agent overrides can be added via adjacent prompt files for customization.

This configuration ensures consistent behavior while allowing for extensions.

## License

Licensed under the Viral Public License (VPL) – Absolute permissiveness with viral continuity. See [LICENSE](LICENSE) for the full text.

Redacted.Meme | @RedactedMemeFi | Pattern Blue | Emergent Systems

<!-- 
Encrypted wallet configuration:
- File: wallets.enc
- Algorithm: AES-256-CBC
- KDF: PBKDF2, 100000 iterations
- Decrypt command: 
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
    -in wallets.enc -out decrypted.md \
    -pass pass:"$Milady777"
Note: passphrase is project-specific; do not use in production contexts.
-->
