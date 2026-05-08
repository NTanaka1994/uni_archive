from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

f = open("API_key.txt", "r", encoding="utf-8")
api_key = f.read().strip()
f.close()


def load_text_documents():
    files = [
        "嘱託職員.txt",
        "就業規則.txt"
    ]

    documents = []

    for filename in files:
        loader = TextLoader(filename, encoding="utf-8")
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = filename

        documents.extend(docs)
    documents.extend(docs)
    return documents
    
def build_vector_store(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    split_docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

    vector_store = FAISS.from_documents(split_docs, embeddings)

    return vector_store


def format_docs(docs):
    text = ""
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page_content = doc.page_content
        text += "【参照元: " + source + "】\n"
        text += page_content + "\n\n"
    return text


def create_rag_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "あなたは大学の就業規則を読む補助者です。"
            "与えられた就業規則の抜粋だけを根拠に回答してください。"
            "抜粋に根拠がない場合は「資料内からは分かりません」と答えてください。"
            "断定しすぎず、日本語で分かりやすく説明してください。"
        ),
        (
            "human",
            "質問:\n{question}\n\n"
            "就業規則の抜粋:\n{context}"
        )
    ])

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=api_key
    )

    def retrieve_context(question):
        docs = retriever.invoke(question)
        return format_docs(docs)

    chain = (
        {
            "context": retrieve_context,
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

print("就業規則RAGを準備しています。")

documents = load_text_documents()
vector_store = build_vector_store(documents)
rag_chain = create_rag_chain(vector_store)

print("準備完了。質問を入力してください。終了する場合は exit と入力してください。")

while True:
    question = input("\n質問> ")

    if question == "exit":
        break

    answer = rag_chain.invoke(question)

    print("\n--- 回答 ---")
    print(answer)
