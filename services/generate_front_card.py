import os
from io import BytesIO
from fastapi import Form, HTTPException
from PIL import Image, ImageDraw, ImageFont

from schemas import Word
from core import FONT_FREESENTATION_DIR


def generate_front_card(word: Word, scale: float, image_format='png') -> BytesIO:
    """
    단어 카드 앞면을 생성하고 저장하는 함수

    Args:
        word (Word): 단어(spelling, level, meanings, examples)
        scale (float): 해상도 (기본값: 2.0)
        image_format (str): 이미지 포맷 (기본값: 'png')
    """

    width = int(1280 * scale)
    height = int(720 * scale)

    try:
        # 이미지 생성 (흰색 배경)
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        # 패딩 계산
        padding = int(60 * scale)
        content_width = width - (padding * 2)
        content_height = height - (padding * 2)

        # 폰트 크기 자동 조절을 위한 초기값
        initial_font_size = int(120 * scale)  # JavaScript의 360px를 120px로 조정
        min_font_size = int(10 * scale)

        # 메인 단어 폰트 크기 결정
        word_font_size = initial_font_size
        FONT_PATH = os.path.join(FONT_FREESENTATION_DIR, "Freesentation-9Black.ttf")
        word_font = None

        while word_font_size >= min_font_size:
            word_font = ImageFont.truetype(FONT_PATH, word_font_size)

            # 텍스트 크기 측정
            bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 텍스트가 컨테이너에 맞는지 확인
            if text_width <= content_width and text_height <= (content_height * 0.7):  # 70%만 사용
                break

            word_font_size -= int(5 * scale)

        # 단어 타입 폰트 설정
        type_font_size = int(30 * scale)
        type_font = ImageFont.truetype(FONT_PATH, type_font_size)

        # 메인 단어 그리기
        word_bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
        word_width = word_bbox[2] - word_bbox[0]
        word_height = word_bbox[3] - word_bbox[1]
        word_x = (width - word_width) // 2
        word_y = (height - word_height) // 2 - int(60 * scale)  # 약간 위로

        # 텍스트 그림자 효과 (간단한 오프셋)
        shadow_offset = int(2 * scale)
        draw.text((word_x + shadow_offset, word_y + shadow_offset),
                  word.spelling, font=word_font, fill=(200, 200, 200))  # 그림자
        draw.text((word_x, word_y), word.spelling, font=word_font, fill=(0, 0, 0))  # 메인 텍스트

        # 단어 타입 배경 (둥근 사각형) 그리기 - 유동적 너비, 고정 높이
        type_bbox = draw.textbbox((0, 0), word.level, font=type_font)
        type_text_width = type_bbox[2] - type_bbox[0]
        type_text_height = type_bbox[3] - type_bbox[1]

        # 1. height는 고정, width는 유동적
        type_bg_height = int(50 * scale)  # 고정 높이

        # 2. 현재 width를 최솟값으로 설정 (더 커질 수 있지만 작아질 수 없음)
        min_width = int(70 * scale)  # 기존 고정 너비가 최솟값
        padding_x = int(20 * scale)  # 좌우 여백
        calculated_width = type_text_width + (padding_x * 2)
        type_bg_width = max(min_width, calculated_width)  # 최솟값과 계산된 값 중 큰 값 선택

        type_bg_x = (width - type_bg_width) // 2
        type_bg_y = word_y + word_height + int(60 * scale)

        # 둥근 사각형 배경 그리기 (그라데이션 효과)
        corner_radius = int(25 * scale)  # 30에서 25로 조정 (찌그러짐 완화)

        # 그라데이션을 위한 별도 이미지 생성
        gradient_img = Image.new('RGB', (type_bg_width, type_bg_height), color='white')
        gradient_draw = ImageDraw.Draw(gradient_img)

        # 세로 그라데이션 생성 (#fbbf24 -> #f59e0b)
        start_color = (251, 191, 36)  # #fbbf24
        end_color = (245, 158, 11)  # #f59e0b

        for y in range(type_bg_height):
            # 그라데이션 비율 계산 (0.0 ~ 1.0)
            ratio = y / type_bg_height

            # 색상 보간
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)

            gradient_draw.line([(0, y), (type_bg_width, y)], fill=(r, g, b))

        # 마스크 생성 (둥근 사각형 모양)
        mask = Image.new('L', (type_bg_width, type_bg_height), 0)
        mask_draw = ImageDraw.Draw(mask)

        # 3. 찌그러짐 현상 개선을 위한 처리
        safe_radius = min(corner_radius, (type_bg_height // 2) - 2, (type_bg_width // 2) - 2)
        safe_radius = max(safe_radius, 1)  # 최소값 1 보장

        # 좌표 검증
        if type_bg_width <= 0 or type_bg_height <= 0:
            raise ValueError(f"Invalid dimensions: width={type_bg_width}, height={type_bg_height}")

        try:
            # rounded_rectangle의 좌표는 [x0, y0, x1, y1]에서 x1, y1은 exclusive
            # 즉, 실제 크기보다 1 적게 설정해야 함
            mask_draw.rounded_rectangle([0, 0, type_bg_width - 1, type_bg_height - 1],
                                        radius=safe_radius, fill=255)
        except Exception as e:
            print(f"[download_front_card ERROR] {e}")
            raise HTTPException(
                status_code=500,
                detail=f"이미지 생성 중 오류 발생: {str(e)}"
            )

        # 그라데이션 이미지를 메인 이미지에 붙여넣기
        img.paste(gradient_img, (type_bg_x, type_bg_y), mask)

        # 단어 타입 텍스트 그리기 (중앙 정렬)
        type_text_x = type_bg_x + (type_bg_width - type_text_width) // 2
        type_text_y = type_bg_y + int((type_bg_height - type_text_height) / 2.7)
        draw.text((type_text_x, type_text_y), word.level, font=type_font, fill='white')

        img_bytes = BytesIO()
        img.save(img_bytes, format=image_format.upper())  # PNG, JPG 등
        img_bytes.seek(0)

        return img_bytes

    except Exception as e:
        print(f"[download_front_card ERROR] {e}")
        raise HTTPException(
            status_code=500,
            detail=f"이미지 생성 중 오류 발생: {str(e)}"
        )
