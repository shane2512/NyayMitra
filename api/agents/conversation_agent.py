import google.generativeai as genai
from typing import Dict, Any, Optional, List
import json
import time
from config import Config

class ConversationAgent:
    """
    Serverless-compatible conversation agent for chat functionality.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = Config.GEMINI_MODEL
        
        # In-memory session storage (for serverless, consider using external storage)
        self.sessions = {}
    
    def process_message(self, message: str, session_id: Optional[str] = None, 
                       contract_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a single chat message.
        """
        try:
            print(f"[ConversationAgent] Processing message: {message[:100]}...")
            
            if not message or not message.strip():
                return {
                    "error": "Empty message provided",
                    "status": "error"
                }
            
            # Get or create session
            if not session_id:
                session_id = f"session_{int(time.time())}"
            
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "history": [],
                    "contract_context": None,
                    "created_at": time.time()
                }
            
            session = self.sessions[session_id]
            
            # Update contract context if provided
            if contract_context:
                session["contract_context"] = contract_context
            
            # Generate response
            response = self._generate_response(message, session)
            
            # Add to history
            session["history"].append({
                "user_message": message,
                "ai_response": response,
                "timestamp": time.time()
            })
            
            # Generate follow-up suggestions
            suggestions = self._generate_suggestions(message, response, session)
            
            return {
                "response": response,
                "suggestions": suggestions,
                "session_id": session_id,
                "status": "success"
            }
            
        except Exception as e:
            print(f"[ConversationAgent] Error processing message: {e}")
            return {
                "error": f"Failed to process message: {str(e)}",
                "status": "error"
            }
    
    def process_batch(self, questions: List[str], session_id: Optional[str] = None,
                     contract_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process multiple questions in batch.
        """
        try:
            print(f"[ConversationAgent] Processing batch of {len(questions)} questions")
            
            if not questions:
                return {
                    "error": "No questions provided",
                    "status": "error"
                }
            
            # Get or create session
            if not session_id:
                session_id = f"batch_session_{int(time.time())}"
            
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "history": [],
                    "contract_context": None,
                    "created_at": time.time()
                }
            
            session = self.sessions[session_id]
            
            # Update contract context if provided
            if contract_context:
                session["contract_context"] = contract_context
            
            # Process all questions together for efficiency
            batch_response = self._generate_batch_response(questions, session)
            
            # Add to history
            session["history"].append({
                "user_questions": questions,
                "ai_responses": batch_response,
                "timestamp": time.time(),
                "type": "batch"
            })
            
            return {
                "responses": batch_response,
                "session_id": session_id,
                "question_count": len(questions),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[ConversationAgent] Error processing batch: {e}")
            return {
                "error": f"Failed to process batch: {str(e)}",
                "status": "error"
            }
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        """
        if session_id in self.sessions:
            return self.sessions[session_id]["history"]
        return []
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear a conversation session.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def _generate_response(self, message: str, session: Dict[str, Any]) -> str:
        """
        Generate AI response to a message.
        """
        try:
            # Build context from session history
            context = self._build_context(session)
            
            # Create prompt
            prompt = f"""
            You are NyayMitra, an AI legal assistant specializing in contract analysis and legal guidance.
            
            {context}
            
            User Question: {message}
            
            Provide a helpful, accurate response. If the question is about a specific contract and you have contract context, reference it appropriately. Keep responses concise but informative.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            print(f"[ConversationAgent] Error generating response: {e}")
            return f"I encountered an error while processing your question: {str(e)}"
    
    def _generate_batch_response(self, questions: List[str], session: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate responses to multiple questions efficiently.
        """
        try:
            context = self._build_context(session)
            
            # Create batch prompt
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            
            prompt = f"""
            You are NyayMitra, an AI legal assistant. Please answer these questions concisely and accurately:
            
            {context}
            
            Questions:
            {questions_text}
            
            Provide numbered responses corresponding to each question. Keep each response focused and helpful.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if response and response.text:
                # Parse the batch response
                return self._parse_batch_response(response.text, questions)
            else:
                # Fallback: individual responses
                return [{"question": q, "answer": "Unable to generate response"} for q in questions]
                
        except Exception as e:
            print(f"[ConversationAgent] Error generating batch response: {e}")
            return [{"question": q, "answer": f"Error: {str(e)}"} for q in questions]
    
    def _parse_batch_response(self, response_text: str, questions: List[str]) -> List[Dict[str, str]]:
        """
        Parse batch response into individual Q&A pairs.
        """
        try:
            lines = response_text.split('\n')
            responses = []
            current_answer = []
            question_index = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a numbered response
                if line.startswith(f"{question_index + 1}.") and question_index < len(questions):
                    # Save previous answer if exists
                    if current_answer and question_index > 0:
                        responses.append({
                            "question": questions[question_index - 1],
                            "answer": " ".join(current_answer).strip()
                        })
                    
                    # Start new answer
                    current_answer = [line[len(f"{question_index + 1}."):].strip()]
                    question_index += 1
                else:
                    # Continue current answer
                    current_answer.append(line)
            
            # Add last answer
            if current_answer and question_index <= len(questions):
                responses.append({
                    "question": questions[question_index - 1] if question_index > 0 else questions[-1],
                    "answer": " ".join(current_answer).strip()
                })
            
            # Ensure we have responses for all questions
            while len(responses) < len(questions):
                responses.append({
                    "question": questions[len(responses)],
                    "answer": "Unable to generate response for this question."
                })
            
            return responses[:len(questions)]
            
        except Exception:
            # Fallback: return generic responses
            return [{"question": q, "answer": "Unable to parse response"} for q in questions]
    
    def _build_context(self, session: Dict[str, Any]) -> str:
        """
        Build context string from session data.
        """
        context_parts = []
        
        # Add contract context if available
        if session.get("contract_context"):
            context_parts.append(f"Contract Context: {session['contract_context'][:1000]}...")
        
        # Add recent conversation history
        history = session.get("history", [])
        if history:
            recent_history = history[-3:]  # Last 3 exchanges
            for exchange in recent_history:
                if exchange.get("type") != "batch":
                    context_parts.append(f"Previous Q: {exchange.get('user_message', '')}")
                    context_parts.append(f"Previous A: {exchange.get('ai_response', '')}")
        
        return "\n".join(context_parts) if context_parts else "No previous context available."
    
    def _generate_suggestions(self, message: str, response: str, session: Dict[str, Any]) -> List[str]:
        """
        Generate follow-up question suggestions.
        """
        try:
            # Simple rule-based suggestions for now
            suggestions = []
            
            message_lower = message.lower()
            
            if "termination" in message_lower:
                suggestions.extend([
                    "What are the notice requirements for termination?",
                    "Are there any penalties for early termination?",
                    "What happens to confidential information after termination?"
                ])
            elif "payment" in message_lower or "financial" in message_lower:
                suggestions.extend([
                    "What are the late payment penalties?",
                    "Are there any payment milestones?",
                    "What currency is used for payments?"
                ])
            elif "liability" in message_lower:
                suggestions.extend([
                    "Are there liability caps in this contract?",
                    "What types of damages are excluded?",
                    "Is there indemnification coverage?"
                ])
            else:
                # Generic suggestions
                suggestions.extend([
                    "What are the key risks in this contract?",
                    "Are there any unusual clauses I should know about?",
                    "What are my main obligations under this contract?"
                ])
            
            return suggestions[:3]  # Return max 3 suggestions
            
        except Exception:
            return ["What else would you like to know about this contract?"]
