# Product Information Crawling
> **네이버 상품 API를 이용하여 텍스트 및 이미지를 사용해 상품 검색을 할 수 있는 웹 개발**

<div align="center">
<img width="143" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/8546996b-d978-4167-9ae8-89806792e65f">
<div align="left">

---

## 프로젝트 소개
> 로그인 기능을 통해 **보안성**을 높이고 관리자가 회원관리를 할 수 있게 하여 API 제한을 확인함.

> **텍스트 및 이미지** 두 가지 매체를 통해 검색할 수 있게 설계함.

## Stacks 🐈

### Environment
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)
![LINUX](https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

### Data Base
![MYSQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

### Development
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26.svg?&style=for-the-badge&logo=HTML5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6.svg?&style=for-the-badge&logo=CSS3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScriipt-F7DF1E.svg?&style=for-the-badge&logo=JavaScript&logoColor=black)

### Communication
![KakaoTalk](https://img.shields.io/badge/Kakao_Talk-FFCD00?style=for-the-badge&logo=kakaotalk&logoColor=black)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)

---
## 화면 구성 📺
<div align="center">

| 로그인 페이지 | 회원가입 페이지 |  
| :-------------------------------------------: | :------------: |
| <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/c2dd0de0-7977-4fc4-a251-c6ece116a193"> | <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/1060dcc5-f9b6-4120-ab72-094b1bc389a8"> |
| 텍스트 검색 페이지 | 이미지 검색 페이지 |  
| <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/bedb98f4-2a5e-4a1b-93c2-7aa1ee7837b4"> | <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/a3bda27c-51cd-4f7d-92ca-c5abcfb9a044"> |
| 회원 DB | 검색 시 코드 |
| <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/0d493256-b873-43b5-a8e2-5a9caca75504"> | <img width="400" alt="image" src="https://github.com/ansejoon00/Python_Product_Information_Crawling/assets/156414896/94ec8fd3-7756-4497-b1ad-da34997b34f9"> |

<div align="left">

---
## 아키텍처

### 디렉터리 구조
```bash
├── static
│   ├── css
│   │   ├── index.css
│   │   └── start.css
│   │ 
│   ├── image
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   ├── image3.jpg
│   │   ├── image4.jpg
│   │   ├── image5.jpg
│   │   └── logo.jpg
│   │  
│   └── js
│       └── index.js
│
├── templates
│   ├── index.html
│   └── start.html
│
├── Flow_Chart-Product Information Crawling.png : 순서도
│
├── README.md : 리드미 파일
│
├── app_Ubuntu.py : Linux인 Ubuntu에 보관하고 Linux에서 실행 시 외부에서 접속할 수 있게 한 Code 
│
└── app_Window.py : Window 상에서 실행시키고 외부 IP를 이용해 외부 DB와 연결해서 사용하게 한 Code
