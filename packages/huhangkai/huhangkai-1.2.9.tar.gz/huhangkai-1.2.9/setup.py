import os

os.system("rmdir /s /q dist")
os.system("python commen/setup.py sdist bdist_wheel")
os.system("python -m twine upload dist/* ")
