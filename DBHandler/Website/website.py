from flask import Flask, render_template, request
from DBHandler import DBHandler
from Website.util import addSubmit, addQuerySelector

app = Flask(__name__)


@app.post("/search")
def search():
    sqlCommand = request.form["sql"]
    handler = DBHandler.DBHandler()
    data = handler.queryForHTML(sqlCommand)
    return render_template('search.html', sql=data)


@app.post("/institutions")
@app.route("/institutions")
def institutions():
    institutionId = 1
    if (request.method == 'POST'):
        institutionId = request.form["region"]
    handler = DBHandler.DBHandler()

    sqlCommand = "SELECT institutions.name as Institution,regions.name as Region FROM institutions inner join regions on institutions.regionId = regions.id WHERE regionId ="
    sqlCommand += str(institutionId)
    sqlCommand += " ORDER BY Institution"

    data = handler.queryForHTML(sqlCommand)
    query, info = addQuerySelector("region", handler.query(
        "Select * FROM regions"), institutionId)
    queryList = [query]
    querys = addSubmit("institutions", queryList)

    info = "Institutions in the Region of: " + info

    return render_template('search.html', sql=data, querys=querys, info=info)


@app.post("/diagnosisGroupsByInstitution")
@app.route("/diagnosisGroupsByInstitution")
def diagnosisGroupsByInstitution():
    institutionId = 1
    month = 1
    year = 2020
    if (request.method == 'POST'):
        institutionId = request.form["institution"]
        month = request.form["month"]
        year = request.form["year"]

    handler = DBHandler.DBHandler()
    sqlCommand = "SELECT d.description as Description,(a.minimumAge || ' - ' || a.maximumAge) as 'Age Range',i.name as Institution,r.name as Region,p.month as Month,p.year as Year,hR.gender as Gender,hR.hospitalizations as Hospitalizations,hR.daysOfHospitalization as 'Days of Hospitalization',hR.outpatient as Outpatient,hR.deaths as Deaths FROM healthRegistries hR inner join institutions i on hR.institutionId = i.id inner join periods p on hR.periodId = p.id inner join regions r on i.regionId = r.id inner join diagnosticGroups d on hR.diagnosticGroupId = d.id inner join ageGroups a on hR.ageGroupId = a.id WHERE p.month ="
    sqlCommand += str(month) + " and p.year=" + str(year) + " and i.id=" + \
        str(institutionId) + " ORDER BY d.code,a.minimumAge desc,hR.gender desc"

    data = handler.queryForHTML(sqlCommand)
    query, institutions = addQuerySelector("institution", handler.query(
        "Select i.id,i.name FROM institutions i"), institutionId)
    queryList = [query]

    query, _ = addQuerySelector("month", handler.query(
        "Select p.month,p.month FROM periods p Group by p.month"), month)
    queryList.append(query)
    query, _ = addQuerySelector("year", handler.query(
        "Select p.year,p.year FROM periods p Group by p.year"), int(year)-2015)
    queryList.append(query)

    querys = addSubmit("diagnosisGroupsByInstitution", queryList)
    info = "Diagnosis Groups from the Institution: " + institutions + \
        ", in the date of: " + str(month) + '-' + str(year)

    return render_template('search.html', sql=data, querys=querys, info=info)


@app.route("/institutionsByDeaths")
def institutionsByDeaths():
    handler = DBHandler.DBHandler()

    sqlCommand = """
  select i.name as Institution, r.name as Region, sum(hr.deaths) as 'Total Deaths'
  from institutions i join regions r on i.regionId = r.id
  join healthRegistries hr on hr.institutionId = i.id
  group by i.name, r.name
  order by sum(hr.deaths) desc;
  """

    data = handler.queryForHTML(sqlCommand)

    info = "Institutions Ordered by Total Deaths"

    return render_template('search.html', sql=data, info=info)


@app.route("/regionsByDeaths")
def regionsByDeath():
    handler = DBHandler.DBHandler()

    sqlCommand = """
  select r.name as 'Region', sum(hr.deaths) as 'Total Deaths'
  from institutions i join regions r on i.regionId = r.id
  join healthRegistries hr on hr.institutionId = i.id
  group by r.name
  order by sum(hr.deaths) desc;
  """

    data = handler.queryForHTML(sqlCommand)

    info = "Regions Ordered by Total Deaths"

    return render_template('search.html', sql=data, info=info)


@app.route("/institutionsByHospitalizations")
def institutionsByHospitalizations():
    handler = DBHandler.DBHandler()

    sqlCommand = '''
  select i.name as 'Institution', r.name as 'Region', sum(hr.hospitalizations) as 'Total Hospitalizations', ifnull(round(avg(hr.daysofhospitalization / hr.hospitalizations), 1) || ' day/s', 0) as 'Average Hospitalization Time Per Case'
  from institutions i join regions r on i.regionId = r.id
  join healthRegistries hr on hr.institutionId = i.id
  group by i.name, r.name
  order by sum(hr.hospitalizations) desc, round(avg(hr.daysofhospitalization / hr.hospitalizations), 1) desc;
  '''

    data = handler.queryForHTML(sqlCommand)
    info = "Institutions Ordered by Total Hospitalizations"
    return render_template('search.html', sql=data, info=info)


@app.route("/diagnosisGroupsByDeathsAndHospitalizations")
def diagnosisGroupsByDeathsAndHospitalizations():
    handler = DBHandler.DBHandler()

    sqlCommand = '''
  select dg.description as 'Diagnosis Group', sum(hr.hospitalizations) as 'Total Hospitalizations Per Diagnosis Group', sum(hr.deaths) as 'Total Deaths Per Diagnosis Group'
  from diagnosticGroups dg join healthRegistries hr on dg.id=hr.diagnosticgroupId
  group by dg.description
  order by sum(hr.hospitalizations) desc, sum(hr.deaths) desc;
  '''
    data = handler.queryForHTML(sqlCommand)
    info = "Diagnosis Groups Ordered by Total Deaths and Hospitalizations"
    return render_template('search.html', sql=data, info=info)

@app.route("/morbidityAndMortalityPerAgeGroupForEachDiagnosisGroup")
def morbidityAndMortalityPerAgeGroupForEachDiagnosisGroup():
    handler = DBHandler.DBHandler()

    sqlCommand = '''
  select dg.description as 'Diagnosis Group', (ag.minimumAge || ' - ' || ag.maximumAge) as 'Age Range', sum(hr.hospitalizations) as 'Total Hospitalizations', sum(hr.deaths) as 'Total Deaths'
  from healthRegistries hr join diagnosticGroups dg on hr.diagnosticGroupId = dg.id
  join ageGroups ag on ag.id = hr.ageGroupId
  group by dg.description, ag.minimumAge, ag.maximumAge
  order by dg.description, ag.minimumAge;
  '''
    data = handler.queryForHTML(sqlCommand)
    info = "Diagnosis Groups for each Age Group Ordered by Total Deaths and Hospitalizations"
    return render_template('search.html', sql=data, info=info)
    


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

    return render_template('index.html', stats=stats)
