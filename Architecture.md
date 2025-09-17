# 🧠 AI Architecture of the Ikman Vehicle Finder

The system is **modular**, with each AI component handling a specific role. Together, they form a lightweight **AI pipeline** that goes from human query → structured search → intelligent recommendation → conversational output.

---

## 1. **Input Layer (User Query)**

* User enters free-form text like:
  *“I want a vehicle under 20M for my daily 10km office commute”*
* Input goes into the **Query Analyser** module.

---

## 2. **Query Analyser (Intent Normalizer – LLM)**&#x20;

* Uses **Groq LLM** with a **prompt-engineered system role**.
* Converts natural language into **exactly 2 category keywords** (e.g., *Car, Hybrid*).
* Rules baked into the prompt:

  * Budget normalization → maps LKR ranges into vehicle categories.
  * Distance/usage → influences type (*Scooter vs. Car vs. SUV*).
  * Fuel/economy hints → adds *Hybrid/Electric/Diesel* if needed.

**Output**: `["Car", "Hybrid"]`

---

## 3. **Vehicle Finder (Scraper + Data Layer)**&#x20;

* Uses **Requests + BeautifulSoup** to scrape Ikman.lk.
* Converts raw HTML → structured JSON (title, link, image, price, mileage, location, updated time).
* This forms the **knowledge base** the AI will reason over.

**Output**: JSON ads list

---

## 4. **Result Builder (LLM Response Generator)**&#x20;

* Takes:

  * Original user query
  * JSON ads list
* Uses Groq LLM with a **vehicle-expert system prompt** to:

  * Compare ads (price, location, mileage, freshness).
  * Select the **most relevant matches**.
  * Generate a **short, conversational summary** (Markdown formatted).

**Output**:

> “Best fit: 🚘 Toyota Axio Hybrid around Rs 15M, updated just now.
> Also consider a Wagon R for \~12M if you prefer compact options.”

---

## 5. **Presentation Layer (FastAPI + Frontend)**&#x20;

* **FastAPI Endpoints**:

  * `/vehicles` → raw scrape results.
  * `/search` → AI-powered recommendations.
* **Frontend (index.html)**:

  * Chat-style interface.
  * Renders LLM’s Markdown response into styled cards.

---

# 🔗 Flow Diagram (Conceptual)

```mermaid
graph TD
  A[User Query] --> B[Query Analyser (Groq LLM)]
  B -->|Keywords| C[Vehicle Scraper (Ikman.lk)]
  C -->|JSON Ads| D[Result Builder (Groq LLM)]
  D -->|Markdown Summary| E[FastAPI + Frontend UI]
```

---

# 🎯 Key Takeaway

This architecture is a **mini RAG-like pipeline** (Retrieval + Generation):

* **Retrieval** → scrape live vehicle listings.
* **Generation** → use LLM to reason & recommend.
* **Orchestration** → FastAPI ties it all together into a working app.