"""Edit this file: everything personal lives here."""
USERNAME = "DnOsoro"
HANDLE = "danvas@github"          # shown in the card
NAME = "Danvas Osoro"          # <-- check / change

# Rows of the neofetch-style card: (key, value)
INFO = [
    ("Role",      "Data Engineer"),
    ("Now",       "E-Commerce Lakehouse & RAG System"),
    ("Stack",     "Python, SQL, PySpark, DuckDB"),
    ("Cloud",     "AWS, Databricks, Delta Lake"),
    ("Pipelines", "Airflow, Kafka, batch + streaming"),
    ("Design",    "Medallion lakehouses, hybrid RAG"),
    ("AI",        "Multi-agent SQL, vector search"),
    ("Education", "JKUAT"),
    ("Contact",   "github.com/DnOsoro"),
]

# ---------- portfolio layout ----------
TAGLINE = "I build the data pipelines that make AI answers trustworthy."
LINKEDIN = "https://www.linkedin.com/in/danvas-osoro-26745a376/"

# (repo, one-line pitch, tags)  -> shown as clickable cards. Edit the pitches freely.
PROJECTS = [
    ("data-intelligence-workspace", "Enterprise natural-language data workspace with agentic NL2SQL.",
     ["Python", "NL2SQL", "Agents"]),
    ("production-rag", "Modular RAG system combining BM25 Okapi and ChromaDB vector retrieval.",
     ["Python", "RAG", "ChromaDB", "BM25"]),
    ("enterprise-ai-analyst", "Turns business questions into SQL, runs them on DuckDB, explains the result.",
     ["Python", "DuckDB", "NL2SQL"]),
    ("ensinyo-dairy-ai", "Dairy farm management platform: analytics, AI insights, learning and a marketplace.",
     ["TypeScript", "Analytics", "AI"]),
]

# Skill groups for the stack panel
STACK = [
    ("Languages",        ["Python", "SQL", "TypeScript"]),
    ("Data engineering", ["PySpark", "Airflow", "Kafka", "Pandera", "Pandas"]),
    ("Storage & Cloud",  ["PostgreSQL", "Delta Lake", "Databricks", "AWS", "SeaweedFS (S3)"]),
    ("AI layer",         ["LLMs (Gemini)", "NL2SQL", "RAG", "ChromaDB"]),
    ("Delivery",         ["FastAPI", "Next.js", "Docker", "Vercel"]),
]
