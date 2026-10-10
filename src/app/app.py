import re
import time
import pathlib

import streamlit as st

from rag_from_scratch import Runnable

_CODE_BLOCK = re.compile(r"(```.*?```)", re.DOTALL)
_DISPLAY_DOLLAR = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)   # $$...$$
_DISPLAY_BRACKET = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)  # [ ... ]
_INLINE_PAREN = re.compile(r"\\\((.+?)\\\)", re.DOTALL)     # \(...\)

def _as_display_block(match: re.Match) -> str:
    return f"\n\n$$\n{match.group(1).strip()}\n$$\n\n"

def _as_inline(match: re.Match) -> str:
    return f"${match.group(1).strip()}$"

def normalize_latex(text: str) -> str:
    parts = _CODE_BLOCK.split(text)
    for i, part in enumerate(parts):
        if part.startswith("```"):
            continue
        part = _DISPLAY_DOLLAR.sub(_as_display_block, part)
        part = _DISPLAY_BRACKET.sub(_as_display_block, part)
        part = _INLINE_PAREN.sub(_as_inline, part)
        parts[i] = part
    return re.sub(r"\n{3,}", "\n\n", "".join(parts)).strip()

HISTORY_PATH = pathlib.Path(__file__).parent / "data" / "chat history" / "chat_history.json"
UPLOAD_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "docs"

# Ensure the upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

runnable = Runnable()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize a set in session state to track already processed file names
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# --- MOVED FILE UPLOADER TO SIDEBAR ---
st.set_page_config(layout="wide")
with st.sidebar:
    uploaded_files = st.file_uploader(
        label="Upload your PDFs", 
        type=["pdf"],
        accept_multiple_files=True
    )

st.title(body="Synap")
st.text(body="Instantly connect your research and unlock insights with AI.")
    
# Re-render previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if uploaded_files:
    # Filter out files that have already been processed in this session
    new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]

    if new_files:
        for uploaded_file in new_files:
            file_path: pathlib.Path = UPLOAD_DIR / uploaded_file.name

            # Open and write the file in binary mode
            with open(file_path, "wb") as fp:
                fp.write(uploaded_file.getbuffer())
            
            # Mark this file as processed
            st.session_state.processed_files.add(uploaded_file.name)

        # Show success message in the sidebar
        st.sidebar.success(f"Successfully saved and indexed {len(new_files)} new file(s)")

        # Run embedding chain ONLY when new files are added
        runnable.embedding_chain().invoke(input=pathlib.Path(__file__).parent.parent.parent / "data" / "docs")

if query := st.chat_input(placeholder="What is up?"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)                       

    with st.chat_message("assistant"):
        try:
            json_response: dict[str, str | None] = runnable.response_chain().invoke(
                input={
                    "query": query,
                    "docs_embeddings": runnable.embedding_obj.load_embeddings(),
                    "knowledge_base": runnable.text_splitter_obj.load_chunks()
                }
            )

            display_text: str = normalize_latex(json_response["main_explanation"])
        except Exception as e:
            print("Most probably - OutputParserException")
            display_text = "Thank you for reaching out. Unfortunately, I am unable to provide answers to these specific questions due to policy guidelines. Please feel free to ask about any other topics."

        runnable.memory_obj.save_chat_history(
            chat_history=runnable.current_chat_history, 
            path=pathlib.Path(__file__).parent.parent.parent / "data" / "artifacts" / "chat_history.json"
        )

        def stream_response():
            for char in display_text:
                yield char
                time.sleep(0.005)

        placeholder = st.empty()
        with placeholder:
            st.write_stream(stream_response)
        placeholder.markdown(display_text)

    st.session_state.messages.append({"role": "assistant", "content": display_text})