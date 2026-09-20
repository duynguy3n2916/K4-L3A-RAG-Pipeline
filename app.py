import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_stream


load_dotenv()

st.set_page_config(
    page_title="IELTS Writing Assistant",
    page_icon="✍️",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("✍️ IELTS Writing Assistant")
    st.caption("Tra cứu tiêu chí chấm điểm Band Descriptors & bài mẫu IELTS Writing Task 1 và Task 2.")
    top_k = st.slider("Số chunks truy xuất (top_k)", 3, 10, 5)
    st.divider()
    st.markdown("**Kiến trúc RAG:**")
    st.markdown("- Dense Semantic Search (`gemini-embedding-001`)")
    st.markdown("- Lexical BM25 Search (Cached Index)")
    st.markdown("- RRF Reranking (Hybrid Fusion)")
    st.markdown("- LLM: `gemini-3.5-flash-lite` (Ultra-low latency streaming)")

st.title("✍️ Trợ lý IELTS Writing RAG")
st.caption("Đặt câu hỏi về tiêu chí Band Score (Task 1 & Task 2), kỹ thuật làm bài và từ vựng biểu đạt.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # TODO: Hiển thị sources và retrieval score.
        if message.get("sources"):
            with st.expander(f"📚 Nguồn trích dẫn ({message.get('retrieval_source', 'hybrid')})"):
                for idx, src in enumerate(message["sources"], 1):
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{idx}] {meta.get('title', 'Tài liệu')}** (Nguồn: `{meta.get('source', '')}` | Score: `{src.get('score', 0):.4f}`)")
                    st.caption(src.get("content", ""))

query = st.chat_input("Nhập câu hỏi về IELTS Writing (ví dụ: Tiêu chí Band 7 Task 2 gồm những gì?)...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm tài liệu..."):
            # TODO: Gọi generate_stream(query, top_k).
            stream_gen, sources, retrieval_source = generate_stream(query, top_k=top_k)

        answer = st.write_stream(stream_gen)

        # TODO: Hiển thị sources và citation.
        if sources:
            with st.expander(f"📚 Nguồn trích dẫn ({retrieval_source})"):
                for idx, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{idx}] {meta.get('title', 'Tài liệu')}** (Nguồn: `{meta.get('source', '')}` | Score: `{src.get('score', 0):.4f}`)")
                    st.caption(src.get("content", ""))

        # TODO: Lưu answer và sources vào session state.
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "retrieval_source": retrieval_source,
        })
