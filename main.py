import eel
from tkinter import Tk, filedialog
import json
import screeninfo
import os

allowed_instance_types = [
  "custom",
]

tk_root = Tk()
tk_root.withdraw()

@eel.expose
def get_instances():
  global allowed_instance_types
  try:
    with open(os.path.expanduser('~/AppData/Roaming/.minecraft/launcher_profiles.json'), 'r', encoding="UTF-8") as instances:
      instances = json.loads(instances.read())["profiles"]
      for inst_id, inst_props in instances.copy().items():
        if inst_props["type"] not in allowed_instance_types:
          instances.pop(inst_id)
      return instances
  except Exception as error:
    return error.__str__()

@eel.expose
def export_instance(instance):
  filedialog.asksaveasfile(mode='w', filetypes=[".zip"])

display = screeninfo.get_monitors()[0]

app_width = display.width//2
app_height = display.height/1.5
off_x = (display.width - app_width) // 2
off_y = (display.height - app_height) // 2

eel.init('web')
eel.start('index.html', size=(app_width, app_height), position=(off_x, off_y))