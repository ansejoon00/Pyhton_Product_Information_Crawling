window.onload = function () {
    fetch('/get_categories')
        .then(response => response.json())
        .then(data => {
            var categorySelect = document.getElementById('categorySelect');
            data.categories.forEach(category => {
                var option = document.createElement('option');
                option.value = category;
                option.text = category;
                categorySelect.add(option);
            });
        })
        .catch(error => {
            console.error('에러:', error);
        });
};

function handleKeyDown(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // 엔터 키의 기본 동작 방지 (폼 제출 방지)
        searchText();
    }
}

function searchText() {
    var query = document.getElementById('textQuery').value;
    var formData = new FormData(document.getElementById('textSearchForm'));
    search('search_text', formData, 'text');
}

function displaySelectedImage() {
    var imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = '';

    var selectedImage = document.getElementById('image').files[0];

    // 파일이 선택되었는지 확인
    if (selectedImage) {
        var img = document.createElement('img');
        img.src = URL.createObjectURL(selectedImage);
        img.width = 300;
        imageContainer.appendChild(img);
    } else {
        console.error('이미지 파일을 찾을 수 없습니다.');
    }

    console.log('displaySelectedImage 함수 실행됨');
}

function detectAndSearch() {
    var formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);
    search('search_image', formData, 'result');
}

// 검색 결과를 선택된 카테고리로 필터링하는 함수
function filterByCategory() {
    var selectedCategory = document.getElementById('categorySelect').value;
    var formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);

    fetch('/search_image', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            var resultElement = document.getElementById('result');
            resultElement.innerHTML = '';  // 기존 내용 초기화

            if ('naver_result' in data.imageResults) {
                data.imageResults.naver_result.forEach(item => {
                    // 선택된 카테고리와 일치하는 경우에만 결과를 표시
                    if (!selectedCategory || item.category1 === selectedCategory || item.category2 === selectedCategory || item.category3 === selectedCategory) {
                        var li = document.createElement('li');
                        li.innerHTML = '<img src="' + item.image + '" width="200" height="200">' + '<br>' +
                            '<a href="' + item.link + '">' + item.title + '</a><br>' +
                            '<p>가격: ' + (item.lprice || '정보 없음') + '</p>' +
                            '<p>브랜드: ' + (item.brand || '정보 없음') + '</p>' +
                            '<p>카테고리: ' + (item.category1 || '') + ' > ' + (item.category2 || '') + ' > ' + (item.category3 || '') + '</p>';
                        resultElement.appendChild(li);
                    }
                });
            }
        })
        .catch(error => {
            console.error('에러:', error);
        });
}

function displayPagination(totalPages, currentPage) {
    var paginationElement = document.getElementById("pagination");
    paginationElement.innerHTML = "";

    for (var i = 1; i <= totalPages; i++) {
        var button = document.createElement("button");
        button.innerText = i;
        if (i === currentPage) {
            button.classList.add("active");
        }
        button.addEventListener("click", function () {
            searchText(this.innerText);
        });
        paginationElement.appendChild(button);
    }
}

function search(route, data, resultId) {
    fetch('/' + route, {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
        .then(data => {
            var resultElement = document.getElementById(resultId);
            resultElement.innerHTML = '';  // 기존 내용 초기화

            if ('textResults' in data) {
                var resultContainer = document.createElement('div');
                resultContainer.className = 'result-container';
                data.textResults.forEach(item => {
                    var resultBox = createResultBox(item);
                    resultContainer.appendChild(resultBox);
                });
                resultElement.appendChild(resultContainer);
            }

            if ('imageResults' in data) {
                var resultContainer = document.createElement('div');
                resultContainer.className = 'result-container';
                data.imageResults.naver_result.forEach(item => {
                    var resultBox = createResultBox(item);
                    resultContainer.appendChild(resultBox);
                });
                resultElement.appendChild(resultContainer);
            }
        })
        .catch(error => {
            console.error('에러:', error);
        });
}

// 각 상품 요소를 생성하는 함수
function createResultBox(item) {
    var resultBox = document.createElement('div');
    resultBox.className = 'result-box';

    // 이미지와 정보를 담을 div 추가
    var productInfo = document.createElement('div');
    productInfo.className = 'product-info';

    // 이미지 추가
    var img = document.createElement('img');
    img.src = item.image;
    img.width = 200;
    img.height = 200;

    // 정보 추가
    var info = document.createElement('div');
    info.innerHTML =
        '<a class="product-link" target="_blank" href="' + item.link + '">' + item.title + '</a>' +
        '<p>가격: ' + (item.lprice || '정보 없음') + '</p>' +
        '<p>브랜드: ' + (item.brand || '정보 없음') + '</p>' +
        '<p>카테고리: ' + (item.category1 || '') + ' > ' + (item.category2 || '') + ' > ' + (item.category3 || '') + '</p>';

    // 각각의 div를 상위 div에 추가
    productInfo.appendChild(img);
    productInfo.appendChild(info);

    // 상위 div를 결과에 추가
    resultBox.appendChild(productInfo);

    return resultBox;
}
// 이미지 불러오기
function triggerImageInputClick() {
    document.getElementById('image').click();
}