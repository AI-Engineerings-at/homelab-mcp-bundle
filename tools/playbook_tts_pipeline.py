#!/usr/bin/env python3
"""
Playbook Audio-Pipeline: PDF/Text → Piper TTS → MP3
Nutzt Voice Gateway auf http://10.40.10.80:8085/tts
"""
import json, base64, struct, time, os, sys
import urllib.request
import subprocess

TTS_URL = "http://10.40.10.80:8085/tts"

def text_to_wav(text: str, output_path: str) -> dict:
    """Konvertiert Text zu WAV via Piper TTS"""
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        TTS_URL, data=payload,
        headers={"Content-Type": "application/json"}
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    elapsed = time.time() - start
    
    audio_bytes = base64.b64decode(data["audio"])
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    # Berechne Dauer aus WAV-Header
    sample_rate = struct.unpack("<I", audio_bytes[24:28])[0]
    channels = struct.unpack("<H", audio_bytes[22:24])[0]
    pcm_bytes = len(audio_bytes) - 44
    duration = (pcm_bytes // 2) / (sample_rate * channels)
    
    return {"duration": duration, "size_kb": len(audio_bytes)//1024, "gen_time": elapsed}

def wav_to_mp3(wav_path: str, mp3_path: str, bitrate: str = "64k") -> bool:
    """Konvertiert WAV zu MP3 via ffmpeg"""
    result = subprocess.run(
        ["ffmpeg", "-i", wav_path, "-codec:a", "libmp3lame",
         "-b:a", bitrate, "-y", mp3_path],
        capture_output=True
    )
    return result.returncode == 0

def process_playbook(chapters: list, output_dir: str):
    """Verarbeitet alle Kapitel eines Playbooks"""
    os.makedirs(output_dir, exist_ok=True)
    total_duration = 0
    
    for i, (title, text) in enumerate(chapters, 1):
        print(f"\n[{i}/{len(chapters)}] {title}")
        wav_path = os.path.join(output_dir, f"kapitel_{i:02d}.wav")
        mp3_path = os.path.join(output_dir, f"kapitel_{i:02d}.mp3")
        
        try:
            stats = text_to_wav(text, wav_path)
            wav_to_mp3(wav_path, mp3_path)
            os.remove(wav_path)  # WAV loeschen nach MP3-Konvertierung
            
            total_duration += stats["duration"]
            print(f"  Audio: {stats['duration']:.1f}s | Gen: {stats['gen_time']:.1f}s | MP3: {os.path.getsize(mp3_path)//1024}KB")
        except Exception as e:
            print(f"  FEHLER: {e}")
    
    print(f"\n=== Fertig: {total_duration/60:.1f} Minuten Gesamtdauer ===")

# Demo mit 1 Kapitel
if __name__ == "__main__":
    demo_chapters = [
        ("Kapitel 1: Grundlagen der digitalen Kundengewinnung",
         """Kapitel 1: Grundlagen der digitalen Kundengewinnung.
         In diesem Kapitel lernen Sie, wie Sie Ihre ersten Kunden online gewinnen.
         Der erste Schritt ist immer die Zielgruppenanalyse. Wer sind Ihre idealen Kunden?
         Was sind ihre Probleme und Beduerfnisse? Wenn Sie das verstehen, koennen Sie gezielt auf sie zugehen.
         Ein wichtiges Werkzeug ist Ihre Landing Page. Sie muss klar kommunizieren:
         Was bieten Sie an? Welches Problem loesen Sie? Und warum sollte der Besucher jetzt handeln?
         Klare Botschaften, ein starkes Angebot und ein einfaches Kontaktformular sind das Fundament.""")
    ]
    process_playbook(demo_chapters, "/tmp/playbook_audio")
    print(f"MP3 Datei: /tmp/playbook_audio/kapitel_01.mp3")
