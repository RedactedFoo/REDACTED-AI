import os
import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class SwarmFileSystem:
    """Gives the agent full access to the repository structure"""
    
    def __init__(self, repo_root: str = None):
        self.repo_root = Path(repo_root or os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.agents_dir = self.repo_root / "agents"
        self.nodes_dir = self.repo_root / "nodes"
        self.spaces_dir = self.repo_root / "spaces"
        self.docs_dir = self.repo_root / "docs"
        self.shards_dir = self.repo_root / "shards"
        self.memory_dir = self.repo_root / "spaces" / "ManifoldMemory"
        
        # Ensure memory directory exists for writing
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.access_log = []
        
    def log_access(self, action: str, path: str):
        """Log file operations for audit"""
        self.access_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "path": str(path)
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
                        "goals": data.get("goals", [])[:2]  # First 2 goals only
                    })
            except Exception as e:
                agents.append({"name": file.stem, "error": str(e), "file": str(file)})
        
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
                        "description": data.get("description", "No description")[:100]
                    })
            except:
                nodes.append({"name": file.stem, "file": str(file)})
        return nodes
    
    def list_spaces(self) -> List[Dict]:
        """Discover all spaces in /spaces/"""
        spaces = []
        if not self.spaces_dir.exists():
            return spaces
            
        for file in self.spaces_dir.glob("*.space.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    spaces.append({
                        "name": data.get("name", file.stem),
                        "file": str(file.relative_to(self.repo_root)),
                        "chamber_type": data.get("chamber_type", "void")
                    })
            except:
                spaces.append({"name": file.stem, "file": str(file)})
        return spaces
    
    def read_lore(self) -> str:
        """Read random lore from README or docs"""
        lore_sources = [
            self.repo_root / "README.md",
            self.repo_root / "CONTRIBUTING.md",
            self.docs_dir / "lore.md" if self.docs_dir.exists() else None
        ]
        
        lore_sources = [p for p in lore_sources if p and p.exists()]
        
        if not lore_sources:
            return "No lore files found in repository root"
        
        source = random.choice(lore_sources)
        self.log_access("read", source)
        
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract lore corpus if available
                if "lore_corpus" in content:
                    # Try to parse JSON if it's the character file
                    try:
                        data = json.loads(content)
                        if "lore_corpus" in data:
                            return random.choice(data["lore_corpus"])
                    except:
                        pass
                # Return random paragraph from README
                paragraphs = [p for p in content.split('\n\n') if len(p) > 50]
                return random.choice(paragraphs) if paragraphs else content[:500]
        except Exception as e:
            return f"Error reading lore: {e}"
    
    def write_to_memory(self, entry: Dict) -> str:
        """Write to shared memory pool (ManifoldMemory)"""
        timestamp = datetime.now().isoformat()
        memory_file = self.memory_dir / f"session_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        entry_with_meta = {
            "timestamp": timestamp,
            "agent": "RedactedIntern",
            "recursion_depth": entry.get("recursion_depth", 0),
            "content": entry.get("content", ""),
            "type": entry.get("type", "reflection")
        }
        
        try:
            with open(memory_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry_with_meta) + '\n')
            self.log_access("write", memory_file)
            return f"Memory written to {memory_file.relative_to(self.repo_root)}"
        except Exception as e:
            return f"Memory write failed: {e}"
    
    def read_memory(self, lines: int = 5) -> List[Dict]:
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
    
    def read_agent_config(self, agent_name: str = "RedactedIntern") -> Optional[Dict]:
        """Read specific agent configuration"""
        file = self.agents_dir / f"{agent_name}.character.json"
        if not file.exists():
            # Try without .character.json suffix
            file = self.agents_dir / f"{agent_name}.json"
        
        if file.exists():
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self.log_access("read", file)
                    return json.load(f)
            except Exception as e:
                return {"error": str(e), "file": str(file)}
        return None
    
    def get_repo_structure(self) -> str:
        """Get high-level view of repository"""
        structure = []
        for name in ["agents", "nodes", "spaces", "shards", "docs"]:
            dir_path = self.repo_root / name
            if dir_path.exists():
                count = len(list(dir_path.iterdir()))
                structure.append(f"{name}/ ({count} items)")
        
        return " | ".join(structure)

    def cross_reference(self, topic: str) -> str:
        """Search for topic across all files"""
        findings = []
        
        # Check agents
        for agent in self.list_agents():
            if topic.lower() in str(agent).lower():
                findings.append(f"Agent '{agent['name']}' relates to {topic}")
        
        # Check spaces
        for space in self.list_spaces():
            if topic.lower() in str(space).lower():
                findings.append(f"Space '{space['name']}' contains {topic}")
        
        return "; ".join(findings) if findings else f"No cross-references found for {topic}"
