# Cursor Trial Reset, Chat Recovery & Safe Telemetry Utilities 🚀

A comprehensive, open-source resource for Cursor IDE trial reset, recovering lost AI chat history and safely managing local metadata in the Cursor IDE. 

## ⚠️ The Problem with Traditional Reset Scripts
Many "trial reset" scripts floating around GitHub repos/issues violently wipe your data using broad wildcards like `Remove-Item -Path $dbPath -Force`. This removes your global tracking database without backups, leaving your Cursor previous chat sidebars completely empty and broken.

### Why Your Chats Disappear
Cursor splits its storage architecture across two separate local directories:
1. **Global Storage (`globalStorage`):** Houses the active UI multi-turn session records and conversational responses.
2. **Workspace Storage (`workspaceStorage`):** Maintains your localized workspace hashes, project preferences, and an immutable log of **all text prompts, instructions, and architectural plans** (`aiService.generations`).

When a blind script deletes the global database file, your workspace logs become "orphaned." Cursor can no longer link them to the UI, resulting in a blank sidebar. **However, your raw data is still 100% safe on your drive.**

---

## 📁 Repository Structure
```text
Cursor-Trial-Reset-Chat-Recovery/
│
├── README.md                  # Complete documentation, analysis, and guides
├── LICENSE                    # MIT License
├── cursor_trial_reset.ps1     # UPGRADED: Safe reset script with auto-backups
├── cursor_rollback_backup.ps1 # ROLLBACK: Restores native UI sidebars from a backup
└── scripts/
    └── recover_all_history.py # EXTRACTION: Reconstructs prompt & response journals
```

---

## 🛠️ Data Recovery Guide (Prompt & Response Extraction)

If your sidebars are currently empty, you can bypass Cursor's broken tracking layer entirely and parse out every single conversation tab, user prompt, AI response, and Composer session into a clean, searchable Markdown file.

### Step 1: Locate your Historical Project Folder 
*(Each folder represents a chat session tab on Cursor, so you can identify the folder name that corresponds to the chat session you want to recover)*

1. Press `Win + R`, paste the path below, and hit **Enter**:
   ```text
   %APPDATA%\Cursor\User\workspaceStorage
   ```
2. Switch your view settings to **Details** and click the **Date Modified** column to sort the directories chronologically.
3. Identify the alphanumeric folder name that was modified immediately prior to your data loss event (e.g., `a1b2c3d4...`). Copy this folder string name.

### Step 2: Extract Your Markdown History Journal
1. Make sure Cursor is completely closed.
2. Open `scripts/recover_all_history.py` inside a text editor.
3. Replace the placeholder on **Line 8** (`YOUR_FOLDER_NAME_HERE`) with your copied folder string name.
4. Open your terminal or PowerShell environment and execute the script:
   ```powershell
   python scripts/recover_all_history.py
   ```
5. Open the newly generated `Cursor_Complete_Chat_And_Responses.md` notebook sitting directly on your **Desktop**.

*Note: The script dynamically targets both standard **Chat Panels** and **Composer Trays**, indexing your user queries alongside their corresponding AI response blocks chronologically from newest to oldest.*

---

## 🔒 Safe Reset Script (With Automated Backups)

The `cursor_trial_reset.ps1` script provided in this repository prevents data loss by implementing defensive validation hooks:
* **Forced Task Termination:** Gracefully terminates active and hidden file-watching daemon threads to prevent background disk overwrite failures.
* **Snapshot Archiving:** Copies and timestamp-locks your global relational files into a protected `Backup_History/` directory before any initialization adjustments take place.

### Execution Directions
1. Open PowerShell as an **Administrator**.
2. Run the safe script directly:
   ```powershell
   ./cursor_trial_reset.ps1
   ```

---

## 🔄 Reversing the Reset (Native UI Rollback)

If you use our safe script (`cursor_trial_reset.ps1`) and later decide you want your original workspace sidebars and native previous chat list back, you can achieve **100% native UI recovery** with a single command.

Our script automatically reads your file system state, finds the most recent valid backup file, wipes the empty placeholder files, and stitches the original database structure back together.

### Rollback Directions
1. Open PowerShell as an **Administrator**.
2. Execute the restoration script layout:
   ```powershell
   ./cursor_rollback_backup.ps1
   ```
3. Relaunch Cursor. Your previous conversations will immediately pop back into view exactly where you left them.

---

## 💡 Troubleshooting & Core Fallbacks

### Pro-Tip: Check for Hidden Auto-Saves First
Before you execute any extraction scripts, open `%APPDATA%\Cursor\User\globalStorage` in Windows File Explorer. Look closely for a file named `state.vscdb.backup` or `state.vscdb.corrupted.[TIMESTAMPS]`. 

If Cursor experiences a crash or sudden process termination during a script run, it will sometimes preserve a clean backup array under these extensions to prevent structural data corruption. If you see a file of this nature that is several hundred KB or MB in size, simply delete the new empty `state.vscdb` file, rename the backup file back to exactly `state.vscdb`, and your native sidebar history will fully restore on launch.

### Missing AI Answers? Grab Code Backups
If the Python extraction engine outputs a prompt but notes that the corresponding AI answer layer is missing, it means that instead of a traditional text response, the AI performed raw direct file manipulation on your project workspace. 

Cursor caches every single inline file refactor and change event separately from its chat databases. You can locate and pull your written scripts at any timestamp by reviewing:
```text
%APPDATA%\Cursor\User\History
```
Sort that folder by **Date Modified** to locate your exact files from your last development session.


### ⚠️ A Note on Native Sidebar UI Recovery

**Can you make the Cursor IDE sidebar go back to exactly how it looked before running a destructive trial reset script?**

No. If the trial reset script successfully deleted the `globalStorage/state.vscdb` file without a backup, the native sidebar "Previous Chats" list cannot be repopulated. 

Cursor separates data explicitly: the workspace database tracks the user prompts, while the global database acts as the master host for the actual multi-turn AI response text and session records. Once that global file is deleted, the unique database row IDs are destroyed forever.

However, **your data is never truly gone**:
1. Your prompts, long-form ideas, and architectural instructions can be extracted entirely using the `recover_all_history.py` script provided in this repo.
2. Any code blocks, file refactors, or script extensions that the AI applied to your workspace are safely preserved via local timeline backups. You can access these raw file states anytime by heading to `%APPDATA%\Cursor\User\History` and filtering by timestamp.



> 💡 **PRO-TIP BEFORE RECOVERING:** Before you run any scripts, open `%APPDATA%\Cursor\User\globalStorage` in Windows File Explorer. Look closely for a file named `state.vscdb.corrupted.[TIMESTAMPS]` or `state.vscdb.backup`. Sometimes, if Cursor crashes or is abruptly terminated by a script, it auto-renames your massive chat history database to prevent data overwrites. If you find a file like `state.vscdb.corrupted` that is several megabytes or gigabytes in size, simply rename it back to `state.vscdb`, and your native sidebar history will completely reappear on your next launch!


---

## Contributing

Contributions are welcome! Feel free to submit Pull Requests.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request


## 📜 License
This project is open-source and licensed under the [MIT License](LICENSE). Contributions, multi-platform adaptations (macOS/Linux), and feedback are welcome!


## ⚠️ Disclaimer
This tool is for educational purposes only. If you find the Cursor editor useful, please support the developers by purchasing a license.