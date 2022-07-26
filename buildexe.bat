DEL /q .\build\*
DEL /q .\dist\*
RD /S /Q .\build
RD /S /Q .\dist
pip install pyinstaller
pyinstaller -w ./ImageViewer.py --noconfirm
compil32 /cc ./ImageViewer.iss