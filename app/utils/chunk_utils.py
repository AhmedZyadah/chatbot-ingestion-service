
def chunk_text(pages, chunk_size=200, overlap=30):
    chunks = []
    current_chunk = []
    current_word_count = 0
    current_pages = set()

    for page in pages:
        words = page["text"].split()
        current_pages.add(page["page"])

        for word in words:
            current_chunk.append(word)
            current_word_count += 1

            if current_word_count >= chunk_size:
                # حفظ chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "chunk": chunk_text,
                    "pages": sorted(list(current_pages))
                })

                # تحضير chunk جديد مع overlap
                current_chunk = current_chunk[-overlap:]
                current_word_count = len(current_chunk)
                current_pages = set([page["page"]])  # إعادة التهيئة

    # إضافة آخر chunk لو فيه كلمات متبقية
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "chunk": chunk_text,
            "pages": sorted(list(current_pages))
        })

    return chunks
