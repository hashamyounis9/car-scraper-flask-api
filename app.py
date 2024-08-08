from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# load_dotenv()


def scrape_car(url):
    res = {'key': 'value'}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(proxy={
            "server": "45.127.248.127:5128",
            "username": "gufqwanb",
            "password": "jxm7x6o1k09u"
        })
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state()
            car_featured = page.query_selector(
                '#myCarousel > div.featured-ribbon.pointer > div > div')
            if car_featured:
                res['is_car_featured'] = True
            else:
                res['is_car_featured'] = False
            car_features = page.query_selector(
                '#scroll_car_info > ul.list-unstyled.car-feature-list.nomargin')
            seller_comment = page.query_selector(
                '#scroll_car_info > div:nth-child(14)')
            registered_in = page.query_selector(
                '#scroll_car_detail > li:nth-child(2)').inner_text()
            color = page.query_selector(
                '#scroll_car_detail > li:nth-child(4)').inner_text()
            assembly = page.query_selector(
                '#scroll_car_detail > li:nth-child(6)').inner_text()
            engine_capacity = page.query_selector(
                '#scroll_car_detail > li:nth-child(8)').inner_text()
            body_type = page.query_selector(
                '#scroll_car_detail > li:nth-child(10) > a').inner_text()
            last_updated = page.query_selector(
                '#scroll_car_detail > li:nth-child(12)').inner_text()
            ad_ref_no = page.query_selector(
                '#scroll_car_detail > li:nth-child(14)').inner_text()
            car_image = page.query_selector(
                '#myCarousel > div.lSSlideOuter.h-thumbs > div.lSSlideWrapper.usingCss.img-box > ul > li.lslide.active > img')
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
        except Exception as e:
            return jsonify({"error": e})
        if not car_title or not price or not model or not mileage or not car_type or not location:
            return {'error': 'could not find car details on given url'}, 400
        res['car_title'] = car_title.text_content()
        res['price'] = price.text_content()
        res['model'] = model.text_content()
        res['mileage'] = mileage.text_content()
        res['car_type'] = car_type
        res['location'] = location.text_content()
        res['car_image'] = car_image.get_attribute('src')
        res['car_details'] = {
            "registered_in": registered_in,
            "color": color,
            "assembly": assembly,
            "engine_capacity": engine_capacity,
            "body_type": body_type,
            "last_updated": last_updated,
            "ad_ref_no": ad_ref_no
        }
        res['seller_comment'] = seller_comment.inner_text()
        res['car_features'] = car_features.inner_text()
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