# Privacy / data handling (local beta)

- Birth time, birthplace, current location, goals and preferences are voluntary.
- The application stores personal profiles only in the local private data directory:
  `~/.local/share/divine-arsenal` by default (permissions 0700; SQLite 0600).
- No external APIs are called during normal chart calculations.
- Clicking **Search birthplace** explicitly sends the search string to OpenStreetMap Nominatim.
- Each user can view, update, export or delete their profiles from the same trusted local account. Exports contain sensitive birth data and goals and must be kept private.
- This preview provides no accounts, encrypted storage, tenant isolation or remote access;
  do not run it on a shared OS account.
- Staged agent workspaces can contain goals; deleting a profile also removes its staged workspace (best effort; backups, prior copies and exported files remain separate).
- Raw data must not be checked into GitHub or sent to agents/cloud models without consent.
