# React-that-matters

This repository provides a github react repository dataset and also the script used to perform data mining. The dataset contains about 115 reacts repositories.

The repository is organized into two folders, code and data. The code folder contains the files referring to the mining process, containing the script file getDataGithub<span>.py and the input file inputFile.txt which contains the names of the authors and repositories to be mined. The data contains folder is the file resulting from mining in JSON and CSV format.

## Using the script
------

The python script uses pip3 and also some third party modules for its execution. This way it must be installed to run. Use the following command to install the dependencies used.

```python
pip3 install DateTime PyGithub moment pandas
```

The API used by the script uses user tokens to mine the repositories, so that it can be executed, create a file called tokens<span>.py in the code folder, containing a variable called 'tokens' that receives an array of user tokens. 
Below is an example of how to assemble the token file.

```python
tokens = ['9a8s4d98asd4a98sd4a', 'a3s5d16as5d1a6s5da']
```

To run the script, simply enter the code folder and run the following command:

```python
python3 getDataGitHub.py
```

