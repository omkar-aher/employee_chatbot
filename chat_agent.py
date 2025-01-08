import json
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

class EmployeeChatAgent:
    def __init__(self):
        # Load employee data
        with open('data/employees.json', 'r') as f:
            self.employee_data = json.load(f)
        
        # Initialize Ollama model with llama2
        self.llm = Ollama(model="llama2")
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory()
        
        # Create prompt template with more specific instructions
        self.prompt_template = PromptTemplate(
            input_variables=["question", "employee_data"],
            template="""
            You are a helpful HR assistant. Use the following employee data to answer questions:
            {employee_data}
            
            Question: {question}
            
            Rules:
            1. Only use information from the provided employee data
            2. If information is not available, say so
            3. Keep answers brief and to the point
            4. For skills and certifications, list them clearly
            
            Answer:"""
        )

    def get_response(self, question):
        # Format prompt with current question and employee data
        prompt = self.prompt_template.format(
            question=question,
            employee_data=json.dumps(self.employee_data, indent=2)
        )
        
        # Get response from model
        response = self.llm(prompt)
        
        return response 