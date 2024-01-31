from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, g
import requests
import urllib3
import json
import base64
import pymysql
import re
import time
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'python_project'  # 실제로는 더 복잡하고 안전한 키를 사용해야 합니다.

user_table = 'userTable'  # 유저 테이블
product_list_table = 'product_list'  # 상품 리스트 테이블

openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
accessKey = "cd5dec33-9861-4df3-9144-81753d78e606"
naverClientId = "ziALS23mD4KX9OJX74GG"
naverClientSecret = "Ss9ydhFjrb"

# 네이버 API 설정
NAVER_CLIENT_ID = 'ziALS23mD4KX9OJX74GG'
NAVER_CLIENT_SECRET = 'Ss9ydhFjrb'


# 데이터베이스 연결 함수
def get_db():
    db_config = {
        "host": "외부 IP",
        "user": "sejoon",
        "password": "dkstpwns1!",
        "db": "Product_Information_Crawling",
        "charset": "utf8mb4",
        "port": 33060,
        "cursorclass": pymysql.cursors.DictCursor,
        "use_unicode": True
    }

    try:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = pymysql.connect(**db_config)

        cur = db.cursor()
        print("Connection and Cursor objects:", db, cur)
        return db, cur
    except Exception as e:
        # 적절한 오류 처리를 수행하고 예외를 다시 발생시킴
        print(f"Error connecting to the database: {e}")
        raise


@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# 제품의 이름 저장 시 태그 없애기
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


# 텍스트로 상품 정보 검색 함수에 데이터베이스 저장 기능 추가
def search_text(query):
    url = 'https://openapi.naver.com/v1/search/shop.json'
    headers = {
        'Content-Type': 'application/json',
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
    }
    params = {'query': query, 'display': 100}
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    # 디버그를 위한 출력
    print("[Naver Response Code] " + str(response.status_code))
    print("[Naver Response Body]")
    print(result)

    # 응답 내용 확인 후 수정
    if 'items' in result:
        items = result['items']

        # 데이터베이스에 상품 객체 추가
        db, cur = get_db()
        for item in items:
            product_name = remove_tags(item.get('title', ''))

            # 데이터베이스에 검색된 상품이 있는 지 확인
            cur.execute(
                'SELECT * FROM product_list WHERE product_link = %s', (item.get('link', ''),))
            result = cur.fetchone()

            # 같은 상품이 없으면 데이터베이스에 저장
            if result is None:
                cur.execute('''
                    INSERT INTO product_list (product_name, product_link, product_price, product_brand, product_category1, product_category2, product_category3, product_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (product_name, item.get('link', ''), item.get('lprice', ''), item.get('maker', ''),
                      item.get('category1', ''), item.get(
                          'category2', ''), item.get('category3', ''),
                      item.get('image', '')))
                db.commit()

        return items
    else:
        return {'error': 'No items found in the response'}


# 라우팅 함수 추가
@app.route('/search_text', methods=['POST'])
def search_text_route():
    query = request.form.get('query')
    text_results = search_text(query)

    return jsonify({'textResults': text_results})


# 이미지로 상품 검색
def search_image(image_file):
    # 이미지를 base64로 인코딩
    image_contents = base64.b64encode(image_file.read()).decode("utf8")

    # API 요청 데이터 설정
    request_json = {
        "argument": {
            "type": "jpg",
            "file": image_contents
        }
    }

    # 딜레이를 포함한 이미지 검출 API 호출
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8",
                 "Authorization": accessKey},
        body=json.dumps(request_json)
    )

    # API 응답을 JSON 형식으로 파싱
    response_data = response.data.decode('utf-8')
    result = json.loads(response_data)

    print("result = " + str(result))

    # 이미지 검출이 성공한 경우
    if 'result' in result and result['result'] == 0:
        objects = result['return_object']['data']

        object_info = [{'label': obj['class'],
                        'confidence': obj['confidence']} for obj in objects]

        highest_confidence_obj = max(
            object_info, key=lambda x: x['confidence'])
        highest_confidence_category = highest_confidence_obj['label']

        # Naver 검색 API 호출을 위한 URL 및 헤더 설정
        naver_search_url = f"https://openapi.naver.com/v1/search/shop?query={highest_confidence_category}"
        headers = {
            'X-Naver-Client-Id': naverClientId,
            'X-Naver-Client-Secret': naverClientSecret
        }
        params = {'display': 100}

        # 딜레이를 포함한 Naver 검색 API 호출
        time.sleep(1)  # 1초 딜레이
        naver_response = requests.get(
            naver_search_url, headers=headers, params=params)

        print("이미지 인식된 이름 = " + highest_confidence_category)
        print("[Naver Response Code] " + str(naver_response.status_code))
        print("[Naver Response Body]")
        print(naver_response.text)

        # Naver API 응답이 성공한 경우
        if naver_response.status_code == 200:
            naver_result = naver_response.json()
            combined_result = {
                'objects': object_info,
                'highest_confidence_category': highest_confidence_category,
                'naver_result': naver_result['items']
            }
            return combined_result
        else:
            return {'error': 'Naver API Error'}
    else:
        return {'error': result.get('return_object', {}).get('data', 'Unknown Error')}


# 이미지 검색 결과를 데이터베이스에 저장
def save_to_database(image_results):
    product_list = []  # 이미지 검색 결과에 대한 상품 정보를 저장할 리스트

    for item in image_results['naver_result']:
        product_name = remove_tags(item.get('title', ''))
        conn, cur = get_db()
        # 데이터 베이스에 같은 상품의 정보가 있는지 검색
        cur.execute(
            'SELECT * FROM product_list WHERE product_link = %s', (item.get('link', ''),))
        result = cur.fetchone()
        # 같은 상품이 없으면 저장
        if result is None:
            cur.execute('''
                INSERT INTO product_list (product_name, product_link, product_price, product_brand, product_category1, product_category2, product_category3, product_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (product_name, item.get('link', ''), item.get('lprice', ''), item.get('maker', ''),
                  item.get('category1', ''), item.get(
                      'category2', ''), item.get('category3', ''),
                  item.get('image', '')))
            conn.commit()

            # 새로 저장된 상품 정보를 가져와서 dictionary로 변환 후 리스트에 추가
            cur.execute(
                'SELECT * FROM product_list WHERE product_link = %s', (item.get('link', ''),))
            saved_product = dict(cur.fetchone())
            product_list.append(saved_product)

    return product_list


# 이미지 검색 결과를 데이터베이스에 저장
@app.route('/search_image', methods=['POST'])
def search_image_route():
    image_file = request.files['image']

    image_results = search_image(image_file)

    if 'naver_result' in image_results:
        saved_products = save_to_database(image_results)

        return jsonify({'imageResults': image_results, 'savedProducts': saved_products, 'message': '데이터가 성공적으로 데이터베이스에 저장되었습니다.'})
    else:
        return jsonify({'error': '이미지 결과에서 카테고리를 찾을 수 없습니다.'})


# 검색된 카테고리 목록 가져오기
@app.route('/get_categories', methods=['POST'])
def get_categories():
    image_file = request.files['image']

    # 이미지로 상품 검색하여 카테고리 목록 추출
    image_results = search_image(image_file)

    if 'naver_result' in image_results:
        categories = set()  # 중복을 허용하지 않는 집합으로 선언
        for item in image_results['naver_result']:
            # 각 아이템의 카테고리를 추출하여 집합에 추가
            categories.add(item.get('category1', ''))
            categories.add(item.get('category2', ''))
            categories.add(item.get('category3', ''))

        # 빈 문자열 제거
        categories.discard('')

        # Set을 List로 변환
        categories_list = list(categories)

        return jsonify({'categories': categories_list})
    else:
        return jsonify({'error': 'No categories found in the image results'})


# 로그인 및 회원가입 페이지 접속
@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        # 로그인
        if 'inId' in request.form:  # Sign-in form submitted
            inId = request.form['inId']
            inPw = request.form['inPw']

            # 커서 생성
            with app.app_context():
                db, cur = get_db()
                print("Connection and Cursor objects after get_db():", db, cur)
                g.user_table = user_table  # g 객체에 user_table 설정
                cursor = db.cursor()
                query = "SELECT * FROM %s WHERE id = %s AND password = %s" % (
                    user_table, '%s', '%s')

                cursor.execute(query, (inId, inPw))
                print("Executing query:", query)
                print("Parameters:", (inId, inPw))
                result = cursor.fetchone()

            if result:
                with app.app_context():
                    db, cur = get_db()
                    print("Connection and Cursor objects after get_db():", db, cur)
                    g.user_table = user_table  # g 객체에 user_table 설정
                    cursor = db.cursor()
                    name_query = "SELECT name FROM %s WHERE id = %s" % (
                        user_table, '%s')
                    cursor.execute(name_query, (inId,))
                    rsName = cursor.fetchone()

                if rsName:
                    session['user'] = rsName['name']

                    return redirect(url_for('index'))
                else:
                    # 예외 처리: 해당 ID에 대한 이름이 없을 때의 처리
                    return render_template('start.html')
            else:
                # 로그인 실패 시 플래시 메시지
                # 이 부분에 메인 페이지의 HTML 파일명을 넣어주세요
                return render_template('start.html', error_message='로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.')

        # 회원가입
        elif 'upId' in request.form:  # Sign-up form submitted
            upId = request.form.get('upId')
            upPw = request.form.get('upPw')
            upName = request.form.get('name')
            upEmail = request.form.get('email')
            upPhone = request.form.get('phone-num')

            # 필수 입력 필드에 대한 유효성 검사 추가
            if not all([upId, upPw, upName, upEmail, upPhone]):
                return render_template('start.html', error_message='모든 필수 입력 항목을 채워주세요.')

            # 이메일 형식 검사 (끝이 .com으로 끝나는지)
            if not upEmail.endswith('.com'):
                return render_template('start.html', error_message='올바른 이메일 형식이 아닙니다. (예: example@example.com)')

            # 전화번호 형식 검사 (숫자로 11자리 입력)
            upPhone_digits = ''.join(filter(str.isdigit, upPhone))
            if len(upPhone_digits) != 11:
                return render_template('start.html', error_message='올바른 전화번호 형식이 아닙니다. (숫자로 11자리 입력)')

            # 중복된 ID가 없으면 회원가입 처리
            with app.app_context():
                db, cur = get_db()
                g.user_table = user_table  # g 객체에 user_table 설정

                # 중복된 ID인지 확인
                cur.execute('SELECT * FROM %s WHERE id = %s' %
                            (user_table, '%s'), (upId,))
                existing_user = cur.fetchone()
                if existing_user:
                    return render_template('start.html', error_message='이미 존재하는 ID입니다.')

                # 중복된 ID가 없으면 회원가입 처리
                query = f"INSERT INTO {user_table} (id, password, name, email, phoneNumber) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query, (upId, upPw, upName,
                            upEmail, upPhone_digits))
                db.commit()

            return render_template('start.html', success_message='회원가입 성공!')
    return render_template('start.html')  # 이 부분에 메인 페이지의 HTML 파일명을 넣어주세요


@app.route('/logout')
def logout():
    if 'user' in session:
        # 세션에서 사용자 정보 삭제
        session.pop('user', None)
    return redirect('/')


@app.route('/index')
def index():
    if 'user' in session:
        username = session['user']
        return render_template('index.html', user=username)


if __name__ == '__main__':
    # 외부에서 접속 가능한 모든 IP 주소, 포트 5000으로 설정
    app.run(port=5000, debug=True, host='0.0.0.0')
