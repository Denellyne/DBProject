import os
from DBHandler import DBTypes

def parseString(line : str):
  period = DBTypes.Period(line[:7])
  line = line[8:]
  idx = 0
  diagnosticGroup : DBTypes.DiagnosticGroup = None
  while line[idx] != ',':
    idx += 1
  idx += 1
  if line[idx] == "\"":
    str = line[:idx]
    idx += 1
    while line[idx] != '\"':
      str += line[idx]
      idx += 1
    diagnosticGroup = DBTypes.DiagnosticGroup(str)
    idx += 2
  else:
    while line[idx] != ',':
      idx += 1
    diagnosticGroup = DBTypes.DiagnosticGroup(line[:idx])
    idx += 1
  line = line[idx:]
  idx = 1
  institution : DBTypes.Institution = None
  if line[0] == "\"":
    while line[idx] != '\"':
      idx += 1
    institution = DBTypes.Institution(line[1:idx])
    idx += 2
  else:
    while line[idx] != ',':
      idx += 1
    institution = DBTypes.Institution(line[:idx])
    idx += 1
  line = line[idx:]
  idx = 0
  while line[idx] != ',':
    idx += 1
  region = DBTypes.Region(line[:idx])
  line = line[idx+1:]
  idx = 0
  while line[idx] != ',':
    idx += 1
  age = DBTypes.AgeGroup(line[:idx-1])
  line = line[idx+1:]

  return DBTypes.Entry(period,diagnosticGroup,institution,region,age,DBTypes.HealthRegistry(line))

def parseCSV(filePath : str) -> list[DBTypes.Entry]:
  listParsed = []
  if(os.path.isfile(filePath) == False):
      print("CSV not found")
      return None
  try:
    file = open(filePath,"r")
    file.readline()
    while line := file.readline():
      listParsed += [parseString(line)]
    file.close()
  except OSError:
     print("Error opening file")
     return None
    
  file.close()
  return listParsed
  
