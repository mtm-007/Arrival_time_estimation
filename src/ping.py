from flask import Flask

app = Flask('Ping')

@app.route('/ping', methods=['GET'])
def ping():
    return f'Test flask check 1!\n'


if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0', port=9696)