from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from io import BytesIO
import time

from starlette.responses import JSONResponse

from schemas import WordBase


def generate_front_card(word: WordBase, resolution: str = Form(...)):
    print(word)
    if resolution == "HD":
        scale = 1
    elif resolution == "FHD":
        scale = 1.5
    else:
        scale = 2.0

    width = int(1280 * scale)
    height = int(720 * scale)

    # 1️⃣ Chrome 옵션 설정
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        driver.execute_script(f"""
            const wordEl = document.querySelector('.word');
            let fontSize = 120 * {scale};
            wordEl.style.fontSize = fontSize + 'px';
    
            while ((wordEl.scrollWidth > wordEl.parentElement.clientWidth || wordEl.scrollHeight > wordEl.parentElement.clientHeight) && fontSize > 10) {{
                fontSize -= 5;
                wordEl.style.fontSize = fontSize + 'px';
            }}
            """)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
    print('css 작성')
    try:
        # 2️⃣ HTML + CSS 작성
        html = f"""
        <html>
        <head>
            <style>
            .virtual-card {{
                width: {width}px;
                height: {height}px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 60px;
                background: white;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                box-sizing: border-box;
            }}
            .virtual-card .word {{
                font-size: 120px;
                font-weight: 900;
                color: #1e293b;
                margin-bottom: 30px;
                text-shadow: 0 4px 8px rgba(0,0,0,0.1);
                white-space: nowrap;
            }}
            .virtual-card .type {{
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
                color: white;
                border-radius: 60px;
                font-size: 48px;
                font-weight: 700;
            }}
            </style>
        </head>
        <body>
            <div class="virtual-card">
                <div class="word">{word.spelling}</div>
                <div class="type">{word.wordType}</div>
            </div>
        </body>
        </html>
        """

        # 3️⃣ HTML 렌더링
        driver.get("data:text/html;charset=utf-8," + html)
        time.sleep(0.5)  # 렌더링 대기

        # 4️⃣ 카드 요소 스크린샷
        card_element = driver.find_element("css selector", ".virtual-card")
        png_bytes = card_element.screenshot_as_png

        # 5️⃣ BytesIO에 저장
        buf = BytesIO(png_bytes)
        buf.seek(0)

        # 6️⃣ StreamingResponse 반환
        return StreamingResponse(buf, media_type="image/png", headers={
            "Content-Disposition": f"inline; filename={word.spelling}_card.png"
        })

    except Exception as e:
        print('형 갔다~')
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        driver.quit()
