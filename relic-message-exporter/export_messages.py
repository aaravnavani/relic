import sqlite3
import json
from pathlib import Path

output_path = Path.home() / "Downloads/messages.json"
db_path = Path.home() / "Library/Messages/chat.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
SELECT datetime(message.date / 1000000000 + strftime('%s','2001-01-01'), 'unixepoch') as timestamp,
       handle.id as sender,
       message.text
FROM message
LEFT JOIN handle ON message.handle_id = handle.ROWID
WHERE message.text IS NOT NULL
ORDER BY timestamp DESC
""")

rows = cursor.fetchall()
conn.close()

messages = [{"timestamp": r[0], "sender": r[1], "text": r[2]} for r in rows]

with open(output_path, "w") as f:
    json.dump(messages, f, indent=2)

print(output_path)