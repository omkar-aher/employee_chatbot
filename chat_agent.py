import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

class EmployeeChatAgent:
    def __init__(self):
        try:
            # Load employee data
            with open('data/employees.json', 'r') as f:
                self.employee_data = json.load(f)
            
            # Initialize Ollama model with llama2
            self.llm = Ollama(
                model="llama2",
                base_url="http://localhost:11434"  # Explicitly set Ollama URL
            )
            
            # Test the model
            print("Testing LLM connection...")
            test_response = self.llm("Say 'OK' if you can hear me")
            print(f"LLM Test Response: {test_response}")
            
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            raise
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory()
        
        # Create prompt template with explicit data size mention
        self.prompt_template = PromptTemplate(
            input_variables=["question", "employee_data"],
            template="""
            You are a professional HR assistant. Answer questions about employee data in a concise, business-like manner.
            
            Important: The database contains exactly 10 employee records.
            
            Employee Data:
            {employee_data}
            
            Question: {question}
            
            Guidelines:
            1. Be extremely concise - use 1-2 sentences maximum
            2. For lists (skills/certifications), use bullet points
            3. Use numbers and percentages when relevant
            4. If data isn't available, respond with "Information not available"
            5. Format names in bold
            6. Only reference the 10 employees in the database
            
            Answer:"""
        )

    def get_response(self, question):
        try:
            # Format prompt with current question and employee data
            prompt = self.prompt_template.format(
                question=question,
                employee_data=json.dumps(self.employee_data, indent=2)
            )
            
            print(f"Sending prompt to LLM: {prompt[:100]}...")  # Print first 100 chars of prompt
            
            # Get response from model
            response = self.llm(prompt)
            
            print(f"Received response: {response[:100]}...")  # Print first 100 chars of response
            
            return response
            
        except Exception as e:
            error_message = f"Error getting response: {str(e)}"
            print(error_message)
            return error_message 