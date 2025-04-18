# chatbot-ingestion-service

خدمة **Ingestion** تحول ملفات PDF قانونية/طبية إلى فهرس متجهات (ChromaDB) تمهيدًا للمحادثة عبر RAG.

## ملخص المهمة

1. استلام ملف PDF من `gateway-api` أو مباشرة.
2. استخراج النص (PyPDF).
3. تقسيم المحتوى إلى **chunks** مناسبة للسياق.
4. توليد **Embeddings** باستخدام OpenAI.
5. تخزين المتجهات والبيانات الوصفية فى Chroma.

## المتطلبات

- Python ≥ 3.12
- Docker (لتشغيل Chroma محليًا)

## الإعداد السريع

```bash
# استنساخ الريبو
git clone https://github.com/ZyadahWorks/chatbot-ingestion-service.git
cd chatbot-ingestion-service

# إنشاء بيئة افتراضية
python -m venv .venv && source .venv/bin/activate

# تثبيت التبعيات
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.sample .env
# عدّل OPENAI_API_KEY، CHROMA_HOST، AZURE_STORAGE_CONNECTION_STRING ...

# تشغيل الخدمة مع إعادة تحميل تلقائى
uvicorn app.main:app --reload --port 8001
```

## متغيرات البيئة الأساسية

- `OPENAI_API_KEY`: مفتاح OpenAI.
- `CHROMA_HOST`: عنوان خادم Chroma (عادة `http://localhost:8000`).
- `AZURE_STORAGE_CONNECTION_STRING`: مسار تخزين الملفات.

## الاختبارات

```bash
pytest
```

## التشغيل عبر Docker

```bash
docker compose up --build ingestion-service
```

## رابط الوثيقة الشاملة

لمراجعة المعمارية الكاملة وتعليمات المساهمة، اطلع على الوثيقة الرئيسية فى الريبو **chatbot-gateway-api** داخل `docs/chatbot_project_plan.json`.

---

> هذا الريبو جزء من مشروع *Specialized Document Chatbot*. أى مساهمات مرحب بها!

