import eel
import json
import screeninfo

@eel.expose
def get_instances():
  # try:
  #   with open('~/AppData/Roaming/.minecraft/launcher_profiles.json', 'r') as instances:
  #     instances = json.dump(instances.read())
  #     return instances["profiles"]
  # except:
  #   return {}
  return json.dumps({'One': 2})

display = screeninfo.get_monitors()[0]

eel.init('web')
eel.start('index.html', size=(display.width//2, display.height/1.5))