# D:\PythonProjects\DublinBike\predWeb\predApp.py

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route


@app.route('/showPred/<int:predNum>')
def showPred(predNum):
    showString = 'The predicted number of the available bikes is '
    showString += str(predNum)
    showString += '.'
    return showString
    #return 'The predicted unmber of the available bikes is %d' % predNum

@app.route('/predFun', methods=['POST'])
def predFun():
    user=request.form['day']
    return redirect(url_for('showPred',predNum=15))

if __name__ == '__main__':
    app.run(debug=True)
