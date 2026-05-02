"""Organize audio files into chapter folders."""

import os
import shutil
from pathlib import Path
import json

# Create chapter folders and move audio files
audio_dir = Path('audio')

for ch in range(1, 14):
    ch_folder = audio_dir / f'ch{ch:02d}'
    ch_folder.mkdir(parents=True, exist_ok=True)
    
    # Find and move files for this chapter
    pattern = f'ch{ch:02d}_*.mp3'
    moved = 0
    for file in audio_dir.glob(pattern):
        dest = ch_folder / file.name
        file.rename(dest)
        moved += 1
    
    print(f"ch{ch:02d}: {moved} files moved")

# Update paths in phrases_with_audio.json
with open('data/phrases_with_audio.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for phrase in data.get('phrases', []):
    if 'audio_file' in phrase and 'audio_path' in phrase:
        old_filename = phrase['audio_file']
        # Extract chapter from filename
        ch_num = old_filename.split('_')[0]  # "ch01"
        # Update path
        phrase['audio_file'] = f"{ch_num}/{old_filename}"
        phrase['audio_path'] = str(Path('audio') / ch_num / old_filename)

with open('data/phrases_with_audio.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nUpdated phrases_with_audio.json with new audio paths")
