
def textFrame(texts: str, frame_symble: str = "@") -> str:
    maxText: int = 0

    finishedOutput: str

    for text in texts.splitlines():
        if len(text) > maxText:
            maxText = len(text)

    _texts = [f"{frame_symble} {i.center(maxText)} {frame_symble}" for i in texts.splitlines()]
        

    longFrames = "\n\r" + (frame_symble * (maxText + 4)) + "\n\r"
    finishedOutput = longFrames + "\n\r".join(_texts) + longFrames

    return finishedOutput