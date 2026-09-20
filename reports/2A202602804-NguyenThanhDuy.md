# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Thành Duy
- Mã học viên: 2A202602804
- Nhóm: K4-L3A
- Repository/branch: K4-L3A-RAG-Pipeline-NguyenThanhDuy-2A202602804 / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Ingestion & Preprocessing (Task 1–3) | Thu thập 4 PDF tiêu chí chấm thi IELTS Writing từ British Council/Cambridge, cào 6 bài viết hướng dẫn chuyên sâu từ IELTS Liz và chuẩn hóa sang Markdown đồng nhất | `src/task1_collect_legal_docs.py`, `src/task2_crawl_news.py`, `src/task3_convert_markdown.py` | Done |
| Chunking & ChromaDB Indexing (Task 4) | Cấu hình `RecursiveCharacterTextSplitter` (chunk_size 500, overlap 50) và nạp 167 chunks vào ChromaDB với cosine distance | `src/task4_chunking_indexing.py` | Done |
| Hybrid Retrieval (Task 5–7) | Triển khai Dense Semantic Search (BAAI/bge-m3), Lexical BM25Okapi và thuật toán RRF fusion với $k=60$ | `src/task5_semantic_search.py`, `src/task6_lexical_search.py`, `src/task7_reranking.py` | Done |
| Pipeline & Generation (Task 8–10) | Hợp nhất luồng retrieval có fallback threshold cho dense score, reorder chunks chống lost-in-the-middle và sinh câu trả lời kèm citation/safe refusal | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py`, `src/task10_generation.py` | Done |
| Evaluation & Streamlit UI | Xây dựng bộ golden dataset 15 câu Q&A về IELTS Writing, viết báo cáo đánh giá RESULT.md và hoàn thiện giao diện Chatbot Streamlit | `group_project/evaluation/golden_dataset.json`, `group_project/evaluation/RESULT.md`, `app.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Kết hợp BM25 và Dense Retrieval qua thuật toán RRF (Reciprocal Rank Fusion) thay vì cộng gộp tuyến tính điểm similarity.  
   **Lý do/evidence:** Thang đo của Cosine Similarity ($[0, 1]$) và BM25 ($[0, +\infty)$) hoàn toàn khác biệt. RRF tính điểm dựa trên thứ hạng (rank) $\sum \frac{1}{60 + \text{rank}}$, giúp dung hòa thế mạnh từ vựng chính xác (các thuật ngữ như "Band 7", "Task Achievement") của BM25 và ngữ nghĩa khái quát của Dense Search mà không làm sai lệch phân phối điểm.  
   **Trade-off:** Tăng nhẹ độ trễ tính toán (~12ms in-memory trên CPU) nhưng cải thiện Context Recall từ 0.80 lên 0.92 và Context Precision từ 0.78 lên 0.91 trên bộ test.

2. **Quyết định:** Áp dụng kỹ thuật Document Reordering (anti lost-in-the-middle) đưa các chunk điểm cao nhất về đầu và cuối context trước khi chuyển tới LLM.  
   **Lý do/evidence:** LLM có xu hướng tập trung mạnh vào thông tin ở phần mở đầu và kết thúc của prompt, dễ bỏ qua bằng chứng ở giữa nếu ngữ cảnh dài.  
   **Trade-off:** Tốn thêm thao tác sắp xếp mảng nhỏ (không đáng kể), đổi lại Faithfulness tăng thêm 0.05 và loại bỏ hiện tượng mô hình bỏ sót tiêu chí chấm điểm.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Bộ test tự động `tests/test_contracts.py` (15 test kiểm tra interface và contract) và `tests/test_acceptance.py` (5 test kiểm tra dữ liệu, golden dataset và báo cáo kết quả).
- Kết quả trước/sau nếu có: Trước khi hoàn thiện, gặp lỗi tie-breaker IDF=0 trên tập dữ liệu test nhỏ và các lỗi chưa implement; sau khi xử lý đạt 20/20 test PASSED (100%).
- Lỗi đã phát hiện và cách xử lý: ChromaDB không chấp nhận metadata chứa giá trị `None` (gây lỗi khi insert URL null); đã xử lý bằng cách chuẩn hóa `url: None` thành `""` trước khi upsert vào vector store và phục hồi lại khi trích xuất.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Chưa áp dụng metadata filtering theo từng band score (Band 5, 6, 7, 8, 9), dẫn đến khi hỏi sâu về một band nhất định, các chunk của band liền kề đôi khi vẫn lọt vào top-k do tính chất ngữ nghĩa gần nhau.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung bộ trích xuất metadata chuyên biệt để gắn nhãn `band_level` và `task_type` (Task 1 / Task 2) vào từng chunk, cho phép người dùng lọc chính xác trước khi retrieval.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Thành Duy
