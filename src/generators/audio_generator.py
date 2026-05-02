"""Audio generator for Danish phrases using edge-tts."""

import asyncio
import json
from pathlib import Path
import edge_tts


async def generate_audio_for_phrase(phrase: str, chapter: int, index: int, 
                                    audio_dir: str = 'audio') -> dict:
    """
    Generate audio for a single phrase using edge-tts async API.
    
    Returns: {success: bool, phrase: str, file_path: str, error: str}
    """
    audio_dir_path = Path(audio_dir) / f'ch{chapter:02d}'
    audio_dir_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"ch{chapter:02d}_{index:03d}.mp3"
    filepath = audio_dir_path / filename
    
    try:
        # Use edge-tts async API with correct voice name
        communicate = edge_tts.Communicate(
            text=phrase,
            voice='da-DK-ChristelNeural',  # Correct Microsoft voice name
            rate='+0%',
            volume='-10%'
        )
        
        await communicate.save(str(filepath))
        
        if filepath.exists():
            return {
                'success': True,
                'phrase': phrase,
                'filename': filename,
                'file_path': str(filepath),
                'chapter': chapter,
                'index': index
            }
        else:
            return {
                'success': False,
                'phrase': phrase,
                'error': "File not created",
                'chapter': chapter,
                'index': index
            }
    
    except asyncio.TimeoutError:
        return {
            'success': False,
            'phrase': phrase,
            'error': "Timeout",
            'chapter': chapter,
            'index': index
        }
    except Exception as e:
        return {
            'success': False,
            'phrase': phrase,
            'error': str(e)[:50],
            'chapter': chapter,
            'index': index
        }


def generate_audio_batch(phrases_json: str, audio_dir: str = 'audio', 
                        test_mode: bool = False, test_count: int = 10) -> dict:
    """
    Generate audio for all or test phrases.
    """
    
    try:
        with open(phrases_json, 'r', encoding='utf-8') as f:
            phrases_data = json.load(f)
    except UnicodeDecodeError:
        with open(phrases_json, 'r', encoding='utf-8-sig') as f:
            phrases_data = json.load(f)
    
    results = {
        'generated': 0,
        'failed': 0,
        'phrases_with_audio': [],
        'errors': []
    }
    
    total_to_process = 0
    for chapter_num, phrases_list in phrases_data.get('chapters', {}).items():
        total_to_process += len(phrases_list)
    
    if test_mode:
        total_to_process = min(total_to_process, test_count)
    
    processed = 0
    
    for chapter_num, phrases_list in phrases_data.get('chapters', {}).items():
        for idx, phrase_obj in enumerate(phrases_list):
            if test_mode and processed >= test_count:
                break
            
            phrase = phrase_obj.get('phrase', '')
            # Clean phrase: remove ellipses and incomplete snippets
            phrase = phrase.replace('...', '').replace(' à', '').strip()
            
            if not phrase or len(phrase) < 3:
                continue
            
            processed += 1
            status = f"[{processed}/{total_to_process}] Ch{chapter_num}"
            phrase_display = phrase[:35].encode('ascii', 'replace').decode('ascii')
            print(f"{status}: {phrase_display}", end='', flush=True)
            
            # Run async function
            result = asyncio.run(generate_audio_for_phrase(
                phrase, int(chapter_num), idx, audio_dir
            ))
            
            if result['success']:
                print(" OK")
                results['generated'] += 1
                results['phrases_with_audio'].append({
                    'chapter': result['chapter'],
                    'index': result['index'],
                    'phrase': result['phrase'],
                    'english_meaning': phrase_obj.get('english_meaning', ''),
                    'audio_file': result['filename'],
                    'audio_path': result['file_path']
                })
            else:
                print(f" FAIL")
                results['failed'] += 1
                results['errors'].append(result)
        
        if test_mode and processed >= test_count:
            break
    
    return results


def save_phrases_with_audio(phrases_data: dict, output_path: str = 'data/phrases_with_audio.json'):
    """Save phrases with audio references to JSON."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(phrases_data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {output_path}")


if __name__ == '__main__':
    print("=" * 70)
    print("AUDIO GENERATOR TEST - First 10 Phrases")
    print("=" * 70)
    
    results = generate_audio_batch('data/phrases.json', test_mode=True, test_count=10)
    
    print("\n" + "=" * 70)
    print("Results: " + str(results['generated']) + " success, " + str(results['failed']) + " failed")
    print("=" * 70)
    
    if results['phrases_with_audio']:
        save_phrases_with_audio({'test_phrases': results['phrases_with_audio']})
        print("[OK] Generated audio for " + str(results['generated']) + " phrases")
