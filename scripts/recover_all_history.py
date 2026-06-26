import os
import sqlite3
import json
import datetime

# ==============================================================================
# CONFIGURATION TARGET: Assign the exact historical folder name string here
# ==============================================================================
HISTORICAL_FOLDER = "YOUR_FOLDER_NAME_HERE"
# ==============================================================================

db_path = os.path.expandvars(fr"%APPDATA%\Cursor\User\workspaceStorage\{HISTORICAL_FOLDER}\state.vscdb")
output_path = os.path.expanduser("~/Desktop/Cursor_Complete_Chat_And_Responses.md")

if not os.path.exists(db_path):
    print(f"Extraction Error: Target database asset not found at path:\n{db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def extract_response_by_uuid(db_cursor, target_uuid, tool_type):
    """
    Scans the database tables dynamically depending on whether the transaction
    belongs to a workspace Chat panel or a Composer workspace tray.
    """
    try:
        if "COMPOSER" in tool_type:
            db_cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
            row = db_cursor.fetchone()
            if row and row[0]:
                data = json.loads(row[0])
                composers = data.get("composers", []) if isinstance(data, dict) else data
                for comp in composers:
                    conversation = comp.get("conversation", [])
                    for i, msg in enumerate(conversation):
                        if msg.get("role") in ["assistant", "ai-reply"]:
                            if target_uuid in str(msg) or (i > 0 and target_uuid in str(conversation[i-1])):
                                content = msg.get("content") or msg.get("text")
                                if content: return content.strip()
                                
        elif "CHAT" in tool_type:
            db_cursor.execute("SELECT value FROM ItemTable WHERE key = 'workbench.panel.aichat.view.aichat.chatdata'")
            row = db_cursor.fetchone()
            if row and row[0]:
                data = json.loads(row[0])
                tabs = data.get("tabs", []) if isinstance(data, dict) else data
                for tab in tabs:
                    bubbles = tab.get("bubbles", [])
                    for i, bubble in enumerate(bubbles):
                        if bubble.get("type") in ["ai-reply", "assistant"]:
                            if target_uuid in str(bubble) or (i > 0 and target_uuid in str(bubbles[i-1])):
                                content = bubble.get("text") or bubble.get("content")
                                if content: return content.strip()
    except Exception:
        pass
    return None

try:
    print("Mapping prompt tokens to matching multi-mode dialogue panels...")
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiService.generations'")
    row = cursor.fetchone()
    
    if not row or not row[0]:
        print("Error: Could not retrieve prompt signature tokens.")
        exit()
        
    generations = json.loads(row[0])
    if isinstance(generations, list):
        generations.sort(key=lambda x: x.get("unixMs", 0), reverse=True)
    else:
        generations = [generations]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏆 Complete Reconstructed Cursor Dialogue Journal\n")
        f.write(f"Source Repository Space ID: `{HISTORICAL_FOLDER}`\n")
        f.write("Timeline order: Newest discussions at the top.\n\n")
        f.write("---\n\n")
        
        reconstructed_count = 0
        
        for gen in generations:
            prompt_text = gen.get("textDescription", "").strip()
            if not prompt_text:
                continue
                
            reconstructed_count += 1
            uuid_str = gen.get("generationUUID", "")
            gen_type = str(gen.get("type", "UNKNOWN")).upper()
            icon = "💬" if "CHAT" in gen_type else "🛠️"
            
            unix_ms = gen.get("unixMs")
            time_str = "Unknown Date"
            if unix_ms:
                try:
                    time_str = datetime.datetime.fromtimestamp(unix_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    pass
                    
            f.write(f"## {icon} Discussion Thread #{reconstructed_count} | {time_str} | Tool: {gen_type}\n")
            f.write(f"*Generation Anchor UUID:* `{uuid_str}`\n\n")
            
            f.write("### 👤 YOUR PROMPT:\n")
            f.write(f"```text\n{prompt_text}\n```\n\n")
            
            ai_response = extract_response_by_uuid(cursor, uuid_str, gen_type)
            f.write("### 🤖 CURSOR AI RESPONSE:\n")
            if ai_response:
                f.write(f"{ai_response}\n\n")
            else:
                f.write("> *Note: Response details are kept inside a background checkpoint snapshot or local file state.*\n\n")
                
            f.write("---\n\n")
            
    print(f"\n🎉 Finished! Reconstructed {reconstructed_count} dialogue sequences.")
    print(f"File saved to Desktop: Cursor_Complete_Chat_And_Responses.md")

except Exception as e:
    print(f"Extraction failed: {e}")
finally:
    conn.close()
