import eel
from tkinter import Tk, filedialog
import json
import screeninfo
import zipfile
import os
import pathlib

allowed_instance_types = [
  "custom",
]

@eel.expose
def get_instances():
  global allowed_instance_types
  try:
    with open(os.path.expanduser('~/AppData/Roaming/.minecraft/launcher_profiles.json'), 'r', encoding="UTF-8") as instances:
      instances = json.loads(instances.read())["profiles"]
      for inst_id, inst_props in instances.copy().items():
        if inst_props["type"] not in allowed_instance_types:
          instances.pop(inst_id)
      print(instances)
      return instances
  except Exception as error:
    return error.__str__()

@eel.expose
def export_instance(instance):
  root = Tk()
  root.withdraw()
  root.attributes('-topmost', True)  # Make sure the dialog is on top
  filetypes = [("Minecraft Modpack", "*.zip")]
  filename = instance['name']
  game_dir = pathlib.Path(instance['gameDir'])
  file = filedialog.asksaveasfilename(
    initialfile=filename,
    filetypes=filetypes, 
    defaultextension=filetypes,
    parent=root
  )
  root.destroy()

  included_folders = [
    "config",
    "mods",
    "resourcepacks",
    "shaderpacks",
  ]
  included_files = [
    'options.txt',
  ]

  def add_directory(directory_path, zip_path):
    print('try to write to: ', zip_path, directory_path)
    with zipfile.ZipFile(zip_path, 'a') as zipf:
      for root, dirs, files in os.walk(directory_path):
        for file in files:
          zipf.write(os.path.join(root, file), 
          os.path.relpath(os.path.join(root, file), 
          os.path.join(directory_path, '..')))

  try:
    # Add folders and their contents
     for current_item in game_dir.iterdir():
        print('current item: ', current_item)
        if current_item.name not in included_folders and current_item.name not in included_files:
          print('skip item...')
          continue
        if current_item.is_dir():
          add_directory(current_item, file)
        if current_item.is_file():
          with zipfile.ZipFile(file, 'a') as zipf:
            zipf.write(current_item, current_item.relative_to(game_dir))
        

  except Exception as e:
    raise e

  return file


if __name__ == "__main__":
  display = screeninfo.get_monitors()[0]

  app_width = display.width//2
  app_height = display.height/1.5
  off_x = (display.width - app_width) // 2
  off_y = (display.height - app_height) // 2

  eel.init('web')
  eel.start('index.html', size=(app_width, app_height), position=(off_x, off_y))