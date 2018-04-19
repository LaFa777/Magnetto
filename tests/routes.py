add_header("Content-Type", "text/html; charset=utf-8")

directory_to_html = "./htmls/"
site = ""


def file(str):
    return body(open(directory_to_html + str))


def is_path(str):
    return (bool)(path == (site + str))


# эмуляция Rutracker.org
site = "/rutracker"

if is_path("/index.php"):
    if request.headers['Cookie']:
        file('rutracker_index_auth.html')
    else:
        body("Not logged")

elif is_path("/login.php"):
    if request.headers['Cookie']:
        add_header("Location", site + "/index.php")
        redirect(site + '/index.php')

    # корректные данные для входа
    if (request.form.get('login_username') == "good" and
            request.form.get('cap_code_1234') == "1234"):
        add_header(
            "Set-Cookie", "bb_session=0-11111111-Qh6z0mUuTrTfuluhxTX3")
        redirect(site + '/index.php')
    # некорректные данные для входа или неправильная капча
    if (request.form.get('login_username') == "bad" or
            'cap_code_1234' in request.form):
        file('rutracker_login_incorrect.html')
    else:
        file('rutracker_login_with_captcha.html')

elif is_path("/tracker.php") and query:
    file('rutracker_search.html')

else:
    error(404)
