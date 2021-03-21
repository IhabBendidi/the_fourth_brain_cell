import flask
import recommendation
from flask import request
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/get_recommendation', methods=['GET'])
def moyen_transports():
    code = 200
    question = request.args.get('question')
    if question == '':
        code = 404
        output = "Enter a proper question"
    else :
        output = recommendation.get_question(question)
    return {"code":code,"response":output}


if __name__ == "__main__":
    app.run(port=4500) #host= '0.0.0.0')
#app.run(threaded=True, port=5000)
