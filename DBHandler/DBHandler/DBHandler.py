import sqlite3,os
from DBHandler import DBTypes
from DBHandler import Parser

class DBHandler:
  def __init__(self) -> None:
    '''Initializes Database'''
    databasePath = 'DBHandler/morbilidade.db'
    needsInsertion = False
    if(os.path.exists('DBHandler/morbilidade.db') == False): needsInsertion = True


    #Create and connect to database
    self._connector = sqlite3.connect(databasePath)
    if(self._connector is None):
      print("Connection failed,aborting...")
      exit()

    print("Connection succeded")
    self._cursor = self._connector.cursor()

    if(self._cursor is None):
      print("Cursor is invalid,aborting...")
      exit()

    print("Cursor created successfully")
    if(self.createTables() == False):
      print("Error creating tables,aborting...")
      exit()
    print("Tables created successfully")

    self.__insert()

  def __del__(self):
    if(self._connector is None):
      return
    self._connector.close()

  def __queryDatabase(self,input : str) -> list[any]:

    try:
       result = self._cursor.execute(input)
       return result.fetchall()
    except sqlite3.ProgrammingError:
      print("Invalid input")
      return None
    except Exception as error:
      print("Something has gone terribly wrong:",error)
      return None

  
  def query(self,input : str):
    if(self._cursor is None):
      print("Cursor is invalid,aborting...")
      exit()

    data = self.__queryDatabase(input)
    return data 

  def getData(self,filePath = 'DBHandler/morbilidade.csv'):
      entries = Parser.parseCSV(filePath)
      if(entries is None):
        print("Entries is Null,aborting...")
        exit()
      return entries


  def __insert(self):
    def checkRegions(self,regionName):
      if(len(self._cursor.execute('SELECT * FROM regions WHERE name = ?',(regionName,)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO regions VALUES (NULL,?)",(regionName,))

    def insertInstitution(self,institutionName,regionName):
      if(len(self._cursor.execute('SELECT * FROM institutions WHERE name = ?',(institutionName,)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO institutions VALUES (NULL,?,?)",
                             (institutionName,self._cursor.execute('SELECT id FROM regions WHERE name = ?',(regionName,)).fetchone()[0]))

    def insertAgeGroup(self,minimumAge,maximumAge):
      if(len(self._cursor.execute('SELECT * FROM ageGroups WHERE (minimumAge,maximumAge)=(?,?)',(minimumAge,maximumAge)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO ageGroups VALUES (NULL,?,?)",(minimumAge,maximumAge))

    def insertPeriod(self,month,year):
      if(len(self._cursor.execute('SELECT * FROM periods WHERE (month,year)=(?,?)',(month,year)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO periods VALUES (NULL,?,?)",(month,year))

    def inserDiagnosticGroup(self,code,description):
      if(len(self._cursor.execute('SELECT * FROM diagnosticGroups WHERE (code,description)=(?,?)',(code,description)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO diagnosticGroups VALUES (NULL,?,?)",(code,description))

    def insertHealthRegistry(self : DBHandler,entry : DBTypes.Entry):
      institutionId = self._cursor.execute('SELECT id FROM institutions where name = ?',(entry.institution.name,)).fetchone()[0]
      ageId = self._cursor.execute('SELECT id FROM ageGroups where (minimumAge,maximumAge) = (?,?)',(entry.ageGroup.minimumAge,entry.ageGroup.maximumAge)).fetchone()[0]
      periodId = self._cursor.execute('SELECT id FROM periods where (month,year) = (?,?)',(entry.period.month,entry.period.year)).fetchone()[0]
      diagnosticId = self._cursor.execute('SELECT id FROM diagnosticGroups where code = ?',(entry.diagnostic.index,)).fetchone()[0]

      health = entry.healthRegistry
      self._cursor.execute("INSERT INTO healthRegistries VALUES (NULL,?,?,?,?,?,?,?,?,?)",
                           (health.gender,health.numberOfHospitalization,health.daysOfHospitalization,
                           health.outpatient,health.deaths,institutionId,ageId,periodId,diagnosticId)
                          )

    entries = self.getData()

    for entry in entries:
      checkRegions(self,entry.region.name)
      insertInstitution(self,entry.institution.name,entry.region.name)
      insertAgeGroup(self,entry.ageGroup.minimumAge,entry.ageGroup.maximumAge)
      insertPeriod(self,entry.period.month,entry.period.year)
      inserDiagnosticGroup(self,entry.diagnostic.index,entry.diagnostic.description)
      insertHealthRegistry(self,entry)
      
    self._connector.commit()
    print("All data inserted")
      

  def createTables(self):
    sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(255) NOT NULL 
        );""",
    """CREATE TABLE IF NOT EXISTS diagnosticGroups (
            id INTEGER PRIMARY KEY,
            code INT NOT NULL, 
            description VARCHAR(255) NOT NULL 
        );""",
    """CREATE TABLE IF NOT EXISTS periods (
            id INTEGER PRIMARY KEY, 
            month INT NOT NULL,
            year INT NOT NULL 
        );""",
    """CREATE TABLE IF NOT EXISTS ageGroups (
            id INTEGER PRIMARY KEY,
            minimumAge INT NOT NULL, 
            maximumAge INT NOT NULL 
        );""",
    
    """CREATE TABLE IF NOT EXISTS institutions (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        regionId INT NOT NULL,
        FOREIGN KEY (regionId) REFERENCES regions (id)
        );""",
    """CREATE TABLE IF NOT EXISTS healthRegistries (
        id INTEGER PRIMARY KEY,
        gender CHAR(1) NOT NULL,
        hospitalizations INT NOT NULL,
        daysOfHospitalization INT NOT NULL,
        outpatient INT NOT NULL,
        deaths INT NOT NULL,
        institutionId INT NOT NULL,
        ageGroupId INT NOT NULL,
        periodId INT NOT NULL,
        diagnosticGroupId INT NOT NULL,
        FOREIGN KEY (institutionId) REFERENCES institutions (id),
        FOREIGN KEY (ageGroupId) REFERENCES ageGroups (id),
        FOREIGN KEY (periodId) REFERENCES periods (id),
        FOREIGN KEY (diagnosticGroupId) REFERENCES diagnosticGroups (id)
        );""",
    ]

    for statement in sql_statements:
      try:
        self._cursor.execute(statement)
      except:
        print("Unable to create table, Statement:\n" + statement)
        return False
    self._connector.commit()
    return True

  _connector : sqlite3.Connection = None
  _cursor : sqlite3.Cursor = None 



#def main():
 # handler = DBHandler()
  #handler.insert()

#if __name__ == "__main__":
 # main()


