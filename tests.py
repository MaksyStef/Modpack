main = __import__("main.py")

import unittest
import os


class TestExportInstance(unittest.TestCase):
  def __init__(self):
    self.instance = {
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
    expected = "C:\\Users\\steva\\Downloads\\1.20.1 Fabric.zip"
    self.failUnless(os.path.isfile(exported.filename), "Expected file has no path")