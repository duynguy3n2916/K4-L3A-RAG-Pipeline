import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_stream


load_dotenv()

st.set_page_config(
    page_title="IELTS Writing AI Assistant",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS cho phong cách ChatGPT & Theme IELTS với Watermark mờ
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container chính căn giữa kiểu ChatGPT */
    .main .block-container {
        max-width: 860px;
        padding-top: 1.5rem;
        padding-bottom: 7rem;
    }

    /* Hình nền mờ Watermark chữ IELTS phong cách học thuật */
    [data-testid="stAppViewContainer"] {
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650"><g fill="none" stroke="%23e01a22" stroke-width="2.5" opacity="0.045"><circle cx="500" cy="270" r="190"/><circle cx="500" cy="270" r="170" stroke-dasharray="8 8"/><path d="M500,105 L500,435 M335,270 L665,270"/></g><text x="50%" y="44%" text-anchor="middle" dominant-baseline="middle" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="180" fill="%23e01a22" opacity="0.04" letter-spacing="16">IELTS</text><text x="50%" y="58%" text-anchor="middle" dominant-baseline="middle" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="28" fill="%23002f6c" opacity="0.04" letter-spacing="14">WRITING ASSISTANT</text></svg>');
        background-repeat: no-repeat;
        background-position: center 40%;
        background-attachment: fixed;
        background-size: 780px auto;
    }

    /* Chat message container kiểu ChatGPT */
    [data-testid="stChatMessage"] {
        padding: 1.1rem 1.4rem !important;
        border-radius: 18px !important;
        margin-bottom: 1.25rem !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }

    /* Phân biệt bong bóng chat của User (viền đỏ IELTS nhẹ) */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(224, 26, 34, 0.06) !important;
        border: 1px solid rgba(224, 26, 34, 0.22) !important;
    }

    /* Khung nhập liệu ChatGPT thanh thoát ở đáy màn hình */
    [data-testid="stChatInput"] {
        border-radius: 28px !important;
        border: 1.5px solid rgba(224, 26, 34, 0.35) !important;
        box-shadow: 0 6px 28px rgba(0, 0, 0, 0.22) !important;
        transition: all 0.25s ease !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #e01a22 !important;
        box-shadow: 0 0 0 3px rgba(224, 26, 34, 0.2), 0 8px 30px rgba(0, 0, 0, 0.3) !important;
    }

    /* Header IELTS Badge */
    .ielts-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 0.25rem;
    }

    .ielts-badge {
        background: linear-gradient(135deg, #e01a22, #c8102e);
        color: #ffffff;
        font-weight: 900;
        font-size: 1.15rem;
        padding: 4px 12px;
        border-radius: 6px;
        letter-spacing: 1.5px;
        box-shadow: 0 2px 10px rgba(224, 26, 34, 0.35);
    }

    .ielts-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .ielts-pill {
        background: rgba(34, 197, 94, 0.12);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.25);
        font-size: 0.75rem;
        padding: 2px 10px;
        border-radius: 9999px;
        font-weight: 600;
    }

    /* Cards gợi ý câu hỏi ban đầu */
    .suggestion-card {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(224, 26, 34, 0.2);
        background: rgba(224, 26, 34, 0.03);
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .suggestion-card:hover {
        border-color: #e01a22;
        background: rgba(224, 26, 34, 0.08);
        transform: translateY(-2px);
    }

    /* Expander trích dẫn nguồn */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt_to_submit" not in st.session_state:
    st.session_state.prompt_to_submit = None

# Sidebar cấu hình và tra cứu
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <span style="background: #e01a22; color: white; font-weight: 900; font-size: 1.1rem; padding: 3px 10px; border-radius: 5px;">IELTS</span>
        <span style="font-size: 1.25rem; font-weight: 700;">Writing Lab</span>
    </div>
    """, unsafe_allow_html=True)

    # Nút tạo hội thoại mới kiểu ChatGPT
    if st.button("➕ Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.session_state.prompt_to_submit = None
        st.rerun()

    st.caption("Trợ lý tra cứu tiêu chí Band Descriptors, kỹ thuật viết Task 1 & Task 2.")
    st.divider()

    top_k = st.slider("Số chunks truy xuất (top_k)", 3, 10, 5)

    st.markdown("**Kiến trúc RAG tối ưu:**")
    st.markdown("- 🚀 **LLM**: `gemini-3.5-flash-lite` *(Streaming ~1.2s)*")
    st.markdown("- 🔍 **Dense**: `gemini-embedding-001` *(3072 dims)*")
    st.markdown("- 📑 **Sparse**: BM25 Okapi *(In-Memory Cache)*")
    st.markdown("- ⚖️ **Reranking**: Reciprocal Rank Fusion (RRF)")

    st.divider()
    st.markdown("**4 Tiêu chí chấm điểm Writing:**")
    st.markdown("- 🎯 **TR / TA**: Task Response & Achievement")
    st.markdown("- 🔗 **CC**: Coherence & Cohesion")
    st.markdown("- 📖 **LR**: Lexical Resource")
    st.markdown("- ⚖️ **GRA**: Grammatical Range & Accuracy")

# Header chính phong cách IELTS
st.markdown("""
<div class="ielts-header">
    <span class="ielts-badge">IELTS</span>
    <span class="ielts-title">Writing Assistant</span>
    <span class="ielts-pill">⚡ Fast RAG v2.0</span>
</div>
""", unsafe_allow_html=True)
st.caption("Tra cứu chuẩn xác tiêu chí chấm điểm Band 1.0 – 9.0, cấu trúc bài viết và bài mẫu chuẩn IELTS.")

# Nếu chưa có tin nhắn nào, hiển thị màn hình chào mừng & 4 thẻ gợi ý câu hỏi phong cách ChatGPT
if len(st.session_state.messages) == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 **Task 1: Cấu trúc Overview chuẩn**\n\nCách viết đoạn tổng quan ăn trọn điểm Task 1?", use_container_width=True):
            st.session_state.prompt_to_submit = "Cách viết đoạn Overview trong IELTS Writing Task 1 để đạt điểm cao là gì?"
            st.rerun()

        if st.button("🎯 **Task 2: Tiêu chí Band 7 Task Response**\n\nYêu cầu phát triển luận điểm và lập trường?", use_container_width=True):
            st.session_state.prompt_to_submit = "Tiêu chí Task Response Band 7 trong IELTS Writing Task 2 gồm những gì?"
            st.rerun()

    with col2:
        if st.button("⏱️ **Chiến lược quản lý 60 phút**\n\nPhân bổ thời gian 20p Task 1 và 40p Task 2 hợp lý?", use_container_width=True):
            st.session_state.prompt_to_submit = "Chiến lược phân bổ 60 phút cho IELTS Writing Task 1 và Task 2 hiệu quả nhất?"
            st.rerun()

        if st.button("✍️ **Các dạng bài kinh điển Task 2**\n\nCấu trúc 5 dạng bài Opinion, Discussion, Problem...?", use_container_width=True):
            st.session_state.prompt_to_submit = "Có các dạng bài luận nào trong IELTS Writing Task 2 và cấu trúc làm bài từng dạng?"
            st.rerun()

# Hiển thị lịch sử hội thoại
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "✍️"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        # TODO: Hiển thị sources và retrieval score.
        if message.get("sources"):
            with st.expander(f"📚 Nguồn trích dẫn ({message.get('retrieval_source', 'hybrid')})"):
                for idx, src in enumerate(message["sources"], 1):
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{idx}] {meta.get('title', 'Tài liệu')}** (Nguồn: `{meta.get('source', '')}` | Score: `{src.get('score', 0):.4f}`)")
                    st.caption(src.get("content", ""))

# Nhận câu hỏi từ input hoặc thẻ gợi ý
user_input = st.chat_input("Nhập câu hỏi về IELTS Writing (ví dụ: Tiêu chí Band 7 Task 2 gồm những gì?)...")

query = None
if st.session_state.prompt_to_submit:
    query = st.session_state.prompt_to_submit
    st.session_state.prompt_to_submit = None
elif user_input:
    query = user_input

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="✍️"):
        with st.spinner("Đang tìm kiếm tài liệu và đối chiếu tiêu chuẩn IELTS..."):
            # TODO: Gọi generate_with_citation(query, top_k).
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
