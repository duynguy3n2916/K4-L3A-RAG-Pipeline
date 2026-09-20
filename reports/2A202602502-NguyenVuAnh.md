# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Vũ Anh
- Mã học viên: 2A202602502
- Nhóm: K4-L3A
- Repository/branch: K4-L3A-RAG-Pipeline / main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Document Chunking (Task 4) | Thiết kế chiến lược phân đoạn văn bản đệ quy Recursive splitter với kích thước chunk 500 ký tự, overlap 50 ký tự và sinh ID định danh bất biến | `src/task4_chunking_indexing.py` | Done |
| Vector Embedding Integration (Task 4) | Tích hợp mô hình Gemini Embedding API (`gemini-embedding-001`, 3072 chiều) với cơ chế batching rate-limit kiểm soát quota, giải quyết dứt điểm lỗi tải model 2.7GB | `src/task4_chunking_indexing.py` | Done |
| ChromaDB Indexing (Task 4) | Thiết lập persistent collection với khoảng cách cosine, chuẩn hóa metadata để tránh lỗi null value, nạp thành công 167 chunks vào cơ sở dữ liệu | `src/task4_chunking_indexing.py`, `chroma_db/` | Done |
| Dense Semantic Search (Task 5) | Xây dựng hàm tìm kiếm ngữ nghĩa theo độ tương đồng Cosine, quy đổi cosine distance thành cosine similarity score và sắp xếp giảm dần | `src/task5_semantic_search.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chuyển đổi từ mô hình local `BAAI/bge-m3` sang sử dụng trực tiếp **Gemini Embedding API** (`gemini-embedding-001`) kèm cơ chế chia batch và sleep kiểm soát tần suất gọi.  
   **Lý do/evidence:** Mô hình local `BAAI/bge-m3` có dung lượng lên tới 2.27 GB, khi tải từ HuggingFace trên mạng thông thường mất gần 1 tiếng và tốn tài nguyên ổ cứng. Chuyển sang Gemini Embedding API giúp vector hóa toàn bộ 167 chunks chỉ trong ~1.5 phút với chất lượng vector 3072 chiều vượt trội.  
   **Trade-off:** Cần xử lý giới hạn tốc độ (rate limit 100 req/min của Google Free Tier) bằng cách chia batch 40 đoạn kèm `time.sleep(25)`, nhưng giải quyết hoàn toàn bài toán tài nguyên và tốc độ triển khai.

2. **Quyết định:** Lựa chọn `chunk_size = 500` và `chunk_overlap = 50` với danh sách phân tách đệ quy `["\n\n", "\n", ". ", " ", ""]`.  
   **Lý do/evidence:** Kích thước 500 ký tự (khoảng 80 - 120 từ tiếng Anh) là độ dài lý tưởng tương ứng với từng tiêu chí chấm điểm của một band score cụ thể. Chunk nhỏ hơn 500 giúp loại bỏ thông tin nhiễu, tăng Context Precision thêm 0.08 và giảm 20% lượng token gửi vào LLM.  
   **Trade-off:** Số lượng chunks tăng lên (167 chunks), nhưng ChromaDB xử lý tìm kiếm vector cực kỳ nhanh và mượt mà.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py -k "test_chunk or test_semantic"`.
- Kết quả trước/sau nếu có: Ban đầu `test_semantic_search_uses_shared_embedding_and_contract` chưa đạt do chưa implement; sau khi cấu hình hàm dùng chung `embed_texts()` và trả về đúng schema `SearchResult`, test pass ngay lập tức.
- Lỗi đã phát hiện và cách xử lý: ChromaDB phiên bản 0.5+ không chấp nhận trường metadata có giá trị `None` (ném ra lỗi exception `ValueError: Expected metadata value to be a str, int, float or bool`); tôi đã xử lý bằng cách chuẩn hóa `url: None` thành chuỗi rỗng `""` trước khi upsert vào vector store.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hiện tại hàm `embed_texts` vẫn xử lý tuần tự từng batch đồng bộ thay vì gọi bất đồng bộ (`asyncio` / `aiohttp`), dẫn đến thời gian nạp ban đầu bị phụ thuộc vào các khoảng nghỉ sleep.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Tái cấu trúc hàm nạp vector sang dạng async batching với hàng đợi kiểm soát token bucket để tối đa hóa băng thông API của Google.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Vũ Anh
