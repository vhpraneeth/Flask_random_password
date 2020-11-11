from flask import Flask
import random
import string

app = Flask(__name__)

class vars:
    html_part = '''
        <title> Random password generator </title>
        <script>
            function myFunction() {
            var copyText = document.getElementById("myInput");
            copyText.select();
            //copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            }
        </script>
        <input type="text" value="password123" id="myInput">
        <button onclick="myFunction()">Copy text</button>
        <button id="reloadbutton"><a href="/">Reload</a></button>
    '''

@app.route('/', methods=['GET'])
def home():
    password = generate_password()
    html = vars.html_part.replace('password123', password)
    return html  # password


@app.route('/api/', methods=['GET'])
def api():
    password = generate_password()
    return password


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
        passwd = all_list + diff_list
    else:
        passwd = all_list[:]
    random.shuffle(passwd) #shuffle'em
    return ''.join(passwd)


if __name__ == '__main__':
    app.run(debug=False)
