# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Thành Duy
- Mã học viên: 2A202602804
- Nhóm: K4-L3A
- Repository/branch: K4-L3A-RAG-Pipeline / member/2A202602804-NguyenThanhDuy

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Legal Documents Collection (Task 1) | Nghiên cứu, tuyển chọn và viết script tải 4 tài liệu PDF tiêu chí chấm điểm chính thức từ British Council và Cambridge Assessment (Band Descriptors Task 1 & 2, Examiner Criteria, Model Answers) | `src/task1_collect_legal_docs.py`, `data/landing/legal/` | Done |
| Web News Crawling (Task 2) | Xây dựng trình thu thập dữ liệu bất đồng bộ với Crawl4AI, cào 12 bài viết chuyên sâu về phương pháp làm bài, từ vựng collocations, tiêu chí chấm và các dạng bài từ chuyên trang IELTS Liz | `src/task2_crawl_news.py`, `data/landing/news/` | Done |
| Markdown Standardization (Task 3) | Ứng dụng công cụ MarkItDown để chuyển đổi cấu trúc PDF và JSON sang Markdown chuẩn hóa, bảo toàn cấu trúc bảng tiêu chí và gắn đầy đủ metadata phục vụ trích dẫn | `src/task3_convert_markdown.py`, `data/standardized/` | Done |
| Data Acceptance Verification | Kiểm tra chất lượng dữ liệu thu thập, đảm bảo 16 tài liệu không rỗng, kích thước đạt chuẩn (> 1024 bytes) và độ dài ký tự đạt yêu cầu | `tests/test_acceptance.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng công cụ `MarkItDown` để chuyển đổi tài liệu PDF tiêu chí chấm điểm thay vì các thư viện đọc text thuần túy như PyPDF hay pdfminer.  
   **Lý do/evidence:** Bảng tiêu chuẩn chấm thi IELTS Writing Band Descriptors có cấu trúc bảng đa cột phức tạp (Task Response, Coherence & Cohesion, Lexical Resource, Grammar). Các thư viện text thông thường làm dính các cột chữ vào nhau làm mất ngữ nghĩa. `MarkItDown` giữ lại được định dạng phân cấp Markdown và cấu trúc bảng rõ ràng.  
   **Trade-off:** Thời gian xử lý file PDF bằng MarkItDown lâu hơn đọc plain text khoảng 1-2 giây cho mỗi tài liệu, nhưng chất lượng văn bản chuẩn hóa đầu ra cao hơn hẳn.

2. **Quyết định:** Thiết kế cấu trúc JSON lưu trữ bài viết cào từ web có schema metadata bắt buộc (`url`, `title`, `date_crawled`, `content_markdown`) và gắn header metadata ở đầu file Markdown.  
   **Lý do/evidence:** Giúp bảo toàn nguồn gốc xuất xứ của từng tài liệu xuyên suốt từ khâu landing đến khâu trích xuất (retrieval) và sinh trích dẫn (citation) của Task 10.  
   **Trade-off:** Tăng thêm dung lượng lưu trữ nhỏ cho metadata nhưng thỏa mãn hoàn toàn `test_corpus_has_required_news_with_metadata` và `MODULE_CONTRACTS.md`.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Chạy `pytest tests/test_acceptance.py -k "test_corpus or test_standardized"`.
- Kết quả trước/sau nếu có: Trước khi hoàn thiện, thư mục `data/` chưa có dữ liệu khiến 3 acceptance test bị FAIL; sau khi hoàn thiện script và thu thập đủ 16 tài liệu (4 PDF + 12 bài viết), cả 3 test dữ liệu đều PASS tuyệt đối (100%).
- Lỗi đã phát hiện và cách xử lý: Tiêu đề cào về từ web thường dính hậu tố tên trang web (ví dụ ` - IELTS Liz`), đã xử lý bằng chuỗi xử lý `.split(" - IELTS Liz")[0].strip()` để tiêu đề tài liệu được ngắn gọn và sạch sẽ.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Đối với các bảng số liệu phức tạp trong PDF Task 1 Model Answers, một số ký hiệu bảng đặc biệt vẫn chưa được chuyển đổi thành bảng Markdown Table dạng grid chuẩn.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Tích hợp công cụ Document Intelligence chuyên dụng (như MinerU hoặc Docling) để trích xuất bảng biểu đa cột thành Markdown Table hoàn hảo 100%.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Thành Duy
