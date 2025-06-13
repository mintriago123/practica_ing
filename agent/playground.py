from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
import os

agent_storage: str = "tmp/agents.db"

web_agent = Agent(
    name="Michael Intriago",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools()],
    instructions=["Always include sources"],
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

app = Playground(agents=[web_agent, finance_agent]).get_app()

# --- HABILITAR CORS SOLO PARA TU UI ---
try:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://icy-ground-0f6a42f1e.1.azurestaticapps.net"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
except ImportError:
    pass  # Si no es FastAPI/Starlette, ignora CORS

# --- MOSTRAR URL PÚBLICA AL ARRANCAR ---
def print_public_url(port):
    public_url = os.environ.get("PUBLIC_URL")
    if public_url:
        print(f"Playground URL (AZURE): {public_url}")
    else:
        print(f"Playground URL (local): http://localhost:{port}")

# --- ENDPOINT PARA OBTENER LA URL PÚBLICA DESDE EL REQUEST ---
try:
    from fastapi import Request
    @app.get("/public-url")
    async def public_url(request: Request):
        host = request.headers.get("host", f"localhost:{port}")
        scheme = "https" if os.environ.get("WEBSITES_ENABLE_HTTPS") == "1" or os.environ.get("PUBLIC_URL", "").startswith("https") else "http"
        return {"public_url": f"{scheme}://{host}/"}
except Exception:
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    print_public_url(port)
    serve_playground_app("playground:app", reload=True, port=port)