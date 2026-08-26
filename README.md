# GenAI Assignment 1 — LangChain Chatbot

A practice project built with **LangChain, Pydantic, and Streamlit** to demonstrate prompt-based routing, parallel response generation, structured output, and a simple chat interface.

## Project Overview

This project implements an AI tutor chatbot where the user can select a **response category** and an **explanation level** before asking a question.

The chatbot supports three response categories:

- **General Intuition** — prioritizes theoretical and general explanations.
- **Programming Intuition** — prioritizes programming concepts, approaches, code, and short explanations.
- **Mathematical Intuition** — prioritizes mathematical concepts, terminology, equations, and explanations alongside equations.

The user can also select an explanation level:

- Beginner-Friendly
- Intermediate
- Deep Intuition

The application uses **ChatGroq** as the chat model and provides a Streamlit-based interface with chat history.

## Features

- Chatbot interface built with Streamlit.
- User-selectable response category.
- User-selectable explanation level.
- `PromptTemplate` for constructing prompts.
- `RunnableBranch` for category-based routing.
- `RunnableParallel` for generating answer and summary outputs simultaneously.
- Pydantic structured output using `PydanticOutputParser`.
- Chat history maintained with Streamlit session state.
- API credentials loaded through environment variables.

## LangChain Components

### 1. PromptTemplate

The project uses separate `PromptTemplate` objects for the three response categories. Each template receives the user's question, selected category, selected explanation level, and chat history as dynamic inputs.

This keeps prompt construction separate from model invocation and allows the chatbot to change its behavior according to the user's selections.

### 2. RunnableBranch

`RunnableBranch` routes the user's request according to the selected response category.

```text
Programming Intuition  → Programming Chain
Mathematical Intuition → Mathematical Chain
General Intuition      → General Chain
```

The implementation checks `category_input` and selects the corresponding prompt chain.

### 3. RunnableParallel

`RunnableParallel` is used to run two response pipelines from the same user request:

```text
User Question
      │
      ▼
 RunnableParallel
    ┌───────┴───────┐
    ▼               ▼
 Summary          Answer
```

Both outputs are generated through the conditional response chain and parsed into the project's structured Pydantic response format.

### 4. Pydantic Structured Output

The project defines a `Response` Pydantic model containing:

- `answer`
- `summary`
- `confidence`
- `category`
- `keywords`

`PydanticOutputParser` is used to validate model output against this schema.

## Project Structure

```text
GenAi-Assignment-1/
│
├── app.py              # Streamlit application and chatbot flow
├── chatbot.py          # ChatGroq model configuration
├── prompts.py          # PromptTemplate definitions
├── schemas.py          # Pydantic response schema and output parsers
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment-variable configuration
├── .gitignore          # Ignores the local .env file
└── README.md           # Project documentation
```

## Technologies Used

- Python
- LangChain
- LangChain Core
- ChatGroq
- Pydantic
- Streamlit
- python-dotenv

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/FuadTasin/GenAi-Assignment-1.git
cd GenAi-Assignment-1
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the API key required by the ChatGroq configuration.

Do **not** commit the `.env` file. The repository's `.gitignore` excludes `.env`.

### 5. Run the application

```bash
streamlit run app.py
```

## How It Works

The application follows this general workflow:

```text
User Question
      │
      ├── Response Category
      │
      └── Explanation Level
              │
              ▼
       RunnableBranch
       ┌──────┼──────┐
       ▼      ▼      ▼
   General  Math  Programming
       └──────┼──────┘
              ▼
       RunnableParallel
          ┌───┴───┐
          ▼       ▼
      Summary    Answer
          └───┬───┘
              ▼
     Pydantic Structured Output
              │
              ▼
       Streamlit Chat UI
```

The application also keeps the conversation in `st.session_state.chat_history` and passes the history into the response prompts so previous conversation context can be considered.

## Notes

This project was created primarily as a **practice/learning assignment** to understand and demonstrate LangChain Runnable components, prompt templates, Pydantic structured output, and Streamlit integration.

It is intentionally a relatively simple chatbot rather than a production-ready application.

## Assignment Requirements Covered

- [x] Chat model
- [x] PromptTemplate
- [x] Pydantic Structured Output
- [x] RunnableBranch
- [x] RunnableParallel
- [x] Streamlit chat interface
- [x] Chat history
- [x] `requirements.txt`
- [x] `.env` excluded from Git

## Author

**Fuad Tasin**

GitHub: https://github.com/FuadTasin
