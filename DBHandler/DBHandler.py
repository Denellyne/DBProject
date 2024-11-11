import sqlite3,os

class DBHandler:
  def __init__(self,databasePath : str) -> None:
    '''Initializes Database'''

    # Check if database exists
    if(os.path.isfile(databasePath) == False):
      print("Database not found,aborting...")
      exit()

    # Connects to database
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
    if(data is None): 
      return 
    for row in data: 
      print('Title:', row['title'],
            'Year:', row['year'])


  _connector : sqlite3.Connection = None
  _cursor : sqlite3.Cursor = None 



if __name__ == "__main__":
  handler = DBHandler('movie_stream.db')

  handler.query("SELECT Title,Year FROM MOVIE WHERE Title LIKE '%star wars%' ORDER BY Year DESC")

