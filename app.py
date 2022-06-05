import os
import json
import requests
from flask import Flask, render_template, url_for
from jinja2 import Markup


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    files = sorted([ f for f in os.listdir(os.path.join(APP_ROOT,'contributors')) if '.json' in f ])
    
    astring = ""
    bstring = ""

    count = 0
    for f in files:
        with open(os.path.join(APP_ROOT,'contributors/'+f)) as fh:
            jsonfile = json.loads(fh.read())

            avatar = ""

            for fname in os.listdir(os.path.join(APP_ROOT,'static/avatars')):
                if f[:-5]+"." in fname:
                    avatar = url_for('static',filename='avatars/'+fname)
            if avatar:
                pass
            else:
                avatar = url_for('static', filename='default.png')

            
            skills_hobbies = ""
            for skill in jsonfile['skills_hobbies']:
                skills_hobbies += f'<span class="text-light px-2 py-1 mx-1 mb-1 rounded translucent" style="background:#38007d; font-weight:500">{skill}</span>'

            astring += f"""
            <div class="card text-dark shadow mr-2 mb-4 bg-light" style="max-width: 22rem">
                <div class="card-header text-center h5 mb-0">
                    {f[:-5]}
                </div>
                <div class="card-body">
                    <img src="{avatar}" width="128px" alt="..." class="mx-auto my-auto d-block rounded" draggable="false">
                </div>
                <button type="button" class="btn btn-dark" data-toggle="modal" data-target="#{"c"+str(count)}">
                    View Contributor
                </button>
            </div>\n
            """

            bstring += f"""
            <div class="modal fade" id="{"c"+str(count)}" tabindex="-1" aria-labelledby="{"c"+str(count)}" aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <center><h5 class="modal-title" id="{"c"+str(count)}">{f[:-5]}</h5></center>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <img src="{avatar}" width="200px" alt="..." class="mx-auto d-block img-thumbnail mb-3" draggable="false">

                                <h3 class="h3 text-center">About</h3>

                                <blockquote class="blockquote text-center mb-4">
                                    <p>{jsonfile['about']}</p>
                                </blockquote>

                                <table class="table table-hover">
                                    <tbody>
                                        <tr>
                                            <th scope="row">Name</th>
                                            <td>{jsonfile['name']}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Course</th>
                                            <td>{jsonfile['course']}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Batch</th>
                                            <td>{jsonfile['batch']}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Institution</th>
                                            <td colspan="2">{jsonfile['institution']}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Skills/Hobbies</th>
                                            <td class="d-flex flex-wrap" colspan="2">
                                                {skills_hobbies}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>

                            </div>
                            <div class="modal-footer">
                                <a href="https://github.com/{f[:-5]}" target="_blank" class="mx-auto"><img src="{url_for('static', filename='github.png')}" class="translucent" alt="{f[:-5]}'s GitHub" width="56px" draggable="false"></a>
                            </div>
                        </div>
                    </div>
                </div>
            """
        count+=1
    return render_template('home.html', astring=astring, bstring=bstring, count=count)

port = os.environ.get('PORT', 5000)
if __name__ == '__main__':
    app.run(threaded=True, port=port)