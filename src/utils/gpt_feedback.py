"""GPT-4o-mini integration for phrase comparison and Italian-specific error detection."""

import os
import json
from openai import OpenAI


class PhraseComparator:
    """Compare user transcriptions with expected Danish phrases using GPT-4o-mini."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize GPT-4o-mini comparator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = 'gpt-4o-mini'
    
    def compare_phrases(self, user_transcription: str, expected_phrase: str, 
                       italian_context: bool = True) -> dict:
        """
        Compare user's transcription with expected Danish phrase.
        
        Returns:
            {
                'is_correct': bool,
                'error_type': str or None,  # vocab, word_order, grammar, pronunciation, italian_interference
                'italian_interference': str or None,  # specific Italian interference pattern
                'feedback': str,
                'missing_words': list,
                'extra_words': list
            }
        """
        
        system_prompt = """You are a Danish A1 speaking coach for Italian speakers.
Your job is to evaluate if the user's speech transcription matches the expected Danish phrase.

Analyze the transcription and provide:
1. Whether it's correct (exact match or very close)
2. If incorrect, categorize the error:
   - vocab: wrong word used
   - word_order: incorrect verb position or subject placement (V2 rule)
   - grammar: verb tense, article (en/et), modal verb, or preposition error
   - pronunciation: spelling differs due to pronunciation (silent letters, stød, vowels)
   - italian_interference: specific Italian→Danish transfer error

3. Italian-specific interference patterns to watch for:
   - Over-pronunciation: Italian speakers pronounce all letters (Danish has silent g, d)
   - Stød errors: missing glottal stop (unique to Danish)
   - Gender confusion: wrong article (en vs et) - Italian has gendered nouns
   - Verb endings: adding -o/-a/-i (Italian pattern) instead of -r/-er
   - Soft D: pronouncing hard [d] instead of soft [ð] or barely audible
   - R pronunciation: rolled r [r] instead of guttural [ʀ]

4. Constructive feedback in 1-2 sentences
5. List of missing or extra words

Respond in JSON format only."""
        
        user_message = f"""Expected Danish phrase: "{expected_phrase}"
User's transcription: "{user_transcription}"

Is this correct? Provide detailed analysis."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                system=system_prompt
            )
            
            # Parse response
            response_text = response.content[0].text
            
            # Try to extract JSON
            try:
                # Handle potential markdown JSON blocks
                if '```json' in response_text:
                    json_str = response_text.split('```json')[1].split('```')[0].strip()
                elif '```' in response_text:
                    json_str = response_text.split('```')[1].split('```')[0].strip()
                else:
                    json_str = response_text.strip()
                
                result = json.loads(json_str)
            except (json.JSONDecodeError, IndexError):
                # Fallback if JSON parsing fails
                result = {
                    'is_correct': user_transcription.lower() == expected_phrase.lower(),
                    'error_type': None if user_transcription.lower() == expected_phrase.lower() else 'unknown',
                    'italian_interference': None,
                    'feedback': response_text,
                    'missing_words': [],
                    'extra_words': []
                }
            
            return result
        
        except Exception as e:
            print(f"Error comparing phrases: {e}")
            return {
                'is_correct': False,
                'error_type': 'error',
                'italian_interference': None,
                'feedback': f"Could not evaluate. Error: {str(e)}",
                'missing_words': [],
                'extra_words': []
            }
    
    def get_correction_suggestion(self, user_transcription: str, 
                                 expected_phrase: str) -> str:
        """Get AI-generated correction suggestion."""
        
        prompt = f"""The user said: "{user_transcription}"
The correct Danish phrase is: "{expected_phrase}"

Provide a brief, encouraging correction hint for an Italian speaker learning Danish A1:"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
        
        except Exception as e:
            return f"Try again: {expected_phrase}"


# Singleton instance
_comparator = None

def get_comparator(api_key: str = None) -> PhraseComparator:
    """Get or create a PhraseComparator instance."""
    global _comparator
    if _comparator is None:
        _comparator = PhraseComparator(api_key=api_key)
    return _comparator


if __name__ == '__main__':
    print("=" * 70)
    print("GPT-4o-mini PHRASE COMPARATOR TEST")
    print("=" * 70)
    
    try:
        comparator = get_comparator()
        
        # Test cases
        test_cases = [
            ("Jeg hedder Anders", "Jeg hedder Anders"),  # Correct
            ("Je hedder Anders", "Jeg hedder Anders"),   # Missing letter
            ("Jeg hedder Andreas", "Jeg hedder Anders"), # Wrong word
        ]
        
        for user, expected in test_cases:
            print(f"\nExpected: {expected}")
            print(f"User said: {user}")
            result = comparator.compare_phrases(user, expected)
            print(f"Correct: {result.get('is_correct')}")
            print(f"Error: {result.get('error_type')}")
            print(f"Feedback: {result.get('feedback')[:100]}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Requires OPENAI_API_KEY environment variable")
