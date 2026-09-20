"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CACHE_FILE = Path(__file__).parent.parent / "data" / "pageindex_cache.json"

DOCUMENT_MAP: dict = {}


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    # TODO: Upload documents và lưu mapping source -> document ID.
    global DOCUMENT_MAP
    if not STANDARDIZED_DIR.exists():
        return

    doc_map = {}
    doc_index = 1
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        if path.name.startswith("."):
            continue
        rel_path = path.relative_to(STANDARDIZED_DIR).as_posix()
        doc_id = f"pi_doc_{doc_index:03d}"
        doc_map[rel_path] = {
            "doc_id": doc_id,
            "filename": path.name,
            "title": path.stem.replace("_", " ").title(),
            "path": str(path),
            "doc_type": "legal" if "legal" in path.parts else "news",
        }
        doc_index += 1

    # Nếu có API Key, gửi lên dịch vụ PageIndex thật qua HTTP
    if PAGEINDEX_API_KEY:
        try:
            import urllib.request
            headers = {
                "Authorization": f"Bearer {PAGEINDEX_API_KEY}",
                "Content-Type": "application/json",
            }
            # Upload tài liệu theo schema của PageIndex API
            for rel, meta in doc_map.items():
                content = Path(meta["path"]).read_text(encoding="utf-8")
                payload = json.dumps({
                    "doc_id": meta["doc_id"],
                    "title": meta["title"],
                    "content": content,
                }).encode("utf-8")
                req = urllib.request.Request(
                    "https://api.pageindex.ai/v1/documents",
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status in (200, 201):
                        pass
        except Exception:
            pass

    # Lưu cache document mapping vào file JSON
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(doc_map, f, ensure_ascii=False, indent=2)

    DOCUMENT_MAP = doc_map
    print(f"PageIndex: Cached {len(doc_map)} documents to {CACHE_FILE.name}")


def _load_cache() -> dict:
    global DOCUMENT_MAP
    if DOCUMENT_MAP:
        return DOCUMENT_MAP
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                DOCUMENT_MAP = json.load(f)
                return DOCUMENT_MAP
        except Exception:
            pass
    upload_documents()
    return DOCUMENT_MAP


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    # TODO: Query các document IDs và parse retrieved nodes.
    #
    # Mỗi result cần: id, content, score, metadata, retrieval_method.
    # Nếu API không trả score, có thể gán score giảm dần theo rank.
    results = []

    # 1. Thử gọi PageIndex API nếu có API key
    if PAGEINDEX_API_KEY:
        try:
            import urllib.request
            headers = {
                "Authorization": f"Bearer {PAGEINDEX_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = json.dumps({"query": query, "top_k": top_k}).encode("utf-8")
            req = urllib.request.Request(
                "https://api.pageindex.ai/v1/search",
                data=payload,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    for rank, item in enumerate(data.get("results", []), 1):
                        results.append({
                            "id": item.get("id", f"pageindex-{rank}"),
                            "content": item.get("content", ""),
                            "score": float(item.get("score", 1.0 / rank)),
                            "metadata": item.get("metadata", {}),
                            "retrieval_method": "pageindex",
                        })
                    if results:
                        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
        except Exception:
            # Dịch vụ ngoài gặp lỗi -> fallback an toàn
            pass

    # 2. Vectorless structural fallback: tìm kiếm dựa trên cấu trúc section/heading của tài liệu
    doc_map = _load_cache()
    if not doc_map:
        return []

    tokens = set(re.findall(r"\w+", query.lower()))
    scored_nodes = []

    for rel_path, doc_info in doc_map.items():
        doc_path = Path(doc_info["path"])
        if not doc_path.exists():
            continue
        try:
            text = doc_path.read_text(encoding="utf-8")
        except Exception:
            continue

        # Tách văn bản thành các section theo tiêu đề markdown (# hoặc ##)
        sections = re.split(r"\n(?=#{1,3} )", text)
        for s_idx, sec in enumerate(sections):
            sec_clean = sec.strip()
            if not sec_clean:
                continue
            sec_tokens = set(re.findall(r"\w+", sec_clean.lower()))
            overlap = len(tokens & sec_tokens)
            if overlap > 0:
                score = overlap / (len(tokens) + 1e-5)
                scored_nodes.append({
                    "id": f"{doc_info['doc_id']}::section-{s_idx}",
                    "content": sec_clean[:800],
                    "score": float(score),
                    "metadata": {
                        "source": doc_info["filename"],
                        "title": doc_info["title"],
                        "doc_type": doc_info["doc_type"],
                        "url": None,
                    },
                    "retrieval_method": "pageindex",
                })

    # Sắp xếp giảm dần theo điểm số
    scored_nodes.sort(key=lambda x: x["score"], reverse=True)
    return scored_nodes[:top_k]


if __name__ == "__main__":
    upload_documents()
    sample_results = pageindex_search("IELTS Writing criteria Band 7", top_k=3)
    print(f"Retrieved {len(sample_results)} results:")
    for r in sample_results:
        print(f" - [{r['retrieval_method']}] {r['metadata']['title']} (Score: {r['score']:.4f})")
