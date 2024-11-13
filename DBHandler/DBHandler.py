import sqlite3,os,Parser,DBTypes

class DBHandler:
  def __init__(self) -> None:
    '''Initializes Database'''
    databasePath = 'morbilidade.db'

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
    self._cursor.row_factory = sqlite3.Row


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

  def getData(self,filePath = 'morbilidade.csv'):
      entries = Parser.parseCSV(filePath)
      if(entries is None):
        print("Entries is Null,aborting...")
        exit()
      return entries
  
  def insert(self):
    entries = self.getData()
    for entry in entries:
      if(len(self._cursor.execute('SELECT * FROM regions WHERE name = ?',(entry.region.name,)).fetchall()) == 0):
        self._cursor.execute("INSERT INTO regions VALUES (NULL,?)",(entry.region.name,))
      self._cursor.execute("INSERT INTO institutions VALUES (NULL,?,?)",(entry.institution.name,
                                                                         self._cursor.execute('SELECT id FROM regions WHERE name = ?',(entry.region.name,)).fetchone()[0]))
      
    self._connector.commit()
      

  def createTables(self):
    sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(255) NOT NULL 
        );""",
    """CREATE TABLE IF NOT EXISTS diagnosticGroups (
            id INTEGER PRIMARY KEY,
            code INT NOT NULL, 
            name VARCHAR(255) NOT NULL 
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
    """CREATE TABLE IF NOT EXISTS healthRegistrys (
        id INTEGER PRIMARY KEY,
        gender INT NOT NULL,
        hospitalization INT NOT NULL,
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
    self._connector.commit()

  _connector : sqlite3.Connection = None
  _cursor : sqlite3.Cursor = None 

  
if __name__ == "__main__":
  handler = DBHandler()
  handler.createTables()
  handler.insert()



