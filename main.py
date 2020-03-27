import json
import requests
from datetime import datetime
from flask import Flask
app = Flask('app')

@app.route('/')
def home_route():
  headers = {
    'Referer': 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
  }
  resp = requests.get('https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=190&cacheHint=true', headers=headers)
  parsed = json.loads(resp.text)
  cos = parsed.get('features')

  total_deaths = 0
  total_confirmed = 0

  html = '''
  <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
  </style>
  <table>
            <tr>
            <th>Region</th>
            <th>Confirmed</th>
            <th>Recovered</th>
            <th>Deaths</th>
            <th>Active</th>
            <th>Last update</th>
            </tr>'''
  for co in cos:
    name = co.get('attributes').get('Country_Region')
    confirmed =  co.get('attributes').get('Confirmed')
    total_confirmed += int(confirmed)
    recovered  =  co.get('attributes').get('Recovered')
    deaths  =  co.get('attributes').get('Deaths')
    total_deaths += int(deaths)
    active  =  co.get('attributes').get('Active')
    ts = str(datetime.fromtimestamp(co.get('attributes').get('Last_Update')/1000))
    html = html + f'''<tr>
                        <td>{name}</td>
                        <td>{confirmed}</td>
                        <td>{recovered}</td>
                        <td>{deaths}</td>
                        <td>{active}</td>
                        <td>{ts}</td>
                      </tr>'''
  html = html + '</table>'
  html = f'<h1>Total confirmed: {total_confirmed}<h1/><h1>Total deaths: {total_deaths}<h1/>' + html
  return html

if __name__=='__main__':
  app.run(host='0.0.0.0', port=8080)