import sqlite3
from google import genai
from datetime import datetime

# ── Configure Gemini ──────────────────────────────────────────────────────────
client = genai.Client(api_key="AIzaSyD-iAWrcKTKfXJ49DSV07UMEL5wDLNX0K8")  # ← paste your key here

# ── Connect to database ───────────────────────────────────────────────────────
conn   = sqlite3.connect("sales.db")
cursor = conn.cursor()

# ── Query history ─────────────────────────────────────────────────────────────
history = []   # each entry: { question, sql, rows, columns, time }

# ── Helpers ───────────────────────────────────────────────────────────────────

def divider(char="─", width=64):
    print(char * width)

def print_banner():
    print()
    divider("═")
    print("  🧠  I n t e l l i S Q L")
    print("  Intelligent SQL Querying · Powered by Gemini")
    divider("═")
    print("  Commands:  'history'  · 'clear'  · 'exit'")
    divider()
    print()

def print_table(columns, rows):
    """Print rows as a formatted ASCII table."""
    if not rows:
        print("  (no rows returned)")
        return

    # Calculate column widths
    col_widths = [len(str(c)) for c in columns]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Build format string
    row_fmt  = "  │ " + " │ ".join(f"{{:<{w}}}" for w in col_widths) + " │"
    sep_line = "  ├─" + "─┼─".join("─" * w for w in col_widths) + "─┤"
    top_line = "  ┌─" + "─┬─".join("─" * w for w in col_widths) + "─┐"
    bot_line = "  └─" + "─┴─".join("─" * w for w in col_widths) + "─┘"

    print(top_line)
    print(row_fmt.format(*[str(c).upper() for c in columns]))
    print(sep_line)
    for row in rows:
        print(row_fmt.format(*[str(v) for v in row]))
    print(bot_line)
    print(f"  {len(rows)} row{'s' if len(rows) != 1 else ''} returned")

def print_history():
    if not history:
        print("  No queries yet.\n")
        return
    divider()
    print("  📋  QUERY HISTORY")
    divider()
    for i, entry in enumerate(history, 1):
        print(f"  [{i}] {entry['time']}  →  {entry['question']}")
        print(f"       SQL: {entry['sql']}")
        print(f"       Rows: {entry['rows']}")
        print()
    divider()

def generate_sql(question):
    prompt = f"""
    You are an expert SQL assistant.

    Table:
    customers(id, name, city, purchase_amount)

    Convert the question below to a valid SQLite SQL query.
    Return ONLY the SQL query — no explanation, no markdown, no backticks.

    Question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    sql = response.text.strip()

    # Strip markdown fences if present
    if sql.startswith("```"):
        lines = sql.splitlines()
        sql   = "\n".join(lines[1:-1]).strip()

    return sql

def run_query(sql):
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows    = cursor.fetchall()
    return columns, rows

# ── Main loop ─────────────────────────────────────────────────────────────────

print_banner()

while True:
    try:
        question = input("  Ask your database: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n  Goodbye!")
        break

    if not question:
        continue

    # ── Built-in commands ──
    if question.lower() == "exit":
        print("\n  Goodbye!")
        break

    if question.lower() == "history":
        print_history()
        continue

    if question.lower() == "clear":
        history.clear()
        print("  History cleared.\n")
        continue

    # ── Generate SQL ──
    print("\n  ⏳ Thinking...", end="\r")
    try:
        sql_query = generate_sql(question)
    except Exception as e:
        print(f"  ✗ Gemini error: {e}\n")
        continue

    print(f"  ✓ Generated SQL:")
    print(f"    {sql_query}\n")

    # ── Execute SQL ──
    try:
        columns, results = run_query(sql_query)
        print_table(columns, results)

        # Save to history
        history.append({
            "question": question,
            "sql":      sql_query,
            "rows":     len(results),
            "columns":  columns,
            "time":     datetime.now().strftime("%H:%M:%S"),
        })

    except Exception as e:
        print(f"  ✗ Query error: {e}")

    print()

conn.close()


