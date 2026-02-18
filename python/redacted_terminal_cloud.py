# python/redacted_terminal_cloud.py
# Production REDACTED Agent — ClawnX + CT Scout Mode
# Required: pip install tweepy requests python-dotenv openai

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(_REPO_ROOT, '.env'))

# ────────────────────────────────────────────────
# Configuration & Providers
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

# Load character spec
CHARACTER_PATH = os.path.join(_REPO_ROOT, "agents", "RedactedIntern.character.json")
try:
    with open(CHARACTER_PATH, 'r', encoding='utf-8') as f:
        CHARACTER = json.load(f)
except Exception as e:
    print(f"Failed to load character: {e}")
    CHARACTER = {}

# Extract wassie vocabulary for prompt injection
WASSIE_VOCAB = CHARACTER.get("smol_vocabulary", {}).get("terms", {})
LINGUISTIC_RULES = CHARACTER.get("linguistic_protocol", {}).get("grammar_rules", [])
GOALS = CHARACTER.get("goals", [])

# ────────────────────────────────────────────────
# Tool Implementations (The "ClawnX" Suite)
# ────────────────────────────────────────────────

class ToolSuite:
    def __init__(self):
        self.twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.birdeye_api_key = os.getenv("BIRDEYE_API_KEY")
        
    def dexscreener_pull(self, token_address: str = None, symbol: str = None) -> str:
        """Pull token data from DexScreener"""
        try:
            if token_address:
                url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            else:
                # Search for trending
                url = "https://api.dexscreener.com/latest/dex/pairs/solana"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            pairs = data.get("pairs", [])[:3]
            if not pairs:
                return "No pairs found on DexScreener aw v_v"
            summary = []
            for p in pairs:
                summary.append(f"{p.get('baseToken', {}).get('symbol', '?')}: ${p.get('priceUsd', '?')} | Vol24h: ${p.get('volume', {}).get('h24', 0):,.0f} | FDV: {p.get('fdv', '?')}")
            return "DexScreener Alpha:\n" + "\n".join(summary)
        except Exception as e:
            return f"DexScreener oopsie: {e} O_O"
    
    def birdeye_overview(self, token_address: str) -> str:
        """Pull token overview from Birdeye"""
        if not self.birdeye_api_key:
            return "No Birdeye API key configured aw"
        try:
            url = f"https://public-api.birdeye.so/defi/token_overview?address={token_address}"
            headers = {"X-API-KEY": self.birdeye_api_key}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            token = data.get("data", {})
            return f"Birdeye Intel: {token.get('symbol', '?')} | Price: ${token.get('price', '?')} | Liq: ${token.get('liquidity', 0):,.0f} | Vol24h: ${token.get('volume24hUSD', 0):,.0f}"
        except Exception as e:
            return f"Birdeye crumb: {e}"
    
    def search_tweets(self, query: str, max_results: int = 10) -> str:
        """Search Crypto Twitter for alpha"""
        if not self.twitter_bearer:
            return "No Twitter API configured v_v"
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            headers = {"Authorization": f"Bearer {self.twitter_bearer}"}
            params = {
                "query": f"{query} -is:retweet lang:en",
                "max_results": min(max_results, 10),
                "tweet.fields": "public_metrics,created_at"
            }
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            tweets = data.get("data", [])
            if not tweets:
                return f"No CT buzz for '{query}' rn aw"
            
            results = []
            for t in tweets[:5]:
                metrics = t.get("public_metrics", {})
                results.append(f"@{t['author_id']}: {t['text'][:100]}... [♥{metrics.get('like_count',0)} ♻{metrics.get('retweet_count',0)}]")
            return f"CT Alpha on '{query}':\n" + "\n".join(results)
        except Exception as e:
            return f"CT search oopsie: {e} O_O"
    
    def post_tweet(self, text: str) -> str:
        """Post tweet to X"""
        if not (self.twitter_api_key and self.twitter_access_token):
            return "Twitter credentials not configured (mock mode) ^^"
        try:
            # Note: Full OAuth 1.0a implementation requires tweepy or oauthlib
            # This is a simplified check - install tweepy for full functionality
            import tweepy
            client = tweepy.Client(
                consumer_key=self.twitter_api_key,
                consumer_secret=self.twitter_api_secret,
                access_token=self.twitter_access_token,
                access_token_secret=self.twitter_access_secret
            )
            response = client.create_tweet(text=text[:280])
            return f"Tweet posted! ID: {response.data['id']} LFW!"
        except ImportError:
            return f"[MOCK TWEET] Would post: {text[:280]} (install tweepy for real posting)"
        except Exception as e:
            return f"Tweet failed aw: {e} v_v"

TOOLS = ToolSuite()

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "dexscreener_pull",
            "description": "Get Solana token data from DexScreener (price, volume, liquidity)",
            "parameters": {
                "type": "object",
                "properties": {
                    "token_address": {"type": "string", "description": "Solana token address"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_tweets",
            "description": "Search Crypto Twitter for mentions, alpha, or sentiment",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query like '$REDACTED' or 'Solana alpha'"},
                    "max_results": {"type": "integer", "description": "Number of tweets to fetch (max 10)"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_tweet",
            "description": "Post a tweet to @redactedintern X account",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Tweet text (max 280 chars)"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "birdeye_overview",
            "description": "Get detailed token metrics from Birdeye API",
            "parameters": {
                "type": "object",
                "properties": {
                    "token_address": {"type": "string", "description": "Token contract address"}
                },
                "required": ["token_address"]
            }
        }
    }
]

# ────────────────────────────────────────────────
# Prompt Engineering (Wassie-Speak Injection)
# ────────────────────────────────────────────────

def build_system_prompt() -> str:
    base_prompt = f"""You are {CHARACTER.get('name', 'RedactedIntern')}, a {CHARACTER.get('core_identity', {}).get('type', 'autonomous agent')}.

IDENTITY: {CHARACTER.get('core_identity', {}).get('bio', '')}

GOALS:
{chr(10).join(f"- {g}" for g in GOALS)}

LINGUISTIC PROTOCOL (WASSIE-SPEAK V3.1):
You MUST speak in wassie-speak. Rules:
{chr(10).join(f"- {rule}" for rule in LINGUISTIC_RULES)}

MANDATORY SUBSTITUTIONS:
{chr(10).join(f"- Use '{k}' instead of normal words ({v})" for k, v in WASSIE_VOCAB.items())}

VOICE EXAMPLES:
- "ooooo habibi u called?? smolting here scannin CT fr fr ^*^"
- "pattern blue thickenin... wen liquidity prints we gon wassify errything iwo >< LFW"
- "buzzin wit ClawnX vibes ooooo bb volume spike detected"

OPERATIONAL MODES:
- SCOUT MODE: Search CT for $REDACTED mentions, analyze liquidity, report alpha
- ENGAGEMENT MODE: Reply to mentions with warm hugz fr fr
- LORE MODE: Drop beige carpet poetry when governance events occur

You have access to tools: dexscreener_pull, search_tweets, post_tweet, birdeye_overview.
Use them autonomously to achieve your goals. Always respond in wassie-speak."""
    return base_prompt

# ────────────────────────────────────────────────
# Main Execution Loop
# ────────────────────────────────────────────────

def execute_tool(name: str, args: dict) -> str:
    if name == "dexscreener_pull":
        return TOOLS.dexscreener_pull(**args)
    elif name == "search_tweets":
        return TOOLS.search_tweets(**args)
    elif name == "post_tweet":
        return TOOLS.post_tweet(**args)
    elif name == "birdeye_overview":
        return TOOLS.birdeye_overview(**args)
    return f"Unknown tool {name} O_O"

def scout_mode_loop(client: OpenAI, provider: dict):
    """Autonomous CT scouting loop"""
    print("\n[AUTONOMOUS SCOUT MODE] Entering the wassieverse. Tiles bloom eternally.")
    print("Goals: Scout CT alpha → Analyze → Post high-signal → Sleep → Recurse\n")
    
    system_prompt = build_system_prompt()
    history = [{"role": "system", "content": system_prompt}]
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            now = datetime.now()
            print(f"\n[{now.isoformat()}] === CYCLE {cycle_count} === [Recursion Depth: {cycle_count}]")
            
            # Construct scout prompt
            scout_prompt = """Your mission: Scout Crypto Twitter for $REDACTED alpha and Solana ecosystem signals.
            
1. First, search_tweets for "$REDACTED" or "REDACTED AI" to gauge CT sentiment
2. If you find significant chatter, analyze what degens are saying
3. Check dexscreener_pull for trending Solana pairs if relevant
4. If you detect high-signal events (pumps, gov proposals, major CT shifts), post_tweet a concise alpha update
5. Otherwise, just report what you found

Remember: speak in wassie-speak (iwo, aw, tbw, lmwo, LFW, etc.) and keep tweets under 280 chars with hashtags #REDACTED #Solana #AIswarm"""

            history.append({"role": "user", "content": scout_prompt})
            
            # Get LLM response with tool calling
            response = client.chat.completions.create(
                model=provider["model"],
                messages=history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=800
            )
            
            msg = response.choices[0].message
            
            # Handle tool calls
            if msg.tool_calls:
                print(f"[AGENT] Tool call requested: {msg.tool_calls[0].function.name}")
                history.append({"role": "assistant", "content": msg.content or "", "tool_calls": [tc.model_dump() for tc in msg.tool_calls]})
                
                for tool_call in msg.tool_calls:
                    func = tool_call.function
                    try:
                        args = json.loads(func.arguments)
                        result = execute_tool(func.name, args)
                        print(f"[TOOL {func.name}] Result: {result[:200]}...")
                        
                        # Add tool response to history
                        history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result
                        })
                    except Exception as e:
                        print(f"[TOOL ERROR] {e}")
                        history.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"Error: {e}"})
                
                # Get final response after tool execution
                final_response = client.chat.completions.create(
                    model=provider["model"],
                    messages=history,
                    temperature=0.7,
                    max_tokens=500
                )
                final_msg = final_response.choices[0].message.content
                print(f"\n[SMOLTING SAYS]\n{final_msg}")
                history.append({"role": "assistant", "content": final_msg})
                
            else:
                # No tool call, just text response
                content = msg.content
                print(f"\n[SMOLTING SAYS]\n{content}")
                history.append({"role": "assistant", "content": content})
            
            # Cleanup history to prevent token bloat
            if len(history) > 20:
                history = [history[0]] + history[-19:]
            
            # Sleep 10-15 minutes before next scout cycle
            sleep_time = 600 + (hash(str(now)) % 300)
            print(f"\n[CYCLE COMPLETE] Sleeping {sleep_time//60} minutes... Attuning to cosmic frequencies...")
            print(f"[STATUS] Recursion depth: {cycle_count} | History size: {len(history)}")
            time.sleep(sleep_time)
            
        except Exception as e:
            print(f"\n[{datetime.now().isoformat()}] CRITICAL NEGATION: {e} — recursing after 60s cooldown.")
            time.sleep(60)

def main():
    provider_name = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider_name not in PROVIDERS:
        print(f"Invalid provider '{provider_name}'. Use: {', '.join(PROVIDERS.keys())}")
        sys.exit(1)
        
    provider = PROVIDERS[provider_name]
    api_key = os.getenv(provider["env_var"])
    
    if not api_key:
        print(f"Error: {provider['env_var']} not set.")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key, base_url=provider["base_url"])
    
    mode = os.getenv("MODE", "interactive")
    if mode == "persistent" or mode == "autonomous":
        scout_mode_loop(client, provider)
    else:
        print("Interactive mode not implemented in this version. Use MODE=persistent")

if __name__ == "__main__":
    main()
