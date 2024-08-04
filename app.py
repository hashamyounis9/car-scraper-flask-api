from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()


def scrape_car(url):
    res = {'key': 'value'}
    with sync_playwright() as pw:
        server = os.getenv('SERVER')
        port = os.getenv('PORT')
        # USERNAME somehow doesn't work, returns os username
        username = os.getenv('USERNAMES')
        password = os.getenv('PASS')
        print(server)
        print(port)
        print(username)
        print(password)
        browser = pw.chromium.launch(proxy={
            "server": server + ':' + port,
            "username": username,
            "password": password
        })
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state()
        car_title = page.query_selector('#scroll_car_info > h1')
        price = page.query_selector(
            '#scrollToFixed > div.side-bar > div.well.price-well.pos-rel.mb20 > div > strong')
        model = page.query_selector(
            '#scroll_car_info > table > tbody > tr > td:nth-child(1) > p > a')
        mileage = page.query_selector(
            '#scroll_car_info > table > tbody > tr > td:nth-child(2) > p')
        car_type = page.query_selector(
            '#scroll_car_info > table > tbody > tr > td:nth-child(3) > p > a')
        if car_type:
            car_type = car_type.text_content() + ' and ' + page.query_selector(
                '#scroll_car_info > table > tbody > tr > td:nth-child(4) > p > a').text_content()
        location = page.query_selector('#scroll_car_info > p > a')
        if not car_title or not price or not model or not mileage or not car_type or not location:
            return {'error': 'could not find car details on given url'}, 400
        res['car_title'] = car_title.text_content()
        res['price'] = price.text_content()
        res['model'] = model.text_content()
        res['mileage'] = mileage.text_content()
        res['car_type'] = car_type
        res['location'] = location.text_content()
    res.pop('key')
    response = jsonify(res)
    response.status_code = 200
    return response


@app.route("/")
def index():
    url = request.args.get('url')
    if not url:
        return jsonify({"Error": "missing 'url' paramerter"}), 400
    res = scrape_car(url=url)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
