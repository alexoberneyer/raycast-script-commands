#!/Users/alex/Code/raycast-script-commands/.venv/bin/python
# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Speak Clipboard (Sesame TTS)
# @raycast.mode compact

# Optional parameters
# @raycast.icon 🗣️
# @raycast.description Convert clipboard text to speech using Sesame TTS model
# @raycast.packageName TTS
# @raycast.needsConfirmation false

import subprocess
import sys
import tempfile


def get_clipboard_text() -> str:
    """Get text from clipboard using pbpaste."""
    try:
        result = subprocess.run(["pbpaste"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get clipboard content: {e}")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error getting clipboard: {e}")
        return ""


def speak(text: str):
    """Convert text to speech using macOS built-in TTS as fallback."""
    try:
        import torch
        from transformers import AutoProcessor, AutoModelForTextToWaveform
        import soundfile as sf
        import numpy as np
        import os
    except ImportError as e:
        print(f"⚠️ ML dependencies not available: {e}")
        print("🔄 Using macOS built-in TTS instead...")
        use_builtin_tts(text)
        return

    print("🔄 Loading Sesame TTS model...")
    
    # Check for HF token
    hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    
    try:
        model_id = "sesame/csm-1b"
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        # Try to load with authentication if token is available
        auth_kwargs = {"token": hf_token} if hf_token else {}
        
        processor = AutoProcessor.from_pretrained(model_id, **auth_kwargs)
        model = AutoModelForTextToWaveform.from_pretrained(model_id, **auth_kwargs)
        model = model.to(device)
        
        print("✅ Sesame TTS model loaded successfully!")
        
        print("🎙️ Generating speech...")
        inputs = processor(text=text, return_tensors="pt")
        for k, v in inputs.items():
            if hasattr(v, "to"):
                inputs[k] = v.to(device)

        audio = model.generate(**inputs)
        waveform = audio["waveform"][0].to("cpu").numpy()
        sr = int(audio["sampling_rate"])

        if waveform.ndim > 1:
            waveform = np.squeeze(waveform)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, waveform, sr)
            path = tmp.name

        print("🔊 Playing audio...")
        try:
            subprocess.run(["afplay", path], check=True, capture_output=True)
            print("✅ Audio playback completed!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Audio playback failed: {e}")
        finally:
            try:
                os.remove(path)
            except Exception as e:
                print(f"⚠️ Could not clean up temporary file: {e}")
                
    except Exception as e:
        if "gated repo" in str(e).lower() or "restricted" in str(e).lower():
            print("🔒 Sesame TTS requires authentication.")
            print("💡 Get access at: https://huggingface.co/sesame/csm-1b")
            print("💡 Then set HUGGINGFACE_HUB_TOKEN environment variable")
            print("🔄 Using macOS built-in TTS instead...")
            use_builtin_tts(text)
        else:
            print(f"⚠️ Sesame TTS failed: {e}")
            print("🔄 Using macOS built-in TTS instead...")
            use_builtin_tts(text)


def use_builtin_tts(text: str):
    """Fallback to macOS built-in text-to-speech."""
    try:
        print("🗣️ Using macOS built-in TTS...")
        # Use macOS say command for TTS
        subprocess.run(["say", text], check=True, capture_output=True)
        print("✅ Speech completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Built-in TTS failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ TTS error: {e}")
        sys.exit(1)


def main():
    """Main function to get clipboard text and speak it."""
    text = get_clipboard_text()

    if not text:
        print("📋 Clipboard is empty or contains no text.")
        sys.exit(1)

    print(
        f"📝 Text to speak ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}"
    )
    speak(text)


if __name__ == "__main__":
    main()
