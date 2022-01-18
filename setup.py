import os
os.system("pip install numpy")
os.system("pip install matplotlib")
os.system("pip install deap")
os.system("pip install pandas")
# os.system("pip install -i https://test.pypi.org/simple/ eslpy==0.0.145")
os.system("pip install --index-url https://test.pypi.org/simple/ eslpy --force")
os.system("pip install tqdm")
os.system("pip install scipy")
os.system("pip install line_profiler")
os.system("pip install cython==3.0.0a10")

os.system("pip freeze > requirements.txt")