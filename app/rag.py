import os


# ============================================================
# KNOWLEDGE BASE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

KNOWLEDGE_FOLDER = os.path.join(
    BASE_DIR,
    "knowledge_base"
)


# ============================================================
# LOAD SOP DOCUMENTS
# ============================================================

def load_knowledge_base():

    documents = {}

    if not os.path.exists(KNOWLEDGE_FOLDER):
        return documents

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        if filename.lower().endswith(".txt"):

            filepath = os.path.join(
                KNOWLEDGE_FOLDER,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                documents[filename] = file.read()

    return documents


# ============================================================
# SIMPLE KEYWORD RETRIEVAL
# ============================================================

def retrieve_relevant_sop(question):

    documents = load_knowledge_base()

    if not documents:
        return "No SOP documents are available."

    question_words = set(
        question.lower()
        .replace("?", "")
        .replace(",", "")
        .split()
    )

    best_document = None
    best_score = 0

    for filename, content in documents.items():

        content_words = set(
            content.lower()
            .replace("?", "")
            .replace(",", "")
            .split()
        )

        score = len(
            question_words.intersection(
                content_words
            )
        )

        if score > best_score:

            best_score = score
            best_document = filename

    if best_document is None:

        return list(documents.values())[0]

    return documents[best_document]