

**Agentic-Flow** is a production-grade Multi-AI Agent system designed to solve complex, real-time reasoning tasks. By leveraging **LangGraph** for stateful orchestration and **Groq’s LPU** hardware for lightning-fast inference, the system breaks down user queries into manageable sub-tasks. Each task is assigned to specialized agents—such as a **Research Agent** (using Tavily) or a **Reasoning Agent** (using Llama 3)—ensuring highly accurate, up-to-date, and context-aware response



### 2.Core features:

* **Stateful Multi-Agent Orchestration:** Uses **LangGraph** to manage cycles and conditional branching, allowing agents to "think," "search," and "verify" before responding.^^
* **High-Speed Inference:** Integrated with **Groq API** to deliver real-time performance (sub-second response times) using cutting-edge models like Llama 3.^^
* **Real-Time Knowledge Retrieval:** Utilizes the **Tavily Search API** to bypass LLM knowledge cutoffs and fetch verified internet data.^^
* **Scalable Backend Architecture:** Built on  **FastAPI** **, enabling asynchronous request handling and high concurrency.**^^
* **Enterprise UI:** A clean, intuitive chat interface built with **Streamlit** for seamless user interaction.^^

### 3.Technical Stack (The "LLM-DevOps" Loop)


| **Category**         | **Tools Used**          |
| -------------------------- | ----------------------------- |
| **Orchestration**    | LangGraph, LangChain          |
| **LLM Provider**     | Groq (LPU Inference), Llama 3 |
| **Real-time Search** | Tavily API                    |
| **Backend API**      | FastAPI, Pydantic, Uvicorn    |
| **Frontend UI**      | Streamlit                     |
| **CI/CD & Quality**  | Jenkins, SonarQube            |
| **Infrastructure**   | Docker, AWS (EC2/ECS), WSL 2  |

### **4. System Architecture**

1. **Input:** The user submits a query via the **Streamlit** interface.^^
2. **API Gateway:****FastAPI** receives the payload and triggers the LangGraph workflow.^^
3. **Agent Logic:** * The **Orchestrator** determines if external research is needed.
   * **The ****Search Agent** fetches real-time data via  **Tavily** **.**^^
   * The **Reasoning Agent** (Groq) synthesizes the data into a final answer.
4. **DevOps Pipeline:** Every code change is scanned by **SonarQube** for security/quality and automatically deployed via **Jenkins** to an  **AWS** -hosted **Docker** container.


### **5. Why this project is "Production-Ready"**

Unlike simple "Prompt-and-Response" chatbots, this project addresses the core challenges of AI engineering:

* **Reliability:** Implements **HTTPException** handling and data validation to prevent crashes.
* **Transparency:** Uses **LangSmith** or custom logging to track agent thought processes.
* **Efficiency:** The **DevOps pipeline** ensures that only high-quality, bug-free code reaches the AWS environment.
