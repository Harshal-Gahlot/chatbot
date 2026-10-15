# Agents.md - Chatbot Project Guide

## Project Structure

``` python
chatbot/
├── .env                  # Environment variables (APP_MODE=groq)
├── .example.env          # Example env template
├── .venv/               # Python virtual environment
├── requirements.txt      # Dependencies (10 packages)
├── src/                 # Source code directory (MOVED FROM root)
│   ├── __init__.py       # (if needed for package imports)
│   ├── app.py           # Chainlit web UI entry point (246 lines)
│   ├── config.py        # Configuration & env loading (76 lines)
│   ├── llm_error_handling.py  # Error wrapper (19 lines)
│   ├── terminal.py      # CLI chat interface (30 lines)
│   ├── tools.py         # Web search tool (48 lines)
│   └── utils.py         # File handling & PDF extraction (52 lines)
├── supabase_client.py   # Empty placeholder (0 lines, not imported)
├── README.md
├── prompt.env.md        # Fallback system prompt source
└── Harshal_Gahlot_Resume.pdf  # Reference document
```

## Key Files & Responsibilities

### `src/config.py` - Configuration Manager

- Loads `.env` via `python-dotenv`
- Supports 3 LLM providers: `groq`, `openrouter`, `local`
- **Current provider**: `groq` (from `.env`)
- Sets: `BASE_URL`, `API_KEY`, `MODEL`, `TEMPERATURE`
- Creates Supabase client instance at `config.SUPABASE`
- **Known issue**: Raises `ValueError` if required env vars missing (lines 40-45)

### `src/app.py` - Chainlit Web UI (246 lines)

**Entry point for web chats. Handles:**

- OAuth login (Google provider via `cl.oauth_callback`)
- Chat initialization with system prompt
- Message processing with tool calling
- Web search integration via `tools_schema`
- File upload support (PDFs, text files) via `utils.extractUploadedFilesByUser()`
- Chat resume from thread state
- Custom `CustomDataLayer` for Supabase file storage (lines 225-246)
- Error handling with stack traces (uses `utils.printError`)

### `src/tools.py` - Web Search Tool

- Uses `ddgs` library to search text queries
- Returns top 8 results formatted as "Title | Body | URL"
- Schema defined in `tools_schema` list (used by Chainlit's `tools` parameter)
- **Single tool**: `search_web` only (extensible via schema)

### `src/utils.py` - File & PDF Handling

- `getContent()`: Extracts text from PDF pages using `PyPDF2`
- `extractUploadedFilesByUser()`: Processes uploaded elements, appends content to message
- `getFileContentFromElement()`: Fetches file content via HTTP GET, supports text/pdf
- `printError()`: Red-colored console output helper
- **Missing**: File type/size validation

### `src/llm_error_handling.py` - Error Wrapper

- `handle_error(fun, *args)`: Catches exceptions, prints traceback with line numbers
- Used by `terminal.py` and could be used by `app.py`

### `src/terminal.py` - CLI Chat Interface

- Standalone CLI using `main.py` patterns
- Reads from `config` for model/settings
- Loop until user types "bye"
- Wraps `chat()` with `handle_error()` for crash protection

## Environment Setup

### `.env` (active - groq mode)

```
APP_MODE=groq
MODEL='qwen/qwen3.8-27b'
OPENROUTER_API_KEY=sk-or-v1-...
GROQ_API_KEY=gsk_...
CHAINLIT_AUTH_SECRET=...
OAUTH_* credentials
SUPABASE_URL/KEY pairs
DATABASE_URL local/prod
```

### `.example.env` (template for new deployments)

```
APP_MODE=local
MODEL='qwen/qwen3.8-27b'
... (other vars empty)
```

**To activate**: `export $(grep -v '^#' .env | xargs)` or simply ensure `.env` exists with correct values.

## Known Issues & Todo Items

### Critical Blockers

1. **Config initialization**: Must have `APP_MODE` and `MODEL` env vars set before importing `config`

### High Priority

1. **Duplicate error handling**: Both `llm_error_handling.py` and `utils.py:49-52` define `printError()` - consolidate
2. **No file validation**: `utils.py` accepts any mime with "text" or "pdf" substring - add size/type checks
3. **Missing tests**: No test files found; critical paths (`tools.py`, `utils.py`, `config.py`) untested

### Medium Priority

1. **Magic numbers**: `max_iterations=5` (app.py:73), temperature values hardcoded
2. **Print statements instead of logging**: Throughout app.py and utils.py (logging commented out at app.py:22)
3. **Single tool only**: Only `search_web` implemented; `tools_schema` allows more

### Low Priority

1. **No CLI args**: `main.py` and `terminal.py` hardcode provider selection
2. **No .env.example documented**: `.example.env` exists but minimal
3. **Fragile prompt loading**: `config.py:10-19` fallback chain for SYS_PROMPT

### Tech Debt (Planned)

 1. **`supabase_client.py` empty**: 0 lines, not imported anywhere - can be removed or implemented
 2. **`config.py` refactor planned**: User has future plans for comprehensive rewrite
 3. **`app.py` module size**: 246 lines handles auth, chat, tools, data layer - consider splitting

## Development Commands

```bash
# Activate venv
source .venv/bin/activate

# Install deps (if needed)
pip install -r requirements.txt

# Run with proper path
cd chatbot && .venv/bin/python -c "import sys; sys.path.insert(0, 'src'); from src/config import config; print(config.MODEL)"

# Or set env vars first
export APP_MODE=groq
export MODEL='qwen/qwen3.8-27b'
.venv/bin/python main.py  # or src/terminal.py
```

## Likely Future Changes

Based on user's intent:

- Full `config.py` rewrite planned
- Potential removal of `supabase_client.py`
- Test suite addition
- Module splitting for `app.py`
- File upload validation improvements
- agent able to send auther an email on aproval/behalf of user chatting with it.
- vision integration for image processing and analysis
- fetch GitHub data on any profile including author's
- fetch LinkedIn data on any profile including author's
- better search engine tool then ddgs
