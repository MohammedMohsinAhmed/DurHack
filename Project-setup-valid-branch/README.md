# Project-setup
Steps to initialise projects and repos correctly

#**Virtual env**
python3 -m venv venv  # Creates a new virtual environment in a directory called "venv"

#(Mac)
source venv/bin/activate

#(Windows)
.\venv\Scripts\activate

#Create requirements.txt
pip freeze > requirements.txt

#Load requirements.txt
pip install -r requirements.txt

#####################
#Toml file to define constants
import tomli
with open("settings.toml", mode="rb") as fp:
    config = tomli.load(fp)

print(config['model']['country'])
#Dependancy management


#Path probelsm when importing
use: python -m my_project.folder.module

#Create .gitignore
echo '# Compiled source #
###################
*.com
*.class
*.dll
...
#Virtual environments
######################
venv/
env/
env.bak/



#######################
node_modules/
jspm_packages/
bower_components/' >> .gitignore
