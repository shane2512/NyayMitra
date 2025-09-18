import re
import time
from typing import Dict, List, Optional

class ConversationModeratorAgent:
    """
    Validates and filters user messages before sending to Gemini.
    Can block, flag, or sanitize disallowed queries (e.g., unsafe, offensive, or restricted topics).
    """
    def __init__(self, block_patterns=None, allow_patterns=None):
        # Patterns for queries to block (regex)
        self.block_patterns = block_patterns or [
            r"\b(?:violence|hate|abuse|illegal|drugs|terror|exploit|self-harm|suicide|kill|murder|bomb)\b",
            r"\b(?:credit card|password|ssn|social security|bank account)\b",
            r"\b(?:sexual|porn|nude|explicit)\b",
            r"\b(?:hack|exploit|malware|phishing|ransomware)\b"
        ]
        self.allow_patterns = allow_patterns or []

    def is_allowed(self, message: str) -> bool:
        """Returns True if the message is allowed, False if blocked."""
        for pattern in self.block_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return False
        if self.allow_patterns:
            for pattern in self.allow_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return True
            return False
        return True

    def filter_message(self, message: str) -> dict:
        """Returns dict with status and reason if blocked, or allowed message."""
        if not self.is_allowed(message):
            return {"allowed": False, "reason": "Query blocked by moderator: disallowed content detected."}
        return {"allowed": True, "message": message}

class ConversationModerator:
    """
    Moderator for managing conversation flow between user and AI.
    Handles context management, session state, and conversation orchestration.
    """
    
    def __init__(self, api_key: str = None, model_name: str = None):
        # Import here to avoid circular import
        from .conversation_agent import ConversationAgent
        self.conversation_agent = ConversationAgent(api_key, model_name)
        self.sessions = {}  # Store multiple conversation sessions
        self.current_session_id = None
        self.contract_context = None  # Store contract analysis context if available
        
    def create_session(self, session_id: str = None) -> str:
        """Create a new conversation session"""
        if not session_id:
            session_id = f"session_{int(time.time())}"
        
        self.sessions[session_id] = {
            "created_at": time.time(),
            "messages": [],
            "context": {}
        }
        self.current_session_id = session_id
        print(f"[ConversationModerator] Created session: {session_id}")
        return session_id
    
    def set_contract_context(self, contract_analysis: Dict):
        """Set contract analysis context for informed responses"""
        self.contract_context = contract_analysis
        if self.current_session_id and self.current_session_id in self.sessions:
            self.sessions[self.current_session_id]["context"]["contract"] = contract_analysis
        print("[ConversationModerator] Contract context updated")
    
    def process_message(self, user_message: str, session_id: str = None) -> Dict:
        """
        Process a user message and return AI response with metadata.
        """
        try:
            # Use provided session or current session
            if session_id:
                self.current_session_id = session_id
            elif not self.current_session_id:
                self.current_session_id = self.create_session()
            
            session = self.sessions.get(self.current_session_id, {})
            
            print(f"[ConversationModerator] Processing message in session: {self.current_session_id}")
            
            # Build context for the conversation agent
            context = {}
            if self.contract_context:
                context["contract"] = self.contract_context
            if session.get("context"):
                context.update(session["context"])
            
            # Generate response
            response = self.conversation_agent.generate_response(user_message, context)
            
            # Get follow-up suggestions
            suggestions = self.conversation_agent.suggest_followup_questions(user_message)
            
            # Store in session
            if self.current_session_id in self.sessions:
                self.sessions[self.current_session_id]["messages"].append({
                    "user": user_message,
                    "assistant": response,
                    "timestamp": time.time(),
                    "suggestions": suggestions
                })
            
            return {
                "response": response,
                "session_id": self.current_session_id,
                "suggestions": suggestions,
                "status": "success",
                "has_contract_context": bool(self.contract_context)
            }
            
        except Exception as e:
            print(f"[ConversationModerator] Error processing message: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your message. Please try again.",
                "session_id": self.current_session_id,
                "suggestions": [],
                "status": "error",
                "error": str(e)
            }
    
    def process_batch(self, questions: List[str], session_id: str = None) -> Dict:
        """Process multiple questions in batch mode"""
        try:
            if session_id:
                self.current_session_id = session_id
            elif not self.current_session_id:
                self.current_session_id = self.create_session()
            
            print(f"[ConversationModerator] Processing batch of {len(questions)} questions")
            
            # Process batch through conversation agent
            batch_text = "\n".join([f"Q{i+1}: {q}" for i, q in enumerate(questions)])
            response = self.conversation_agent.generate_response(batch_text)
            
            # Store in session
            if self.current_session_id in self.sessions:
                self.sessions[self.current_session_id]["messages"].append({
                    "user": f"Batch questions: {batch_text}",
                    "assistant": response,
                    "timestamp": time.time(),
                    "batch_size": len(questions)
                })
            
            return {
                "response": response,
                "session_id": self.current_session_id,
                "questions_processed": len(questions),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[ConversationModerator] Error processing batch: {e}")
            return {
                "response": "Error processing batch questions.",
                "session_id": self.current_session_id,
                "status": "error",
                "error": str(e)
            }
    
    def get_session_history(self, session_id: str = None) -> List[Dict]:
        """Get conversation history for a session"""
        sid = session_id or self.current_session_id
        if sid and sid in self.sessions:
            return self.sessions[sid]["messages"]
        return []
    
    def get_conversation_summary(self, session_id: str = None) -> str:
        """Get summary of conversation"""
        sid = session_id or self.current_session_id
        if sid:
            # Set the conversation history in agent
            history = self.get_session_history(sid)
            if history:
                return f"Conversation with {len(history)} exchanges in session {sid}"
        return "No conversation to summarize."
    
    def clear_session(self, session_id: str = None):
        """Clear a conversation session"""
        sid = session_id or self.current_session_id
        if sid and sid in self.sessions:
            del self.sessions[sid]
            if sid == self.current_session_id:
                self.current_session_id = None
            print(f"[ConversationModerator] Cleared session: {sid}")
    
    def _summarize_contract_context(self) -> str:
        """Summarize contract context for conversation"""
        if not self.contract_context:
            return ""
        
        summary = "Contract Analysis Context:\n"
        
        if "risk_report" in self.contract_context:
            risk_report = self.contract_context["risk_report"]
            high_risks = sum(1 for r in risk_report.values() 
                           if r.get("analysis", {}).get("risk_level") == "High")
            summary += f"- {len(risk_report)} clauses analyzed\n"
            summary += f"- {high_risks} high-risk clauses identified\n"
        
        if "summary" in self.contract_context:
            summary += f"- Summary: {self.contract_context['summary'][:200]}...\n"
        
        if "simulation" in self.contract_context:
            sim = self.contract_context["simulation"]
            summary += f"- Risk simulation: {sim.get('safety_index', 'N/A')} safety index\n"
        
        return summary
