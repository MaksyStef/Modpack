import eel
import json
import screeninfo
import os

@eel.expose
def get_instances():
  try:
    with open(os.path.expanduser('~/AppData/Roaming/.minecraft/launcher_profiles.json'), 'r', encoding="UTF-8") as instances:
      instances = json.loads(instances.read())["profiles"]
      for instance_id, instance_props in instances.items():
        if instance_props.type != "custom":
          instances.pop(instance_id)
      print(instances)
      return instances
  except Exception as error:
    return error.__str__()

display = screeninfo.get_monitors()[0]

app_width = display.width//2
app_height = display.height/1.5
off_x = (display.width - app_width) // 2
off_y = (display.height - app_height) // 2

eel.init('web')
eel.start('index.html', size=(app_width, app_height), position=(off_x, off_y))