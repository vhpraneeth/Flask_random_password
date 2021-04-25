from flask import Flask, request
import random
import string


class vars:
    var = ''
    html_code = '''
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="shortcut icon" href="https://www.lastpass.com/-/media/43c6c6862a08410a8ef34ab46a3a750b.ico">
        <title> Random password generator </title>
        <p onload="copyText()"/>
        <br/> <br/> <br/>
        <div class="contentcontainer med left" style="margin-left: 200px;">
          <input type="text" value="password123" id="myInput" onfocus="copyText()">
          <button type="submit" onclick="copyText()" class="btn btn-success btn-lg">Copy text</button>
          <a class="btn btn-outline-dark" href="/" role="button">Reload</a>
        </div>

        <script>
          function copyText() {
            // copy random password after button click
            myInput.select();
            document.execCommand("copy");
          }
          myInput.addEventListener("keydown", function (e) {
    		if (e.code === "Enter") // checks whether the pressed key is "Enter"
        		copyText();
		  });
        </script>
    '''


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    password = generate_password()
    html = vars.html_code.replace('password123', password)
    return html


@app.route('/api/', methods=['GET'])
def api():
    password = generate_password()
    return password


@app.route('/var/', methods=['GET', 'POST'])
def change_var():
    ' To store the value the user wants '
    try:
        var = request.args.get('var')  # use /var?var=abcd to update the stored value
    except:
        var = ''
    if var:  # store value
        if len(var) < 50:
            vars.var = var
        else:
            return 'Text too long to store. Limit is 50'
    else:  # read value
        var = vars.var
    return var


def generate_password(minlen=15, minuchars=3, minlchars=3, minnumbers=3, min_other=3):
    # random sample lists for each char type
    other_chars = string.printable[:-5]
    other_chars = other_chars.replace('\\', '')
    uc_list = random.sample(string.ascii_uppercase, minuchars)
    lc_list = random.sample(string.ascii_lowercase, minlchars)
    n_list = random.sample(string.digits, minnumbers)
    others_list = random.sample(other_chars, min_other)
    #join them in one list
    all_list = uc_list + lc_list + n_list + others_list
    #if total chars is less than min len, full with printables
    if len(all_list)<minlen:
        diff = minlen - len(all_list)
        diff_list = random.sample(string.printable, diff)
        password = all_list + diff_list
    else:
        password = all_list[:]
    random.shuffle(password)
    return ''.join(password)


if __name__ == '__main__':
    app.run(port=8080)
