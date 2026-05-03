"""Error logging and tracking system."""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class ErrorLogger:
    """Log and track speaking practice errors."""
    
    def __init__(self, errors_file: str = 'data/errors.json'):
        """
        Initialize error logger.
        
        Args:
            errors_file: Path to errors JSON file
        """
        self.errors_file = errors_file
        Path(errors_file).parent.mkdir(parents=True, exist_ok=True)
        self.session_errors = []
    
    def log_error(self, phrase: str, user_transcription: str, expected_phrase: str,
                  error_type: str, italian_interference: str = None, 
                  feedback: str = None):
        """
        Log a single error.
        
        Args:
            phrase: Danish phrase
            user_transcription: What user said
            expected_phrase: Correct phrase
            error_type: vocab, word_order, grammar, pronunciation, italian_interference
            italian_interference: Specific Italian transfer pattern (if applicable)
            feedback: Correction feedback
        """
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'phrase': expected_phrase,
            'user_transcription': user_transcription,
            'error_type': error_type,
            'italian_interference': italian_interference,
            'feedback': feedback
        }
        
        self.session_errors.append(error_entry)
    
    def save_session(self, session_date: str = None):
        """
        Save session errors to file.
        
        Args:
            session_date: Date for grouping errors (defaults to today)
        """
        if not session_date:
            session_date = datetime.now().strftime('%Y-%m-%d')
        
        # Load existing errors
        existing_data = self._load_errors()
        
        # Add session errors
        if session_date not in existing_data['sessions']:
            existing_data['sessions'][session_date] = []
        
        existing_data['sessions'][session_date].extend(self.session_errors)
        
        # Save
        with open(self.errors_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(self.session_errors)} errors for {session_date}")
        self.session_errors = []
    
    def get_error_summary(self, session_date: str = None) -> dict:
        """
        Get summary of errors for a session.
        
        Returns:
            {
                'total_errors': int,
                'error_types': {type: count},
                'italian_interference_patterns': {pattern: count},
                'top_mistakes': [...]
            }
        """
        if not session_date:
            session_date = datetime.now().strftime('%Y-%m-%d')
        
        errors_data = self._load_errors()
        session_errors = errors_data['sessions'].get(session_date, [])
        
        summary = {
            'total_errors': len(session_errors),
            'error_types': defaultdict(int),
            'italian_interference_patterns': defaultdict(int),
            'top_mistakes': defaultdict(int)
        }
        
        for error in session_errors:
            # Count error types
            error_type = error.get('error_type', 'unknown')
            summary['error_types'][error_type] += 1
            
            # Count Italian interference patterns
            if error.get('italian_interference'):
                pattern = error['italian_interference']
                summary['italian_interference_patterns'][pattern] += 1
            
            # Track most problematic phrases
            phrase = error.get('phrase', 'unknown')
            summary['top_mistakes'][phrase] += 1
        
        # Convert defaultdicts to regular dicts
        summary['error_types'] = dict(summary['error_types'])
        summary['italian_interference_patterns'] = dict(summary['italian_interference_patterns'])
        summary['top_mistakes'] = dict(sorted(
            summary['top_mistakes'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])  # Top 5 mistakes
        
        return summary
    
    def _load_errors(self) -> dict:
        """Load existing errors from file."""
        if Path(self.errors_file).exists():
            try:
                with open(self.errors_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        
        return {
            'metadata': {
                'created': datetime.now().isoformat(),
                'version': 1
            },
            'sessions': {}
        }


# Singleton instance
_logger = None

def get_error_logger(errors_file: str = 'data/errors.json') -> ErrorLogger:
    """Get or create an ErrorLogger instance."""
    global _logger
    if _logger is None:
        _logger = ErrorLogger(errors_file=errors_file)
    return _logger


if __name__ == '__main__':
    print("=" * 70)
    print("ERROR LOGGER TEST")
    print("=" * 70)
    
    logger = get_error_logger('data/test_errors.json')
    
    # Log test errors
    logger.log_error(
        phrase="Jeg hedder Anders",
        user_transcription="Je hedder Anders",
        expected_phrase="Jeg hedder Anders",
        error_type="pronunciation",
        italian_interference="over-pronunciation (silent j)",
        feedback="The 'j' in 'Jeg' is barely pronounced in Danish"
    )
    
    logger.log_error(
        phrase="Hun er på universitetet",
        user_transcription="Hun er pa universitetet",
        expected_phrase="Hun er på universitetet",
        error_type="vocab",
        feedback="Remember: 'på' (on/at)"
    )
    
    # Save and display summary
    logger.save_session()
    summary = logger.get_error_summary()
    
    print("\nSession Summary:")
    print(f"Total errors: {summary['total_errors']}")
    print(f"Error types: {summary['error_types']}")
    print(f"Italian interference: {summary['italian_interference_patterns']}")
    print(f"Top mistakes: {summary['top_mistakes']}")
