import edge_tts

async def ovoz(matn, filename="output.mp3", voice="uz-UZ-MadinaNeural"):
    tts = edge_tts.Communicate(matn, voice)
    await tts.save(filename)
    return filename
