import google.generativeai as genai
from typing import Dict, Any, Optional, List
from config import Config

class TranslatorAgent:
    """
    Serverless-compatible translator agent for multi-language contract summaries.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = Config.GEMINI_MODEL
        
        # Supported languages
        self.supported_languages = {
            "en": "English",
            "hi": "Hindi",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "pt": "Portuguese",
            "ru": "Russian",
            "it": "Italian"
        }
        
        # User interest areas
        self.interest_areas = [
            "financial_obligations",
            "termination_clauses", 
            "liability_limitations",
            "intellectual_property",
            "confidentiality",
            "dispute_resolution",
            "payment_terms",
            "delivery_schedules",
            "warranty_provisions",
            "force_majeure",
            "compliance_requirements",
            "renewal_options"
        ]
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages."""
        return self.supported_languages
    
    def translate_summary(self, contract_text: str, target_language: str, 
                         user_interests: List[str] = None) -> Dict[str, Any]:
        """
        Generate a translated summary focusing on user interests.
        """
        try:
            print(f"[Translator] Translating to {target_language}")
            
            # Validate language
            if target_language not in self.supported_languages:
                return {
                    "error": f"Unsupported language: {target_language}",
                    "status": "error"
                }
            
            # Validate input
            if not contract_text or len(contract_text.strip()) < 100:
                return {
                    "error": "Insufficient contract text for translation",
                    "status": "error"
                }
            
            # Truncate if too long
            max_chars = 20000
            if len(contract_text) > max_chars:
                contract_text = contract_text[:max_chars] + "..."
            
            language_name = self.supported_languages[target_language]
            interests_text = ""
            
            if user_interests:
                valid_interests = [i for i in user_interests if i in self.interest_areas]
                if valid_interests:
                    interests_text = f"\nPay special attention to these areas: {', '.join(valid_interests)}"
            
            # Create translation prompt
            prompt = f"""
            You are a legal expert and translator. Analyze this contract and provide a comprehensive summary in {language_name}.

            Requirements:
            1. Translate and summarize the key points of this contract
            2. Focus on practical implications for the parties involved
            3. Highlight important terms, obligations, and potential risks
            4. Use clear, professional language appropriate for business contexts
            5. Maintain legal accuracy while being accessible to non-lawyers
            {interests_text}

            Structure your response with these sections:
            1. Contract Overview (type, parties, purpose)
            2. Key Terms and Obligations  
            3. Financial Aspects (if applicable)
            4. Important Dates and Deadlines
            5. Risks and Considerations
            6. Recommendations

            Contract Text:
            {contract_text}

            Provide the summary entirely in {language_name}, maintaining professional legal terminology where appropriate.
            """
            
            # Generate translated summary
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                return {
                    "error": "Failed to generate translated summary",
                    "status": "error"
                }
            
            translated_summary = response.text.strip()
            
            # Parse structured sections
            sections = self._parse_translated_sections(translated_summary)
            
            print(f"[Translator] Generated {len(translated_summary)} character summary in {language_name}")
            
            return {
                "translated_summary": translated_summary,
                "sections": sections,
                "target_language": target_language,
                "language_name": language_name,
                "user_interests": user_interests or [],
                "character_count": len(translated_summary),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[Translator] Translation error: {e}")
            return {
                "error": f"Translation failed: {str(e)}",
                "status": "error"
            }
    
    def _parse_translated_sections(self, translated_text: str) -> Dict[str, str]:
        """
        Parse the translated summary into structured sections.
        """
        try:
            sections = {}
            current_section = None
            current_content = []
            
            lines = translated_text.split('\n')
            
            # Common section headers in multiple languages
            section_indicators = [
                'overview', 'contract overview', 'aperçu', 'resumen', 'übersicht',
                'key terms', 'términos clave', 'termes clés', 'wichtige begriffe',
                'financial', 'financier', 'financiero', 'finanziell',
                'dates', 'fechas', 'dates', 'termine',
                'risks', 'riesgos', 'risques', 'risiken',
                'recommendations', 'recomendaciones', 'recommandations', 'empfehlungen'
            ]
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this line is a section header
                is_header = False
                for indicator in section_indicators:
                    if indicator.lower() in line.lower() and (
                        line.endswith(':') or 
                        len(line.split()) <= 4 or
                        line.startswith('#') or
                        line.isupper()
                    ):
                        is_header = True
                        break
                
                if is_header:
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Start new section
                    current_section = line.replace(':', '').replace('#', '').strip()
                    current_content = []
                else:
                    # Add to current section content
                    if current_section:
                        current_content.append(line)
            
            # Save last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content)
            
            return sections
            
        except Exception:
            # If parsing fails, return the full text as one section
            return {"Full Summary": translated_text}
    
    def get_translation_metrics(self) -> Dict[str, Any]:
        """
        Get translation service metrics and statistics.
        """
        return {
            "supported_languages": len(self.supported_languages),
            "available_languages": list(self.supported_languages.keys()),
            "interest_areas": self.interest_areas,
            "service_status": "active"
        }
