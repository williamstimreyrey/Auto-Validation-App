# Auto-Validation-App
App for auto validating inventory for KOs

## Powershell Scripts:
### To download necessary packages for the app to function properly run this in the same directory as requirements.txt:
pip install -r requirements.txt

#### To bundle and create .exe run this in the same directory as app.py and utils.py:
pyinstaller --onefile --noconsole --hidden-import utils.py main.py