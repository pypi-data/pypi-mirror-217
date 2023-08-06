"""
ironpdf

IronPdf for Python
"""
# load .NET core
from pythonnet import load
load("coreclr")
# imports
import clr
import sys
import os
import platform
# metadata
__version__ = "2023.7.9"
__author__ = 'Iron Software'
__credits__ = 'Iron Software'
# determine root path for IronPdf files
root = ""
# TODO 7/4/23: actually, we can just hard-code "native_package" to "IronPdf" for all platforms
native_package = ""
if platform.system() == "Windows":
   native_package = "IronPdf.Native.Chrome.Windows"
   root = sys.prefix
elif platform.system() == "Linux":
   native_package = "IronPdf.Native.Chrome.Linux"
   root = os.path.join(os.path.expanduser('~'), ".local")
   if not os.path.exists(os.path.join(root, "IronPdf.Slim", "IronPdf.dll")):
      root = "/usr/local"
elif platform.system() == "Darwin":
   if "arm" in platform.processor().lower():
      native_package = "IronPdf.Native.Chrome.MacOS.ARM"
      root = sys.prefix
   else:
      native_package = "IronPdf.Native.Chrome.MacOS"
      root = sys.prefix
   if not os.path.exists(os.path.join(root, "IronPdf.Slim", "IronPdf.dll")):
      root = "/opt/homebrew"
   if not os.path.exists(os.path.join(root, "IronPdf.Slim", "IronPdf.dll")):
      root = "/usr/local"
if not os.path.exists(os.path.join(root, "IronPdf.Slim", "IronPdf.dll")):
  raise Exception("Failed to locate IronPdf.Slim.dll at '" + root +  "'. Please see https://ironpdf.com/troubleshooting/quick-ironpdf-troubleshooting/ for more information")
print('Using root directory ' + root)
# import ironpdf .net assembly
sys.path.append(os.path.join(root, "IronPdf.Slim"))
clr.AddReference("System.Collections")
clr.AddReference(os.path.join(root, "IronPdf.Slim", "IronPdf.dll"))
# import .net types
from System.Collections.Generic import IEnumerable
from System.Collections.Generic import List
from System import DateTime
from IronPdf import *
from IronPdf.Logging import *
from IronPdf.Engines.Chrome import *
from IronPdf.Rendering import *
from IronPdf.Annotations import *
from IronPdf.Editing import *
from IronPdf.Security import *
from IronPdf.Signing import *
from IronPdf.Extensions import *
from IronPdf.Font import *
# configure ironpdf
Installation.LinuxAndDockerDependenciesAutoConfig = True
Installation.AutomaticallyDownloadNativeBinaries = True
Installation.CustomDeploymentDirectory = os.path.join(root, native_package, __version__)
Installation.ChromeGpuMode = ChromeGpuModes.Disabled
Installation.SetProgrammingLang("python")
if platform.system() == "Darwin":
   Installation.SingleProcess = True
# HELPER METHODS
def ToPage(item):
   """
   Converts the specified integer into a page index for IronPdf
   """
   output = List[int]()
   output.Add(item)
   return output
   
def ToPageList(list):
   """
   Converts the specified list of integers into a list of page indices for IronPdf
   """
   output = List[int]()
   for i in range(len(list)):
      output.Add(list[i])
   return output
   
def ToPageRange(start,stop):
   """
   Creates a list of page indices for IronPdf using the specified start and stop index
   """
   output = List[int]()
   for i in range(start,stop):
      output.Add(i)
   return output

def Now():
   """
   Returns the current date and time
   """
   return DateTime.Now