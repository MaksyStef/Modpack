import main
import tk_extend

import unittest
import os


class TestExportInstance(unittest.TestCase):
  instance = {
    'name': '1.20.1 Fabric', 
    'gameDir': 'C:\\Users\\steva\\AppData\\Roaming\\.minecraft-1-20-1', 
    'lastVersionId': 'fabric-loader-0.16.0-1.20.1', 
    'resolution': {'width': 800, 'height': 600, 'fullscreen': False}, 
    'type': 'custom', 
    'created': '2024-08-31T19:05:45+02:00', 
    'lastUsed': '2024-12-22T21:25:35+01:00', 
    'icon': 'Creeper_Head'
  }
  
  def test_export_instance(self):
    exported = main.export_instance(self.instance)
    expected = os.path.expanduser('Downloads\\'+self.instance['name']+'.zip')
    self.assertTrue(os.path.isfile(exported))
    
class TestTkExtended(unittest.TestCase):
  def test_directory_tree_checklist(self):
    base = "C:\\Users\\steva\\AppData\\Roaming\\.minecraft-1-20-1"
    prechecked_paths = [
        "resourcepacks",
        "mods",
        "options.txt"
    ]
    result = tk_extend.ask_directory_tree_with_checkboxes(base, prechecked_paths)
    print("Selected paths:")
    for r in result:
        print(r)