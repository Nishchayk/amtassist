# AmtAssist

A RAG-powered assistant that answers questions about German bureaucracy for international students in Berlin.

## The Problem

International students in Berlin struggle with German bureaucracy — Anmeldung, visa extensions, health insurance, tax registration, Bürgeramt appointments. Official information is scattered, often only in German, and written in complex legal language. Students waste hours Googling and asking WhatsApp groups for answers that should be simple to find.

## The Solution

A retrieval-augmented generation (RAG) system that:

- Ingests trusted English-language sources about German bureaucracy
- Uses a local large language model to answer student questions in plain English
- Cites which source each answer came from, so users can verify

## Tech Stack

- **Language Model:** Llama 3.2 (3B) via Ollama, running locally
- **Vector Database:** ChromaDB for semantic search over documents
- **Embeddings:** sentence-transformers
- **Backend:** FastAPI (Python)
- **Frontend:** HTML + vanilla JavaScript
- **Deployment:** Hugging Face Spaces

## Status

**Week 1 (April 2026):** In progress — building foundational setup and first LLM integration.

**Day 1-2 (April 18-19):** Python virtual environment created. FastAPI installed and hello-world endpoint running locally. GitHub repo initialized with .gitignore and README.

**Day 3 (April 22):** Ollama installed. Llama 3.2 (3B) model pulled and running locally. First Python-to-LLM call successful via `test_llm.py`. Experimented with and without system prompts to observe behavior differences.

**Week 2 — Session 1 (April 28):** Installed `requests` library. Wrote `fetch_one_page.py` to download a single web page from allaboutberlin.com via HTTPS GET request. Confirmed working: HTTP 200 response, ~150KB of raw HTML returned. Observed that raw HTML is dominated by metadata, scripts, and styling — only a small fraction is actual content. Next session: BeautifulSoup parsing to extract just the readable text.

**Week 2 — Sessions 2+3 (May 3):** Installed BeautifulSoup. Modified `fetch_one_page.py` to parse HTML and extract clean readable text. Added file saving with explicit UTF-8 encoding to `data/` folder. Reduced 155,929 chars of raw HTML to 1,296 chars of clean text — a 99.2% noise reduction. Confirmed correct UTF-8 storage by verifying German characters (ü, ä, ß) render properly in VS Code despite Windows terminal mojibake. Lesson: trust the file, not the terminal display.

**Key observation — hallucinations:** Model invented a fake government office acronym ("AEMV") in one response, and incorrectly stated the Anmeldung is done at the Ausländerbehörde in another. The correct location is the Bürgeramt. System prompts reduced verbosity but did not fix factual errors. This confirms the core premise of the project: generic LLMs cannot be trusted with specific bureaucratic facts without RAG grounding.

Building in public — roadmap and weekly progress updates below.

## Roadmap

- [x] Local LLM integration (Ollama)
- [x] Multi-URL document ingestion pipeline
- [x] Text chunking with overlap
- [x] Embedding pipeline (sentence-transformers)
- [x] ChromaDB indexing with metadata
- [x] Semantic retrieval verified
- [ ] End-to-end RAG integration in FastAPI /ask endpoint
- [ ] Frontend (HTML + JS)
- [ ] Deployment to Hugging Face Spaces
- [ ] Error handling and edge cases
- [ ] Blog post documenting the build

## Why I'm Building This

I'm an international student in Berlin doing an MS in AI. I'm building this both because the problem is real for me and my classmates, and because it's a learning project to develop production AI engineering skills with LLMs, vector databases, and deployment.

## About Me

Software engineer with 2 years of Python backend experience from India, currently pursuing MS in AI in Berlin. Graduating August 2027.


## Week 1 Learnings

### What I Built

A working FastAPI server with two endpoints, including an `/ask` endpoint that accepts a user question via URL parameter, sends it to a local Llama 3.2 (3B) model running on Ollama, and returns the answer as JSON. The whole stack runs locally — no API keys, no cloud dependencies. Set up with a Python virtual environment, version-controlled with Git, and pushed to GitHub with a clean commit history.

### What Surprised Me

I expected my first AI project to involve building a chat UI — input box, send button, message bubbles. Instead, the most important thing I built this week was a URL endpoint that returns JSON. Realizing that almost every AI product is just a URL accepting input and returning structured data was a fundamental shift in how I think about AI engineering. The UI is a thin layer on top — the real work is the API.

### What Broke and How I Fixed It

The biggest recurring issue was Git. On Day 2, my push was rejected because GitHub had a README I'd created in the browser that my local repo didn't know about. I learned about merging unrelated histories with `git pull --allow-unrelated-histories`. On Day 4, I hit an Internal Server Error when calling my `/ask` endpoint, and learned to read FastAPI tracebacks — the actual cause was a typo in the model name (`ollama3.2:3b` instead of `llama3.2:3b`), buried inside dozens of framework lines. The lesson: scroll to the bottom of the traceback first, then look for the line referencing your own code.

The bigger Git lesson was establishing the **pull-before-push** habit. Always `git pull` before `git push`. This single habit prevents most Git conflicts.

### Hallucinations — The Most Important Observation

I asked the model "What is the Anmeldung?" three times across different prompts. I got three different wrong answers. One invented a fake government office acronym ("AEMV"). One claimed it was done at the Ausländerbehörde. One claimed it was specific to international students in Berlin. The correct answer — done at the Bürgeramt, required of every resident regardless of nationality — never appeared. System prompts asking the model to "say I'm not certain" did not fix this. The model is confidently wrong, every time, in different ways.

This is the entire reason this project exists. RAG is one of the most important techniques for getting reliable responses from a language model — without it, the model produces confident wrong answers that could actively mislead users.

### What I'd Do Differently

I'd be more disciplined about taking the planned rest days. Early in the week, I felt guilty about resting and tried to push through. I quickly realized that exhausted coding produces more bugs and weaker learning. The days I rested were the days my next session was sharpest. The plan works *because* of the rest, not in spite of it.

### What I'm Taking Into Week 2

A working Git workflow (pull, then push), a habit of reading tracebacks from the bottom up, and an understanding that LLMs hallucinate so confidently that prompts alone cannot fix it. Week 2 starts the real solution: ingesting trusted documents that the model will be forced to ground its answers in.
