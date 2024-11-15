from flask import Flask,render_template
from DBHandler import DBHandler

app = Flask(__name__)

#-
  #JOIN
    #  (SELECT COUNT(*) n_actors FROM ACTOR)
    #JOIN
    #  (SELECT COUNT(*) n_genres FROM MOVIE_GENRE)
    #JOIN 
    #  (SELECT COUNT(*) n_streams FROM STREAM)
    #JOIN 
    #  (SELECT COUNT(*) n_customers FROM CUSTOMER)
    #JOIN 
     # (SELECT COUNT(*) n_countries FROM COUNTRY)
   # JOIN 
    #  (SELECT COUNT(*) n_regions FROM REGION)
  #  JOIN 
 #     (SELECT COUNT(*) n_staff FROM STAFF)

@app.route("/")
def index():
  handler = DBHandler.DBHandler()
  stats = handler._cursor.execute('''
      SELECT * FROM
        (SELECT COUNT(*) numberAgeGroups FROM ageGroups)
      JOIN
        (SELECT COUNT(*) numberInstitutions FROM institutions)
      JOIN
        (SELECT COUNT(*) numberRegions FROM regions)
      JOIN
        (SELECT COUNT(*) numberDiagnostics FROM diagnosticGroups)
      JOIN
        (SELECT COUNT(*) numberPeriods FROM periods)
      JOIN
        (SELECT COUNT(*) numberHealthRegistries FROM healthRegistries)
                        
                                  
                                  ''').fetchone()

  return render_template('index.html',stats=stats)


