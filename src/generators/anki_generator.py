"""Anki deck generator - converts phrases to Anki-compatible CSV format."""

import json
import csv
from pathlib import Path


def generate_anki_deck(phrases_with_audio_json: str, output_csv: str = 'data/anki_deck.csv'):
    """
    Generate Anki CSV deck from phrases with audio.
    
    Format:
    Front: English meaning
    Back: Danish phrase
    Audio: [sound:filename.mp3]
    """
    
    try:
        with open(phrases_with_audio_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        with open(phrases_with_audio_json, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    
    anki_cards = []
    
    phrases = data.get('phrases', [])
    print(f"Converting {len(phrases)} phrases to Anki format...")
    
    for phrase_data in phrases:
        phrase = phrase_data.get('phrase', '')
        english = phrase_data.get('english_meaning', phrase[:50])  # Fallback to phrase preview
        audio_file = phrase_data.get('audio_file', '')
        
        if not phrase:
            continue
        
        # Anki audio reference format
        audio_tag = f"[sound:{audio_file}]" if audio_file else ""
        
        # Create card: Front (English) | Back (Danish + Audio)
        back_content = phrase
        if audio_tag:
            back_content = f"{phrase}<br>{audio_tag}"
        
        anki_cards.append({
            'Front': english,
            'Back': back_content,
        })
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Front', 'Back']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Anki prefers no header, but some versions need it
        for row in anki_cards:
            writer.writerow(row)
    
    print(f"\nGenerated {len(anki_cards)} Anki cards")
    print(f"Saved to {output_csv}")
    
    return anki_cards


def print_sample_cards(output_csv: str, sample_count: int = 5):
    """Print sample of generated cards for verification."""
    print("\n" + "=" * 70)
    print("SAMPLE ANKI CARDS")
    print("=" * 70)
    
    with open(output_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=['Front', 'Back'])
        for i, row in enumerate(reader):
            if i >= sample_count:
                break
            print(f"\nCard {i+1}:")
            print(f"  Front (English):  {row['Front'][:60]}")
            print(f"  Back (Danish):    {row['Back'][:60]}")


if __name__ == '__main__':
    print("=" * 70)
    print("ANKI DECK GENERATOR")
    print("=" * 70)
    
    cards = generate_anki_deck('data/phrases_with_audio.json')
    print_sample_cards('data/anki_deck.csv', sample_count=5)
    
    print("\n[OK] Anki deck ready to import!")
    print("Instructions:")
    print("1. Open Anki Desktop")
    print("2. Go to File > Import")
    print("3. Select data/anki_deck.csv")
    print("4. Configure import settings (delimiter: comma, field count: 2)")
    print("5. Click Import")
