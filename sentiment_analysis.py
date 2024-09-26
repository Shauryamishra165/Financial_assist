from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
import os
import google.generativeai as genai

# load_dotenv()
os.environ['GOOGLE_API_KEY'] = 'AIzaSyD6qA1IwhYgsZtOUs8narrbT6OErB6E0Ks'
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_conversational_chain():
    prompt_template = """
    Give the market sentiment in the context using the latest news given in the context. ALso give a proper reasoning in the answer.
    Take many news articles in consideration and then predict the market sentiment , Also provide links to news articles.
    Context:\n{context}?\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    # model = GPT4All(model_name="gpt4all-lora-quantized")
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain , model

class Document:
    def __init__(self, content, metadata=None):
        self.page_content = content  # The main content
        self.metadata = metadata or {}  # Metadata as a dictionary

# Preprocessing the news articles into Document objects with metadata
def preprocess_news_as_documents(news):
    documents = []
    for article in news:
        title = article.get('title', 'No title available')
        content = article.get('title', '')  # Assuming 'content' holds the article body
        link = article.get('link', '#')
        
        # Prepare metadata
        metadata = {
            "title": title,
            "link": link
        }
        
        # Create a Document object for each article
        doc = Document(content=content, metadata=metadata)
        documents.append(doc)
    
    return documents

def get_sentiment_analysis(query , news):
    chain , model = get_conversational_chain()
    docs = preprocess_news_as_documents(news)
    response = chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    return response , docs