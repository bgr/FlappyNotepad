echo off
python setup.py py2exe
rm -rf FlappyNotepad FlappyNotepad.zip
mv dist FlappyNotepad
zip -r FlappyNotepad.zip FlappyNotepad
echo "Press enter to move to dropbox"
pause
cp FlappyNotepad.zip E:\Dropbox\Public