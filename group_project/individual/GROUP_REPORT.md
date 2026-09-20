# BÁO CÁO TỔNG KẾT ĐỒ ÁN NHÓM
## HỆ THỐNG RAG PIPELINE — TRỢ LÝ TRA CỨU IELTS WRITING

---

### THÔNG TIN DỰ ÁN
* **Khóa học:** K4 AI Engineer / Advanced RAG
* **Nhóm:** L3A
* **Đề tài:** Xây dựng hệ thống RAG Pipeline hỗ trợ tra cứu tiêu chí chấm điểm và hướng dẫn viết IELTS Writing (Task 1 & Task 2)
* **Kho lưu trữ (Repository):** [K4-L3A-RAG-Pipeline](https://github.com/duynguy3n2916/K4-L3A-RAG-Pipeline-NguyenThanhDuy-2A202602804)
* **Ngày hoàn thành:** 20/09/2026

---

### 1. DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG NHIỆM VỤ

| STT | Họ và tên | Mã học viên | Vai trò | Phân công nhiệm vụ chính | Trạng thái |
| :-: | :--- | :---: | :--- | :--- | :-: |
| 1 | **Nguyễn Thành Duy** | **2A202602804** | Trưởng nhóm (Leader) / System Architect | - Pipeline hợp nhất và Fallback logic (Task 8, 9)<br>- Generation có Citation & Safe Refusal (Task 10)<br>- Phát triển giao diện Chatbot Streamlit (`app.py`)<br>- Tích hợp hệ thống và quản lý cấu hình chung | **100% (Done)** |
| 2 | **Trương Việt Anh** | **2A202602444** | Data Engineer | - Thu thập 4 tài liệu PDF chính thức (Task 1)<br>- Crawl 6 bài viết chuyên sâu từ IELTS Liz (Task 2)<br>- Chuẩn hóa toàn bộ dữ liệu sang Markdown (Task 3)<br>- Kiểm thử bộ dữ liệu thô và dữ liệu chuẩn hóa | **100% (Done)** |
| 3 | **Nguyễn Vũ Anh** | **2A202602502** | Vector DB & Semantic Search Specialist | - Chiến lược phân đoạn Recursive Character Splitter (Task 4)<br>- Tích hợp Gemini Embedding API kiểm soát rate-limit (Task 4)<br>- Thiết lập ChromaDB persistent collection cosine distance (Task 4)<br>- Triển khai Dense Semantic Search (Task 5) | **100% (Done)** |
| 4 | **Phạm Quang Đạt** | **2A202602704** | Search Algorithm & Evaluation Specialist | - Thuật toán tìm kiếm từ khóa chính xác BM25Okapi (Task 6)<br>- Thuật toán Reranking Reciprocal Rank Fusion - RRF (Task 7)<br>- Xây dựng bộ Golden Dataset 15 câu Q&A tiếng Việt<br>- Đánh giá thực nghiệm A/B Testing & viết RESULT.md | **100% (Done)** |

---

### 2. TỔNG QUAN KIẾN TRÚC HỆ THỐNG (END-TO-END RAG PIPELINE)

Hệ thống được thiết kế theo kiến trúc 5 tầng tiêu chuẩn công nghiệp:

```text
[Dữ liệu thô (PDF & Web)] 
       ↓ (Task 1, 2)
[Landing Data (PDF & JSON)] 
       ↓ (Task 3: MarkItDown)
[Standardized Markdown (10 docs)] 
       ↓ (Task 4: Recursive Splitter - 500 chars, overlap 50)
[167 Chunks] 
       ↓ (Task 4: Gemini Embedding - 3072 dim)
[ChromaDB Vectorstore] 
       ↓ (Task 9: Retrieval Pipeline)
    ┌──────────────────────────────────────────────────┐
    │  Query → Dense Search (top-k*2) via ChromaDB     │
    │  Query → Lexical Search (top-k*2) via BM25       │
    │  Fusion → RRF Reranking (k=60) → Top-k Hybrid    │
    │  Fallback Check: best_dense_score < 0.3          │
    │    └── Nếu thấp: Gọi PageIndex Fallback          │
    └──────────────────────────────────────────────────┘
       ↓ (Task 10: Document Reordering)
[Reordered Context (Chống Lost-in-the-middle)] 
       ↓ (Task 10: Gemini 3.6 Flash + System Instruction)
[Câu trả lời có Citation & Grounding] 
       ↓
[Giao diện Chatbot Streamlit (app.py)]
```

---

### 3. CÔNG NGHỆ VÀ THƯ VIỆN SỬ DỤNG

* **Vector Database:** ChromaDB (Persistent client, metric `cosine`).
* **Dense Embedding:** Google Gemini Embedding API (`gemini-embedding-001`, vector 3072 chiều) kèm batching rate-limit kiểm soát quota.
* **Lexical Search:** `rank_bm25` (`BM25Okapi`) với bộ giải quyết hòa điểm `match_count * 1e-4`.
* **Reranking:** Reciprocal Rank Fusion (RRF, hằng số $k=60$).
* **Generator / LLM:** Google Gemini 3.6 Flash (`gemini-3.6-flash`).
* **Web Crawler & Converter:** `Crawl4AI` (Async Web Crawler), `MarkItDown` (Microsoft).
* **Giao diện người dùng:** Streamlit (`app.py`) với session state và hiển thị nguồn động.
* **Đánh giá & Kiểm thử:** Ragas 0.4.3, Pytest.

---

### 4. KẾT QUẢ ĐÁNH GIÁ THỰC NGHIỆM (A/B TESTING)

Nhóm tiến hành đánh giá so sánh hiệu năng trên **15 ca kiểm thử thực tế của bộ Golden Dataset** giữa hai cấu hình:
* **Config A:** Dense-only (chỉ dùng vector search qua ChromaDB).
* **Config B:** Hybrid + RRF (kết hợp Dense Search + Lexical BM25 + RRF Reranking).

| Chỉ số Ragas | Config A (Dense-only) | Config B (Hybrid + RRF) | Chênh lệch (Delta) | Nhận xét |
| :--- | :---: | :---: | :---: | :--- |
| **Faithfulness** (Tính trung thực) | 0.82 | **0.94** | **+0.12** | Giảm thiểu tối đa hiện tượng ảo giác (hallucination). |
| **Answer Relevance** (Độ liên quan câu trả lời) | 0.85 | **0.95** | **+0.10** | Trả lời trực diện vào trọng tâm câu hỏi của người dùng. |
| **Context Recall** (Độ bao quát ngữ cảnh) | 0.80 | **0.92** | **+0.12** | Không bỏ sót các điều kiện trong tiêu chí chấm điểm. |
| **Context Precision** (Độ tập trung ngữ cảnh) | 0.78 | **0.91** | **+0.13** | Loại bỏ thông tin nhiễu từ các band điểm liền kề. |
| **ĐIỂM TRUNG BÌNH** | **0.8125** | **0.9300** | **+0.1175 (+11.75%)** | **Config B vượt trội toàn diện trên cả 4 thước đo.** |

---

### 5. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG (ACCEPTANCE & CONTRACT TESTS)

Hệ thống vượt qua **20/20 bài kiểm thử tự động** đạt tỷ lệ **100% PASS**:
* `tests/test_contracts.py` (15/15 PASS): Đảm bảo tuyệt đối schema `Document`, `SearchResult`, `GenerationResult`, tính bất biến của ID và chữ ký hàm ổn định.
* `tests/test_acceptance.py` (5/5 PASS): Xác thực toàn vẹn dữ liệu quy chuẩn ($\ge 3$ PDF), dữ liệu bài viết ($\ge 5$ JSON kèm metadata), chuẩn hóa Markdown, bộ dữ liệu vàng ($\ge 15$ ca Q&A) và báo cáo đánh giá đầy đủ.

---

### 6. HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

1. **Kích hoạt môi trường ảo:**
   ```powershell
   ..\.venv\Scripts\Activate.ps1
   ```
2. **Chạy kiểm thử toàn diện:**
   ```powershell
   pytest tests/
   ```
3. **Khởi chạy ứng dụng Chatbot:**
   ```powershell
   streamlit run app.py
   ```

---

### 7. DANH SÁCH BÁO CÁO CÁ NHÂN ĐÍNH KÈM
* [Báo cáo cá nhân — Nguyễn Thành Duy (2A202602804)](2A202602804-NguyenThanhDuy.md)
* [Báo cáo cá nhân — Trương Việt Anh (2A202602444)](2A202602444-TruongVietAnh.md)
* [Báo cáo cá nhân — Nguyễn Vũ Anh (2A202602502)](2A202602502-NguyenVuAnh.md)
* [Báo cáo cá nhân — Phạm Quang Đạt (2A202602704)](2A202602704-PhamQuangDat.md)
