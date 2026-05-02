Document Links: [install](#install) / [usage](#usage) / [demo](#demo)
<img width="1648" height="349" alt="a" src="https://github.com/user-attachments/assets/7f49a123-4529-4f44-947b-519a546626eb" />

# Binny and Bloom
## A live well app focused on minimizing waste while maximizing utility.<center> <br />
Senior Project - Spring 2026.

<br /><br />




## <a name="install"></a>Installation:<br />

```
SeniorProject/
|  |
|  ├- /docs/
|  └- /src/
|     |  |
|     |  ├- /instance/
|     |  |      ├- 01-build-db-new.py
|     |  |      ├- 02-insert-db-new.py
|     |  |      ├- 03-test-db-new.py
|     |  |      └- inventory.db
|     |  └- /static/
|     |      ├- /css/
|     |      |   ├- homestyle.css
|     |      |   └- mainstyle.css
|     |      ├- /js/
|     |      |   └- MainPageJS.js
|     |      ├- /Pictures/
|     |      |   ├- Binny-original.png
|     |      |   ├- Binny.png
|     |      |   ├- chef.png
|     |      |   ├- favicon.png
|     |      |   └- trail.png
|     |      └- /profile_pics/
|     |          └- demo.png
|     ├- /templates/
|     |    ├- 0-AddItemPageSetup.html
|     |    ├- 0-AIPageSetup.html
|     |    ├- 0-HomePageSetup.html
|     |    ├- 0-InventoryPageSetup.html
|     |    ├- 0-MainPageSetup.html
|     |    ├- 0-SamplePageSetup.html
|     |    ├- AddItemPage.html
|     |    ├- dashboard.html
|     |    ├- HomePage.html
|     |    ├- InventoryPage.html
|     |    ├- LoginPage.html
|     |    ├- Menu.html
|     |    ├- RegisterPage.html
|     |    ├- SamplePage.html
|     |    ├- ScoreboardPage.html
|     |    ├- UserProfile.html
|     |    └- ViewMeal.html
|     ├- .env
|     ├- app.py
|     ├- database.py
|     ├- expiry.py
|     ├- generator.py
|     ├- cli.py
|     ├- models.py
|     ├- openrouterllm.py
|     ├- requirements.txt
|     ├- unit_conversion.py
|     └- validatory.py
├- .gitignore
├- README.md
└- requirements.txt
 ```











For Windows Users:
- ``` apt install python3.13-venv ```      # install the virtual environment module for Python 3.13
- ``` apt install git ```                  # install Git
- ```python3 -m venv venv```               # create virtual environment
- ```git clone https://github.com/nere-var/CSCI4391-project```
- ```cd CSCI-4391-Senior-Project```
- ```pip install -r requirements.txt```    # installs all packages listed

For Mac/Linux Users:
- ``` apt install python3.13-venv ``` # install the virtual environment module for Python 3.13
- ``` apt install git ```             # install Git
- ```python3 -m venv venv```          # create virtual environment
- ```source venv/bin/activate```      # activate it
- ```git clone https://github.com/nere-var/CSCI4391-project```
- ```cd CSCI-4391-Senior-Project```
- ```pip install -r requirements.txt```   # installs all packages listed

Then:
# Create your environment file
- cp src/.env.example src/.env   # macOS/Linux
- copy src/.env.example src/.env # Windows

# Then edit .env and paste your OpenRouter API key
- Go to https://openrouter.ai/ to obtain an API key
- append the .env file with your key

<br><br><br>
## <a name="usage"></a>Usage:<br />
<center> 





 
[Terminal Version](#terminal) | [GUI Version](#gui) 

</center><br><br>

 
### <a name="terminal"></a>Terminal version:<br>

- ```python3 src/cli.py```  # In the Projects root Folder<br>

- This will start an instance in your terminal:<br>


- Select user to login: demo:demo<br>
 <img width="173" height="191" alt="image" src="https://github.com/user-attachments/assets/82f79ed0-3c8d-4931-b0d6-00d93a625637" />

- To view user's inventory(Option 1):<br>
  <img width="437" height="370" alt="image" src="https://github.com/user-attachments/assets/935a21b3-d85b-4553-a6be-397cf7a5889a" />

- View inventory sorted by Dates(Option 2):<br>
  <img width="439" height="303" alt="image" src="https://github.com/user-attachments/assets/8f51a7d6-cfdc-4cda-8c49-e53d65f7eb50" />

- Create recipe(Option 3):<br>
  <img width="517" height="197" alt="image" src="https://github.com/user-attachments/assets/614591c2-712f-40ec-bed8-f2998411b49b" />

- Logout(Option 4):<br>
  <img width="221" height="368" alt="image" src="https://github.com/user-attachments/assets/a0d7e228-ea4c-4167-8c36-f9258847f594" />

- Exit app(Option 5):<br>
  <img width="218" height="159" alt="image" src="https://github.com/user-attachments/assets/9f447935-964f-48ca-834c-0c429cbaf74e" />

<br>


<br>

### <a name="gui"></a> GUI version:<br>

- ```python3 src/app.py```  # In the Projects root Folder<br>
- This will start an instance of Flask which will provide GUI accessed by navigating to the address provided in a browser window:<br>
  <img width="953" height="164" alt="image" src="https://github.com/user-attachments/assets/a4c16929-a3cb-4841-bf0b-2ff8910a1e85" />

<br />

We have provided a database with a various items with username:password  demo:demo<br>
| <img width="157" height="100" alt="Screenshot 2026-02-27 165230" src="https://github.com/user-attachments/assets/3265c059-7ea6-4848-af09-8919711ae2bf" /> | <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/c7c7ba5b-236a-4f09-8675-f7420bdcc37a" /> | <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/d3811057-d9fb-4e2a-b824-afef64dd64c3" /> | <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/6d9c31ae-b3e0-43a1-99a6-e9d6d3cb0f76" />|
|---|---|---|---|

The inventory page shows all of the items the current user has available in their inventory and just below that is field to interact with the AI:<br>
| <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/7b15ce38-a1af-48b6-b204-36c1303daf3f" /> | <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/d0e147de-0825-4419-a9a2-b7f1c409faf5" /> | <img width="157" height="100" alt="image" src="https://github.com/user-attachments/assets/95a6cee3-e664-44c3-9c43-6fdef8b9bbe1" />|
|---|---|---|




If Binny finds a recipe that can be made with only item available in the user's inventory:<br>
<img width="157" height="100" alt="Screenshot 2026-02-27 170105" src="https://github.com/user-attachments/assets/109e1e78-2f98-4231-9cf1-b0aecb2e4b2c" /><br>
If the ingredients are not available:<br>
<img width="157" height="100" alt="Screenshot 2026-02-27 165840" src="https://github.com/user-attachments/assets/83fda730-90af-400d-b462-a667191799bd" />








<br /><br /><br />
<br /><br /><br />

## <a name="demo"></a>Demos:<br />
| Milestone 1 | Milestone 2 | Dry Run 1 | Dry Run 2 | Dry Run 2 - Video Capture |
|---|---|---|---|---|
| <a href="https://www.youtube.com/watch?v=rEP0uPVVnNU"><img src="https://github.com/user-attachments/assets/e90d090b-1b35-484e-860d-6425029413d6" width="300"></a> | <a href="https://www.youtube.com/watch?v=LsMbCGHMmF0"><img src="https://github.com/user-attachments/assets/2e07bb9c-a9e5-4301-b237-0ad46380d198" width="300"></a> | <a href="https://www.youtube.com/watch?v=2m3urxbWoBw"><img src="https://github.com/user-attachments/assets/0d49fcc2-ff06-4719-a18a-fa956b13b94f" width="300"></a>| <a href="https://www.youtube.com/watch?v=2hLODnwbJ2s"><img src="https://github.com/user-attachments/assets/dcff76a6-2d3f-4986-8374-311743b385e5" width="300"></a> | <a href="https://www.youtube.com/watch?v=Vb87FnBxCL4"><img src="https://github.com/user-attachments/assets/3e76e396-21ca-447d-ad09-e79979028ed1" width="300"></a> |















<br /><br /><br />


## <a name="demo"></a>Other Videos:<br />
| Installation Video | Demonstation Backup | Final Presentation |
|---|---|---|
| <a href="https://www.youtube.com/watch?v=6lxgTZllMpQ"><img src="https://github.com/user-attachments/assets/ce0582c6-419b-4812-88e7-2e99936952f5" width="300"></a> |  <a href="https://www.youtube.com/watch?v=ez2_7s_7lyI"><img src="https://github.com/user-attachments/assets/8f091700-ef8b-4902-b49a-836695e1f080" width="300"></a> |  <a href="https://www.youtube.com/watch?v=XjjlXml9yB8"> <img src="https://github.com/user-attachments/assets/5d730b53-17a2-40c0-8b21-aa9e890295d0" width="300"></a>  |



<br /><br /><br /><br />

## The Krusty Compost Crew: <br />
| [<img src="https://avatars.githubusercontent.com/u/230457100?v=4" width="50">](https://github.com/picklefarm1234) | [<img src="https://avatars.githubusercontent.com/u/118304167?v=4" width="50">](https://github.com/AlexandriaTH) | [<img src="https://avatars.githubusercontent.com/u/77978673?s=64&v=4" width="50">](https://github.com/OrangeXR) | [<img src="https://avatars.githubusercontent.com/u/179060597?v=4" width="50">](https://github.com/jayv2025) | [<img src="https://avatars.githubusercontent.com/u/58350011?v=4" width="50">](https://github.com/nere-var) |
|---|---|---|---|---|
















# For hosting on render

## app.py<br>
<br> 
app = Flask(__name__)<br>
app.secret_key = "super-secret-key"<br>
<br>
BASE_DIR = app.root_path<br>
#load_dotenv()  # Load .env file<br>
<br>
<br>
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") #============== for render <br>
<br>

#=============<br>
#Connect to db<br>
#=============<br>
def get_db():<br>
    conn = sqlite3.connect("instance/inventory.db")<br>
    conn.row_factory = sqlite3.Row<br>
    return conn<br>
<br>
<br>
#==========================================<br>
#Inventory Page (uses logged-in player)<br>
#==========================================<br>
@app.route("/inventory",methods=["GET", "POST"])<br>
@login_required<br>
def inventory_page():<br>
    from src.openrouterllm import Ai_Chat   #importing everything from openrouterllm  #<=========== this one line<br>
    player_id = session["player_id"]<br>
<br>
<br>

## OpenRouterLLM.py<br>
<br>
...
# db path + other variables<br>
self.DB_PATH = 'instance/inventory.db' # <------------------- remove src/<br>
self.PLAYER_ID = 1 # for testing<br>
self.MAX_HISTORY = 10 # max number of messages to keep in conversation history to prevent growth<br>
...
<br>
<br>

## database.py

import os<br>
import sqlite3<br>
<br>
BASE_DIR = os.path.dirname(os.path.abspath(__file__))<br>
DB_PATH = os.path.join(BASE_DIR, "instance", "inventory.db")<br>
<br>
def get_db():<br>
    conn = sqlite3.connect(DB_PATH)<br>
    conn.row_factory = sqlite3.Row <br>
    return conn<br>
