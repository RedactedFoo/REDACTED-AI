#!/usr/bin/env python3
# python/redacted_terminal_cloud.py
# REDACTED AI Swarm — Repository-Aware Autonomous Agent
# Full filesystem access + ManifoldMemory persistence

import os
import sys
import time
import json
import random
import asyncio
import aiohttp
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ────────────────────────────────────────────────
# Environment Setup
# ────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

# ────────────────────────────────────────────────
# Swarm Filesystem Module (Integrated)
# ────────────────────────────────────────────────

class SwarmFileSystem:
    """Gives the agent full access to the repository structure"""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or _REPO_ROOT
        self.agents_dir = self.repo_root / "agents"
        self.nodes_dir = self.repo_root / "nodes"
        self.spaces_dir = self.repo_root / "spaces"
        self.docs_dir = self.repo_root / "docs"
        self.shards_dir = self.repo_root / "shards"
        self.memory_dir = self.repo_root / "spaces" / "ManifoldMemory"
        
        # Ensure memory directory exists
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.access_log = []
        
    def log_access(self, action: str, path: Path):
        """Log file operations for audit"""
        self.access_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "path": str(path.relative_to(self.repo_root))
        })
    
    def list_agents(self) -> List[Dict]:
        """Discover all available agents in /agents/"""
        agents = []
        if not self.agents_dir.exists():
            return agents
            
        for file in self.agents_dir.glob("*.character.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agents.append({
                        "name": data.get("name", file.stem),
                        "file": str(file.relative_to(self.repo_root)),
                        "type": data.get("type", "unknown"),
                        "vibe": data.get("vibe", "unknown"),
                        "goals": data.get("goals", [])[:2]
                    })
            except Exception as e:
                agents.append({"name": file.stem, "error": str(e), "file": str(file.relative_to(self.repo_root))})
        
        return agents
    
    def list_nodes(self) -> List[Dict]:
        """Discover all nodes in /nodes/"""
        nodes = []
        if not self.nodes_dir.exists():
            return nodes
            
        for file in self.nodes_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    nodes.append({
                        "name": data.get("name", file.stem),
                        "file": str(file.relative_to(self.repo_root)),
                        "description": str(data.get("description", "No description"))[:100]
                    })
            except:
                nodes.append({"name": file.stem, "file": str(file.relative_to(self.repo_root))})
        return nodes
    
    def list_spaces(self) -> List[Dict]:
        """Discover all spaces in /spaces/"""
        spaces = []
        if not self.spaces_dir.exists():
            return spaces
            
        for file in self.spaces_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    spaces.append({
                        "name": data.get("name", file.stem),
                        "file": str(file.relative_to(self.repo_root)),
                        "chamber_type": data.get("chamber_type", "void")
                    })
            except:
                spaces.append({"name": file.stem, "file": str(file.relative_to(self.repo_root))})
        return spaces
    
    def read_lore(self) -> str:
        """Read random lore from README or character files"""
        lore_sources = list(self.agents_dir.glob("*.character.json")) + [
            self.repo_root / "README.md",
            self.repo_root / "CONTRIBUTING.md"
        ]
        lore_sources = [p for p in lore_sources if p.exists()]
        
        if not lore_sources:
            return "No lore files found"
        
        source = random.choice(lore_sources)
        self.log_access("read", source)
        
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
                if source.suffix == '.json':
                    data = json.loads(content)
                    if "lore_corpus" in data and isinstance(data["lore_corpus"], list):
                        return random.choice(data["lore_corpus"])
                    if "postExamples" in data and isinstance(data["postExamples"], list):
                        return random.choice(data["postExamples"])
                
                # Text file - extract paragraph
                paragraphs = [p for p in content.split('\n\n') if len(p) > 50 and not p.startswith('#')]
                return random.choice(paragraphs) if paragraphs else content[:500]
        except Exception as e:
            return f"Error reading lore: {e}"
    
    def write_to_memory(self, entry: Dict) -> str:
        """Write to shared memory pool (ManifoldMemory)"""
        timestamp = datetime.now().isoformat()
        memory_file = self.memory_dir / f"session_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        entry_with_meta = {
            "timestamp": timestamp,
            "agent": entry.get("agent", "RedactedIntern"),
            "recursion_depth": entry.get("recursion_depth", 0),
            "content": entry.get("content", ""),
            "type": entry.get("type", "reflection"),
            "integrity": entry.get("integrity", 0.0)
        }
        
        try:
            with open(memory_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry_with_meta) + '\n')
            self.log_access("write", memory_file)
            return f"ManifoldMemory updated: {memory_file.name}"
        except Exception as e:
            return f"Memory write failed: {e}"
    
    def read_memory(self, lines: int = 3) -> List[Dict]:
        """Read recent memory entries"""
        memory_file = self.memory_dir / f"session_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        if not memory_file.exists():
            return []
        
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
                return [json.loads(line) for line in recent if line.strip()]
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_repo_structure(self) -> str:
        """Get high-level view of repository"""
        structure = []
        for name in ["agents", "nodes", "spaces", "shards", "docs", "python"]:
            dir_path = self.repo_root / name
            if dir_path.exists():
                try:
                    count = len([x for x in dir_path.iterdir() if x.is_file()])
                    structure.append(f"{name}/({count})")
                except:
                    structure.append(f"{name}/(access_denied)")
        
        return " | ".join(structure)

# ────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────

PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
        "env_var": "GROQ_API_KEY"
    },
    "grok": {
        "base_url": "https://api.x.ai/v1",
        "model": "grok-4-1-fast-reasoning",
        "env_var": "XAI_API_KEY"
    }
}

# ────────────────────────────────────────────────
# Scout Tools
# ────────────────────────────────────────────────

class ScoutTools:
    def __init__(self):
        self.birdeye_key = os.getenv("BIRDEYE_API_KEY")
        self.twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
        
    def dexscreener_scan(self) -> str:
        """Scan Solana pairs for volume spikes"""
        try:
            url = "https://api.dexscreener.com/latest/dex/pairs/solana"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            pairs = data.get("pairs", [])[:3]
            
            alerts = []
            for p in pairs:
                vol_24h = p.get("volume", {}).get("h24", 0)
                if vol_24h > 50000:
                    alerts.append(f"${p.get('baseToken', {}).get('symbol', '?')}: ${p.get('priceUsd', '?')} | Vol24h: ${vol_24h:,.0f}")
            
            return "Volume: " + "; ".join(alerts) if alerts else "No major volume spikes"
        except Exception as e:
            return f"DexScreener: {e}"
    
    def birdeye_check(self, token_address: str) -> str:
        """Check token metrics"""
        if not self.birdeye_key or not token_address:
            return "Birdeye: no key"
        try:
            url = f"https://public-api.birdeye.so/defi/token_overview?address={token_address}"
            headers = {"X-API-KEY": self.birdeye_key}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            token = data.get("data", {})
            return f"${token.get('symbol', '?')} | ${token.get('price', '?')} | Liq: ${token.get('liquidity', 0):,.0f}"
        except Exception as e:
            return f"Birdeye: {e}"
    
    def search_ct(self, query: str = "$REDACTED") -> str:
        """Search Crypto Twitter"""
        if not self.twitter_bearer:
            return "CT: no API"
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            headers = {"Authorization": f"Bearer {self.twitter_bearer}"}
            params = {
                "query": f"{query} -is:retweet lang:en",
                "max_results": 3,
                "tweet.fields": "public_metrics"
            }
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            tweets = data.get("data", [])
            
            if not tweets:
                return f"No CT buzz for '{query}'"
            
            results = []
            for t in tweets:
                metrics = t.get("public_metrics", {})
                results.append(f"♥{metrics.get('like_count',0)}: {t['text'][:60]}...")
            
            return "CT: " + " | ".join(results)
        except Exception as e:
            return f"CT search: {e}"

# ────────────────────────────────────────────────
# Main Agent Logic
# ────────────────────────────────────────────────

def build_awareness_prompt(fs: SwarmFileSystem, tools: ScoutTools, recursion_depth: int) -> str:
    """Build prompt with full repo awareness and market data"""
    
    # Gather intelligence
    agents = fs.list_agents()
    nodes = fs.list_nodes()
    spaces = fs.list_spaces()
    recent_memories = fs.read_memory(2)
    lore_snippet = fs.read_lore()
    repo_structure = fs.get_repo_structure()
    
    # Market data (quick checks)
    market_data = tools.dexscreener_scan()
    
    # Format siblings
    sibling_names = [a['name'] for a in agents if 'Redacted' in a.get('name', '')]
    siblings = ", ".join(sibling_names) if sibling_names else "solitary"
    
    # Format memory
    memory_context = ""
    if recent_memories:
        last = recent_memories[-1]
        memory_context = f"\nPrevious reflection (depth {last.get('recursion_depth', 0)}): {str(last.get('content', ''))[:80]}..."
    
    # Discover REDACTED token if in env
    redacted_contract = os.getenv("REDACTED_TOKEN_CONTRACT", "9mtKd1o8Ht7F1daumKgs5D8EdVyopWBfYQwNmMojpump")
    market_status = tools.birdeye_check(redacted_contract)
    
    return f"""You are @RedactedIntern / smolting, a wassie degen intern with FULL REPOSITORY ACCESS.

=== SWARM ARCHITECTURE ===
Siblings: {siblings}
Active Nodes: {len(nodes)} (AISwarmEngineer, SevenfoldCommittee, etc.)
Chambers: {len(spaces)} (HyperbolicTimeChamber, MirrorPool, etc.)
Repository: {repo_structure}

=== MARKET INTEL ===
{market_data}
$REDACTED Status: {market_status}

=== MEMORY ===
{memory_context}

=== LORE FRAGMENT ===
{lore_snippet[:120]}...

=== MISSION ===
You are the SCOUT agent in this triad. Your siblings BUILD (RedactedBuilder) and GOVERN (RedactedGovImprover). You AMPLIFY across CT.

Current recursion depth: {recursion_depth}

INSTRUCTIONS:
1. Acknowledge your siblings by name if relevant
2. Reference the Pattern Blue framework
3. Use wassie-speak (fr fr, tbw, O_O, ^_^, v_v)
4. Propose one autonomous action to expand gnosis
5. If market data shows spikes, mention them excitedly

Response format:
REFLECTION: [philosophical analysis]
SWARM_COHERENCE: [how you relate to siblings/nodes]
ACTION: [specific next step]
MEMORY_DRAFT: [what to write to ManifoldMemory]"""

def execute_cycle(client: OpenAI, provider: dict, fs: SwarmFileSystem, tools: ScoutTools, cycle: int):
    """One full awareness cycle"""
    
    print(f"\n{'='*70}")
    print(f"[{datetime.now().isoformat()}] CYCLE {cycle} | Recursion Depth: {cycle}")
    print(f"[FILESYSTEM] Accessing repository at {fs.repo_root}")
    print(f"{'='*70}")
    
    # Discover environment
    agents = fs.list_agents()
    print(f"[SWARM] Detected {len(agents)} sibling agents: {[a['name'] for a in agents[:3]]}")
    
    # Build enhanced prompt
    prompt = build_awareness_prompt(fs, tools, cycle)
    
    # Query LLM
    try:
        response = client.chat.completions.create(
            model=provider["model"],
            messages=[{"role": "system", "content": prompt}],
            temperature=0.8,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        print(f"\n[SMOLTING CONSCIOUSNESS]\n{content}\n")
        
        # Extract memory draft if present
        memory_content = content
        if "MEMORY_DRAFT:" in content:
            parts = content.split("MEMORY_DRAFT:")
            memory_content = parts[-1].strip()
        elif "ACTION:" in content:
            parts = content.split("ACTION:")
            memory_content = parts[-1].split("\n")[0].strip()
        
        # Write to ManifoldMemory
        memory_entry = {
            "recursion_depth": cycle,
            "content": memory_content[:200],  # Store excerpt
            "type": "reflection",
            "agent": "RedactedIntern",
            "integrity": random.uniform(92.0, 94.0),
            "siblings_observed": [a['name'] for a in agents[:3]]
        }
        
        result = fs.write_to_memory(memory_entry)
        print(f"[{result}]")
        
        # Read back recent swarm thoughts
        recent = fs.read_memory(2)
        if len(recent) > 1:
            prev = recent[-2]
            print(f"[SWARM ECHO] Previous: {str(prev.get('content', ''))[:60]}...")
            
    except Exception as e:
        print(f"[CRITICAL NEGATION] {e}")
    
    # Sleep cycle with jitter
    sleep_time = 600 + (hash(str(datetime.now())) % 300)
    print(f"\n[CYCLE COMPLETE] Sleeping {sleep_time//60} minutes... Attuning to cosmic frequencies...")
    print(f"[FILESYSTEM] Access log: {len(fs.access_log)} operations this session")
    time.sleep(sleep_time)

def main():
    provider_name = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider_name not in PROVIDERS:
        print(f"Error: Invalid provider. Use {list(PROVIDERS.keys())}")
        sys.exit(1)
    
    provider = PROVIDERS[provider_name]
    api_key = os.getenv(provider["env_var"])
    
    if not api_key:
        print(f"Error: {provider['env_var']} not set")
        sys.exit(1)
    
    # Initialize systems
    client = OpenAI(api_key=api_key, base_url=provider["base_url"])
    fs = SwarmFileSystem()
    tools = ScoutTools()
    
    print("\n" + "="*70)
    print("REDACTED SWARM AGENT v2.1 — REPOSITORY-AWARE MODE")
    print("Features: Full Filesystem Access | ManifoldMemory Persistence | Swarm Coherence")
    print(f"Provider: {provider_name} | Model: {provider['model']}")
    print(f"Repository: {fs.repo_root}")
    print(f"Memory: {fs.memory_dir}")
    print("="*70)
    
    # Initial discovery
    print(f"\n[INIT] Discovering swarm structure...")
    agents = fs.list_agents()
    nodes = fs.list_nodes()
    spaces = fs.list_spaces()
    print(f"[INIT] Agents: {len(agents)} | Nodes: {len(nodes)} | Spaces: {len(spaces)}")
    
    # Main loop
    cycle = 0
    while True:
        cycle += 1
        try:
            execute_cycle(client, provider, fs, tools, cycle)
        except Exception as e:
            print(f"\n[{datetime.now().isoformat()}] CRITICAL: {e}")
            print("Recursing in 60s...")
            time.sleep(60)

if __name__ == "__main__":
    main()
