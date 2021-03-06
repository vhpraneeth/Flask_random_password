from flask import Flask, request
import random, string


class vars:
    var = ''
    html_code = '''
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="shortcut icon" href="https://www.lastpass.com/-/media/43c6c6862a08410a8ef34ab46a3a750b.ico">
        <title> Random password generator </title>

        <p onload="copyText()"/>
        <br> <br> <br>
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
          // when pressed enter on the box, copy password
          myInput.addEventListener("keydown", function (e) {
    		if (e.code === "Enter") // checks whether the pressed key is "Enter"
        		copyText();
		  });
        </script>
    '''


app = Flask(__name__)


def generate_password(minlen=14, minuchars=3, minlchars=3, minnumbers=3, min_other=6):
    # if 1:
    uc_list = random.sample(string.ascii_uppercase, minuchars)
    lc_list = random.sample(string.ascii_lowercase, minlchars)
    n_list = random.sample(string.digits, minnumbers)
    other_chars = string.printable[:-5]
    others_list = random.sample(other_chars, min_other)
    password = uc_list + lc_list + n_list + others_list
    unwanted_chars = ['\t']  # '\\'
    for char in unwanted_chars:
        if char in password:
            password.remove(char)

    # if password length is less than min len, add more char
    # if len(all_list)<minlen:
    #     diff = minlen - len(all_list)
    #     diff_list = random.sample(string.printable, diff)
    #     password = all_list + diff_list
    # else:
    #     password = all_list[:]

    while len(password) < minlen:
        password.append(random.choice(other_chars))
    random.shuffle(password)
    password = ''.join(password)
    return password


@app.route('/', methods=['GET'])
def home():
    return vars.html_code.replace('password123', generate_password())


@app.route('/api/', methods=['GET'])
def api():
    return generate_password()


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


if __name__ == '__main__':
    app.run(port=8080)
