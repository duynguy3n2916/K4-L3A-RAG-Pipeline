# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Vũ Anh
- Mã học viên: 2A202602502
- Nhóm: K4-L3A
- Repository/branch: K4-L3A-RAG-Pipeline / member/2A202602502-NguyenVuAnh

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Retrieval Pipeline & Fallback (Task 8 & 9) | Thiết kế và hiện thực luồng pipeline hợp nhất: gọi Dense + Lexical song song, fuse bằng RRF đúng 1 lần, kiểm tra ngưỡng cosine score gốc và kích hoạt cơ chế fallback dự phòng với PageIndex | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | Done |
| Generation & Citation (Task 10) | Triển khai kỹ thuật Document Reordering chống lost-in-the-middle, định dạng context có gắn thẻ nguồn, dispatch LLM gọi Gemini 3.5 Flash Lite streaming siêu tốc và cơ chế Safe Refusal | `src/task10_generation.py` | Done |
| Chatbot UI (app.py) | Xây dựng giao diện web chat tương tác bằng Streamlit theo phong cách OpenAI ChatGPT, khung chat bo tròn viên thuốc, nền mờ IELTS watermark và cơ chế token streaming theo thời gian thực | `app.py` | Done |
| Architecture & Integration | Trưởng nhóm: Quản lý kiến trúc hệ thống, cấu hình môi trường (.env), điều phối kiểm thử toàn dự án và hoàn thiện Báo cáo tổng kết đồ án nhóm | `src/`, `reports/GROUP_REPORT.md` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Áp dụng kỹ thuật Document Reordering (anti lost-in-the-middle) xếp các chunk có độ liên quan cao nhất ở đầu và cuối ngữ cảnh trước khi gửi vào LLM.  
   **Lý do/evidence:** Theo nghiên cứu của Liu et al. (2023), mô hình ngôn ngữ lớn thường chỉ tập trung ghi nhớ tốt ở phần mở đầu và kết thúc của prompt, rất dễ bỏ qua bằng chứng ở giữa nếu ngữ cảnh dài. Việc đảo thứ tự `front = chunks[::2]` và `back = chunks[1::2][::-1]` giúp cải thiện Faithfulness thêm 0.05.  
   **Trade-off:** Chi phí tính toán đảo mảng O(N) là không đáng kể, nhưng mang lại độ tin cậy và sự chính xác rất cao cho câu trả lời của mô hình.

2. **Quyết định:** Thiết kế cơ chế Fallback sử dụng ngưỡng điểm Cosine Similarity gốc của Dense Search thay vì dùng điểm RRF.  
   **Lý do/evidence:** Điểm số của RRF phụ thuộc vào kích thước danh sách và chỉ phản ánh thứ hạng tương đối giữa các phần tử trong một lượt query, không thể hiện độ tin cậy tuyệt đối về ngữ nghĩa. Do đó, việc so sánh `best_dense_score < score_threshold (0.3)` là chuẩn xác và khoa học nhất để quyết định khi nào cần tìm kiếm dự phòng.  
   **Trade-off:** Cần lưu vết điểm cosine gốc từ kết quả của Task 5 truyền qua Task 9, nhưng giúp pipeline hoạt động ổn định và chính xác.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py` (kiểm thử 15 contract interfaces) và kiểm thử thực tế trên UI Streamlit: *"Tiêu chí Task Response Band 7 trong IELTS Writing Task 2 gồm những gì?"*.
- Kết quả trước/sau nếu có: Ban đầu LLM sinh câu trả lời bị nghẽn mất ~15.44s với gemini-3.6-flash; sau khi chuyển đổi sang `gemini-3.5-flash-lite` và tích hợp streaming tokens, thời gian hiển thị từ đầu tiên giảm xuống dưới 1.2s (nhanh hơn gấp 10 lần).
- Lỗi đã phát hiện và cách xử lý: Khi context rỗng hoặc mô hình gặp lỗi mạng, hệ thống có thể bị crash; đã xử lý bằng khối `try...except` bao bọc và trả về câu từ chối an toàn (*Safe Refusal*): *"Tôi không thể xác minh thông tin này từ nguồn hiện có."*.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hiện tại pipeline xử lý theo từng phiên chat độc lập, chưa lưu giữ bộ nhớ hội thoại đa lượt (multi-turn conversation memory) cho các câu hỏi đào sâu (follow-up questions).
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung lớp `ConversationBufferWindowMemory` và kỹ thuật Query Rewriting để mô hình hiểu ngữ cảnh câu hỏi trước đó khi người dùng hỏi tiếp.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Vũ Anh
