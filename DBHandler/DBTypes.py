def toInt(input : str) -> int:
  result = 0
  while len(input) > 0 and input[0] != '\n': 
    result = result * 10 + (int)(input[0])
    input = input[1:]
  return result

class Period:
  def __init__(self,input : str) -> None:
    inputList = input.split('-')
    self.year = toInt(inputList[0])
    self.month = toInt(inputList[1])
    pass

  month : int = 0
  year : int = 0

class DiagnosticGroup:
  def __init__(self,input : str) -> None:
    idx = 0
    while input[idx] != ',': idx += 1
    
    self.index = toInt(input[:idx])
    self.description = input[idx+1:]
    pass

  description : str = ""
  index : int = 0

class Institution:
  def __init__(self,input : str) -> None:
    self.name = input
    pass
  
  name : str = None

class Region:
  def __init__(self,input : str) -> None:
    self.name = input
    pass
  
  name : str = None

class AgeGroup:
  def __init__(self,input : str) -> None:
    input = input[1:len(input)]
    inputList = input.split('-')
    self.minimumAge = toInt(inputList[0])
    self.maximumAge = toInt(inputList[1])
    pass
  
  minimumAge : int = 0
  maximumAge : int = 0

class HealthRegistry:
  def __init__(self,input : str) -> None:
    inputList = input.split(',')
    self.gender = inputList[0]
    self.numberOfHospitalization = toInt(inputList[1])
    self.daysOfHospitalization = toInt(inputList[2])
    self.outpatient = toInt(inputList[3])
    self.deaths = toInt(inputList[4])

    pass

  gender : str = None
  numberOfHospitalization : int = None
  daysOfHospitalization : int = None
  outpatient : int = None
  deaths : int = None
  
class Entry:

  def __init__(self,PeriodObj,DiagnosticGroupObj,InstitutionObj,RegionObj,AgeGroupObj,HealthRegistryObj) -> None:
    self.period = PeriodObj
    self.diagnostic = DiagnosticGroupObj
    self.institution = InstitutionObj
    self.region = RegionObj
    self.ageGroup = AgeGroupObj
    self.healthRegistry = HealthRegistryObj
    pass


  period : Period = None
  diagnostic : DiagnosticGroup = None
  institution : Institution = None
  region : Region = None
  ageGroup : AgeGroup = None
  healthRegistry : HealthRegistry = None
