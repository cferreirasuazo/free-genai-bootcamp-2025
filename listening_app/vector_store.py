import json
from openai import OpenAI
import os
from typing import Dict, List, Optional
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction

from config import OPENAI_API_KEY


MODEL_ID = "text-embedding-ada-002" 

class OpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_id=MODEL_ID):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )
        self.model_id = model_id

    def __call__(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        try:
            response = self.client.embeddings.create(model=self.model_id, input=texts)
            embeddings = [embedding.embedding for embedding in response.data]
        except Exception as e:
            print(f"Error: {e}")
        return embeddings
    

class QuestionVectorStore:
    def __init__(self,persist_directory:str = "vectorstore"):
        self.embedding_function = OpenAIEmbeddingFunction()
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.persist_directory = persist_directory
        self.collection = self.client.get_or_create_collection(
                name="questions",
                embedding_function=self.embedding_function,
                metadata={"description": "JLPT listening questions"}
        )
    def retrieve(self, question: str):
        results = self.collection.query(query_texts=[question], n_results=1)
        return results

    def add_questions(self, questions: List[Dict], video_id: str):
        """Add questions to the vector store"""            
        ids = []
        documents = []
        metadatas = []
        
        for idx, question in enumerate(questions):
            # Create a unique ID for each question
            question_id = f"{video_id}_{idx}"
            ids.append(question_id)
            
            # Store the full question structure as metadata
            metadatas.append({
                "video_id": video_id,
                "question_index": idx,
                "full_structure": json.dumps(question)
            })
            
            document = f"""
                Situation: {question['Introduction']}
                Dialogue: {question['Conversation']}
                Question: {question['Question']}
                """
        
            documents.append(document)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search_similar_questions(
        self, 
        query: str, 
        n_results: int = 5
    ) -> List[Dict]:            
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Convert results to more usable format
        questions = []
        for idx, metadata in enumerate(results['metadatas'][0]):
            question_data = json.loads(metadata['full_structure'])
            question_data['similarity_score'] = results['distances'][0][idx]
            questions.append(question_data)
            
        return questions

    def get_question_by_id(self, question_id: str) -> Optional[Dict]:
        """Retrieve a specific question by its ID"""
            
        
        result = self.collection.get(
            ids=[question_id],
            include=['metadatas']
        )
        
        if result['metadatas']:
            return json.loads(result['metadatas'][0]['full_structure'])
        return None

    def parse_questions_from_file(self, filename: str) -> List[Dict]:
        """Parse questions from a structured text file"""
        questions = []
        current_question = {}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('<question>'):
                    current_question = {}
                elif line.startswith('Introduction:'):
                    i += 1
                    if i < len(lines):
                        current_question['Introduction'] = lines[i].strip()
                elif line.startswith('Conversation:'):
                    i += 1
                    if i < len(lines):
                        current_question['Conversation'] = lines[i].strip()
                elif line.startswith('Situation:'):
                    i += 1
                    if i < len(lines):
                        current_question['Situation'] = lines[i].strip()
                elif line.startswith('Question:'):
                    i += 1
                    if i < len(lines):
                        current_question['Question'] = lines[i].strip()
                elif line.startswith('Options:'):
                    options = []
                    for _ in range(4):
                        i += 1
                        if i < len(lines):
                            option = lines[i].strip()
                            if option.startswith('1.') or option.startswith('2.') or option.startswith('3.') or option.startswith('4.'):
                                options.append(option[2:].strip())
                    current_question['Options'] = options
                elif line.startswith('</question>'):
                    if current_question:
                        questions.append(current_question)
                        current_question = {}
                i += 1
            return questions
        except Exception as e:
            print(f"Error parsing questions from {filename}: {str(e)}")
            return []

    def index_questions_file(self, filename: str):
        """Index all questions from a file into the vector store"""
        # Extract video ID from filename
        video_id = os.path.basename(filename).split('_section')[0]
        
        # Parse questions from file
        questions = self.parse_questions_from_file(filename)
        print(questions)
        
        # Add to vector store
        if questions:
            self.add_questions(questions, video_id)
            print(f"Indexed {len(questions)} questions from {filename}")


if __name__ == "__main__":
    store = QuestionVectorStore()
