# import os
# from io import BytesIO
# from typing import Dict, List
# from fastapi import Form, HTTPException
# from PIL import Image, ImageDraw, ImageFont
#
# from schemas import Word, Meaning, PartOfSpeech
# from core.config import FONT_FREESENTATION
#
#
# def generate_back_card(word: Word, scale: float, image_format='png'):
#     """
#     단어 카드 뒷면을 생성하고 저장하는 함수
#
#     Args:
#         word (WordBase): 단어(spelling, word_type, meanings, examples)
#         scale (float): 해상도 (기본값: 1.5)
#         image_format (str): 이미지 포맷 (기본값: 'png')
#     """
#
#     contents = convert_meanings_to_dict(word.meanings)
#     width = int(1280 * scale)
#     height = int(720 * scale)
#
#     try:
#         # 이미지 생성 (흰색 배경)
#         img = Image.new('RGB', (width, height), color='white')
#         draw = ImageDraw.Draw(img)
#
#         # 패딩 설정
#         padding = int(60 * scale)
#         content_width = width - (padding * 2)
#         content_height = height - (padding * 2)
#
#         # 폰트 설정
#         BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#         FONT_PATH = os.path.join(FONT_FREESENTATION, "Freesentation-9Black.ttf")
#
#         # 헤더 영역 높이 계산
#         header_height = int(200 * scale)
#         meanings_start_y = padding + header_height + int(40 * scale)  # 헤더 하단 여백
#
#         # === 헤더 영역 ===
#
#         # 메인 단어 폰트 크기 자동 조절
#         word_font_size = int(120 * scale)
#         min_font_size = int(20 * scale)
#         word_font = None
#
#         while word_font_size >= min_font_size:
#             word_font = ImageFont.truetype(FONT_PATH, word_font_size)
#             bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
#             text_width = bbox[2] - bbox[0]
#
#             if text_width <= content_width - int(40 * scale):  # 여백 고려
#                 break
#             word_font_size -= int(5 * scale)
#
#         # 메인 단어 그리기 (헤더 중앙 상단)
#         word_bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
#         word_width = word_bbox[2] - word_bbox[0]
#         word_height = word_bbox[3] - word_bbox[1]
#         word_x = (width - word_width) // 2
#         word_y = padding + int(20 * scale)
#
#         # 텍스트 그림자 효과
#         shadow_offset = int(2 * scale)
#         draw.text((word_x + shadow_offset, word_y + shadow_offset),
#                   word.spelling, font=word_font, fill=(200, 200, 200))
#         draw.text((word_x, word_y), word.spelling, font=word_font, fill=(0, 0, 0))
#
#         # === 의미 영역 ===
#         # 품사별 색상 매핑
#         pos_colors = {
#             PartOfSpeech.NOUN: (79, 70, 229),  # #4f46e5
#             PartOfSpeech.VERB: (16, 185, 129),  # #10b981
#             PartOfSpeech.ADJECTIVE: (245, 158, 11),  # #f59e0b
#             PartOfSpeech.ADVERB: (139, 92, 246),  # #8b5cf6
#             PartOfSpeech.PREPOSITION: (239, 68, 68)  # #ef4444
#         }
#
#         # 의미 항목 그리기
#         current_y = meanings_start_y
#         meaning_font_size = int(42 * scale)
#         # 단어 뜻용 폰트 (Freesentation-6SemiBold)
#         MEANING_FONT_PATH = os.path.join(FONT_FREESENTATION, "Freesentation-7Bold.ttf")
#         meaning_font = ImageFont.truetype(MEANING_FONT_PATH, meaning_font_size)
#         pos_font_size = int(28 * scale)
#         pos_font = ImageFont.truetype(FONT_PATH, pos_font_size)
#
#         print(f"시작 Y 위치: {meanings_start_y}, 화면 높이: {height}")
#
#         # 품사 태그 크기 설정 (정사각형)
#         pos_tag_size = int(45 * scale)
#         tag_spacing = int(20 * scale)  # 품사 태그와 뜻 사이 간격
#
#         # 품사 순서 정의
#         pos_order = [
#             PartOfSpeech.NOUN,
#             PartOfSpeech.VERB,
#             PartOfSpeech.ADJECTIVE,
#             PartOfSpeech.ADVERB,
#             PartOfSpeech.PRONOUN,
#             PartOfSpeech.PREPOSITION,
#             PartOfSpeech.CONJUNCTION,
#             PartOfSpeech.INTERJECTION
#         ]
#
#         # 가장 긴 의미의 너비 계산 (20글자 기준)
#         max_meaning_width = 0
#         meanings_dict = contents.get('contents', {})
#
#         # 정렬된 품사 리스트 생성 (존재하는 품사만)
#         sorted_meanings = [(pos, meanings_dict[pos]) for pos in pos_order if pos in meanings_dict]
#
#         char_limit = 20
#
#         for pos, definition in sorted_meanings:
#             definition_text = str(definition)
#
#             # 20글자 기준으로 첫 번째 줄 계산
#             current_line = ""
#             parts = definition_text.split(',')
#
#             for i, part in enumerate(parts):
#                 part = part.strip()
#                 if i < len(parts) - 1:
#                     part_with_comma = part + ','
#                 else:
#                     part_with_comma = part
#
#                 if current_line:
#                     test_line = current_line + ' ' + part_with_comma
#                 else:
#                     test_line = part_with_comma
#
#                 # 20글자를 넘으면 현재 줄로 확정
#                 if len(test_line) > char_limit and current_line:
#                     break
#                 else:
#                     current_line = test_line
#
#             # 첫 번째 줄의 실제 렌더링 너비 계산
#             if current_line:
#                 line_bbox = draw.textbbox((0, 0), current_line, font=meaning_font)
#                 line_width = line_bbox[2] - line_bbox[0]
#                 if line_width > max_meaning_width:
#                     max_meaning_width = line_width
#
#         # 가장 긴 의미를 중앙 정렬했을 때의 시작 x 좌표 계산
#         # 전체 요소 = 품사 태그 + 간격 + 의미 텍스트
#         total_width = pos_tag_size + tag_spacing + max_meaning_width
#         centered_start_x = (width - total_width) // 2
#
#         # 품사 태그의 시작 위치
#         pos_start_x = centered_start_x
#
#         for pos, definition in sorted_meanings:
#             # 품사의 첫 글자만 추출
#             pos_char = pos[0] if pos else '?'
#
#             pos_x = pos_start_x
#             pos_y = current_y
#
#             # 품사 태그 배경 (둥근 정사각형)
#             border_color = pos_colors.get(pos, (79, 70, 229))
#             pos_mask = Image.new('L', (pos_tag_size, pos_tag_size), 0)
#             pos_mask_draw = ImageDraw.Draw(pos_mask)
#             pos_radius = int(10 * scale)
#             pos_mask_draw.rounded_rectangle([0, 0, pos_tag_size - 1, pos_tag_size - 1],
#                                             radius=pos_radius, fill=255)
#
#             pos_bg_img = Image.new('RGB', (pos_tag_size, pos_tag_size), border_color)
#             img.paste(pos_bg_img, (pos_x, pos_y), pos_mask)
#
#             # 품사 텍스트 (중앙 정렬)
#             pos_bbox = draw.textbbox((0, 0), pos_char, font=pos_font)
#             pos_text_width = pos_bbox[2] - pos_bbox[0]
#             pos_text_height = pos_bbox[3] - pos_bbox[1]
#             pos_text_x = pos_x + (pos_tag_size - pos_text_width) // 2
#             pos_text_y = pos_y + int((pos_tag_size - pos_text_height) / 2.5)
#             draw.text((pos_text_x, pos_text_y), pos_char, font=pos_font, fill='white')
#
#             # 정의 텍스트 (품사 태그의 우측 끝에서 간격만큼 떨어진 위치)
#             definition_x = pos_x + pos_tag_size + tag_spacing
#             definition_y = pos_y + (pos_tag_size - meaning_font_size) // 3.5
#
#             # 정의 텍스트 길이 조절
#             max_def_width = width - definition_x - padding - int(20 * scale)
#             definition_text = str(definition)
#
#             # 글자 수로 줄바꿈 처리 (20글자 기준)
#             char_limit = 20
#             lines = []
#             current_line = ""
#             current_char_count = 0
#
#             # 쉼표로 구분된 각 뜻을 처리
#             parts = definition_text.split(',')
#
#             for i, part in enumerate(parts):
#                 part = part.strip()
#                 # 쉼표 추가 (마지막 항목 제외)
#                 if i < len(parts) - 1:
#                     part_with_comma = part + ','
#                 else:
#                     part_with_comma = part
#
#                 # 현재 줄에 추가했을 때의 글자 수 계산
#                 if current_line:
#                     test_line = current_line + ' ' + part_with_comma
#                     test_char_count = len(test_line)
#                 else:
#                     test_line = part_with_comma
#                     test_char_count = len(part_with_comma)
#
#                 # 20글자를 넘으면 새 줄로
#                 if test_char_count > char_limit and current_line:
#                     lines.append(current_line)
#                     current_line = part_with_comma
#                     current_char_count = len(part_with_comma)
#                 else:
#                     current_line = test_line
#                     current_char_count = test_char_count
#
#             # 마지막 줄 추가
#             if current_line:
#                 lines.append(current_line)
#
#             # 모든 줄 표시
#             line_height = meaning_font_size + int(8 * scale)
#             for line_idx, line in enumerate(lines):
#                 line_y = definition_y + (line_idx * line_height)
#                 draw.text((definition_x, line_y), line,
#                           font=meaning_font, fill=(0, 0, 0))
#
#             # 다음 품사 위치 계산 (마지막 줄 기준)
#             total_lines_height = len(lines) * line_height
#             if total_lines_height > pos_tag_size:
#                 current_y += total_lines_height + int(15 * scale)
#             else:
#                 current_y += pos_tag_size + int(15 * scale)
#
#             print(f"'{pos}' 품사 처리 완료. 다음 y 위치: {current_y}")
#
#         # 파일 저장
#         img_bytes = BytesIO()
#         img.save(img_bytes, format=image_format.upper())  # PNG, JPG 등
#         img_bytes.seek(0)
#
#         return img_bytes
#
#     except Exception as e:
#         print(f"[download_front_card ERROR] {e}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"이미지 생성 중 오류 발생: {str(e)}"
#         )
#
#
# def convert_meanings_to_dict(meanings: List[Meaning]):
#     max_length = 0
#     contents = {}
#
#     for m in meanings:
#         pos = m.part_of_speech
#         content = contents.get(pos, '')
#
#         if content:
#             definition = f'{content}, {m.definition}'
#         else:
#             definition = m.definition
#         contents[pos] = definition
#
#         length = len(definition)
#         if max_length < length:
#             max_length = length
#
#     d = {'max_length': max_length, 'contents': contents}
#     print(d)
#     return d

import os
from io import BytesIO
from typing import List
from fastapi import HTTPException
from PIL import Image, ImageDraw, ImageFont

from schemas import Word, Meaning, PartOfSpeech
from core import FONT_FREESENTATION_DIR


def generate_back_card(word: Word, scale: float, image_format='png'):
    """
    단어 카드 뒷면을 생성하고 저장하는 함수

    Args:
        word (WordBase): 단어(spelling, word_type, meanings, examples)
        scale (float): 해상도 (기본값: 2.0)
        image_format (str): 이미지 포맷 (기본값: 'png')
    """

    contents = convert_meanings_to_dict(word.meanings)
    width = int(1280 * scale)
    height = int(720 * scale)

    try:
        # 이미지 생성 (흰색 배경)
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        # 패딩 설정
        padding = int(60 * scale)
        content_width = width - (padding * 2)
        content_height = height - (padding * 2)

        # 폰트 설정
        FONT_PATH = os.path.join(FONT_FREESENTATION_DIR, "Freesentation-9Black.ttf")

        # 헤더 영역 높이 계산
        header_height = int(200 * scale)
        meanings_start_y = padding + header_height + int(40 * scale)  # 헤더 하단 여백

        # === 헤더 영역 ===

        # 메인 단어 폰트 크기 자동 조절
        word_font_size = int(120 * scale)
        min_font_size = int(20 * scale)
        word_font = None

        while word_font_size >= min_font_size:
            word_font = ImageFont.truetype(FONT_PATH, word_font_size)
            bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
            text_width = bbox[2] - bbox[0]

            if text_width <= content_width - int(40 * scale):  # 여백 고려
                break
            word_font_size -= int(5 * scale)

        # 메인 단어 그리기 (헤더 중앙 상단)
        word_bbox = draw.textbbox((0, 0), word.spelling, font=word_font)
        word_width = word_bbox[2] - word_bbox[0]
        word_height = word_bbox[3] - word_bbox[1]
        word_x = (width - word_width) // 2
        word_y = padding + int(20 * scale)

        # 텍스트 그림자 효과
        shadow_offset = int(2 * scale)
        draw.text((word_x + shadow_offset, word_y + shadow_offset),
                  word.spelling, font=word_font, fill=(200, 200, 200))
        draw.text((word_x, word_y), word.spelling, font=word_font, fill=(0, 0, 0))

        # === 의미 영역 ===
        # 품사별 색상 매핑
        pos_colors = {
            PartOfSpeech.NOUN: (239, 68, 68),  # #ef4444 - 빨강 (가장 흔한 품사)
            PartOfSpeech.VERB: (236, 72, 153),  # #ec4899 - 핑크
            PartOfSpeech.ADJECTIVE: (245, 158, 11),  # #f59e0b - 노랑/주황
            PartOfSpeech.ADVERB: (79, 70, 229),  # #4f46e5 - 파랑
            PartOfSpeech.PRONOUN: (139, 92, 246),  # #8b5cf6 - 보라
            PartOfSpeech.PREPOSITION: (16, 185, 129),  # #10b981 - 에메랄드
            PartOfSpeech.CONJUNCTION: (251, 146, 60),  # #fb923c - 오렌지
            PartOfSpeech.INTERJECTION: (6, 182, 212)  # #06b6d4 - 민트
        }

        # 의미 항목 그리기
        current_y = meanings_start_y
        meaning_font_size = int(42 * scale)
        # 단어 뜻용 폰트 (Freesentation-6SemiBold)
        MEANING_FONT_PATH = os.path.join(FONT_FREESENTATION_DIR, "Freesentation-7Bold.ttf")
        meaning_font = ImageFont.truetype(MEANING_FONT_PATH, meaning_font_size)
        pos_font_size = int(28 * scale)
        pos_font = ImageFont.truetype(FONT_PATH, pos_font_size)

        # 품사 태그 크기 설정 (정사각형)
        pos_tag_size = int(45 * scale)
        tag_spacing = int(20 * scale)  # 품사 태그와 뜻 사이 간격

        # 품사 순서 정의
        pos_order = [
            PartOfSpeech.NOUN,
            PartOfSpeech.VERB,
            PartOfSpeech.ADJECTIVE,
            PartOfSpeech.ADVERB,
            PartOfSpeech.PREPOSITION,
            PartOfSpeech.PRONOUN,
            PartOfSpeech.CONJUNCTION,
            PartOfSpeech.INTERJECTION
        ]

        # 가장 긴 의미의 너비 계산 (20글자 기준)
        max_meaning_width = 0
        meanings_dict = contents.get('contents', {})

        # 정렬된 품사 리스트 생성 (존재하는 품사만)
        sorted_meanings = [(pos, meanings_dict[pos]) for pos in pos_order if pos in meanings_dict]

        # 품사가 5개를 넘으면 PRONOUN, CONJUNCTION, INTERJECTION 제외
        if len(sorted_meanings) > 6:
            exclude_pos = {PartOfSpeech.CONJUNCTION, PartOfSpeech.INTERJECTION}
            sorted_meanings = [(pos, meaning) for pos, meaning in sorted_meanings if pos not in exclude_pos]

        char_limit = 20

        for pos, definition in sorted_meanings:
            definition_text = str(definition)

            # 20글자 기준으로 첫 번째 줄 계산
            current_line = ""
            parts = definition_text.split(',')

            for i, part in enumerate(parts):
                part = part.strip()
                if i < len(parts) - 1:
                    part_with_comma = part + ','
                else:
                    part_with_comma = part

                if current_line:
                    test_line = current_line + ' ' + part_with_comma
                else:
                    test_line = part_with_comma

                # 20글자를 넘으면 현재 줄로 확정
                if len(test_line) > char_limit and current_line:
                    break
                else:
                    current_line = test_line

            # 첫 번째 줄의 실제 렌더링 너비 계산
            if current_line:
                line_bbox = draw.textbbox((0, 0), current_line, font=meaning_font)
                line_width = line_bbox[2] - line_bbox[0]
                if line_width > max_meaning_width:
                    max_meaning_width = line_width

        # 가장 긴 의미를 중앙 정렬했을 때의 시작 x 좌표 계산
        # 전체 요소 = 품사 태그 + 간격 + 의미 텍스트
        total_width = pos_tag_size + tag_spacing + max_meaning_width
        centered_start_x = (width - total_width) // 2

        # 품사 태그의 시작 위치
        pos_start_x = centered_start_x

        for pos, definition in sorted_meanings:
            # 품사의 첫 글자만 추출
            pos_char = pos[0] if pos else '?'

            pos_x = pos_start_x
            pos_y = current_y

            # 품사 태그 배경 (둥근 정사각형)
            border_color = pos_colors.get(pos, (79, 70, 229))
            pos_mask = Image.new('L', (pos_tag_size, pos_tag_size), 0)
            pos_mask_draw = ImageDraw.Draw(pos_mask)
            pos_radius = int(10 * scale)
            pos_mask_draw.rounded_rectangle([0, 0, pos_tag_size - 1, pos_tag_size - 1],
                                            radius=pos_radius, fill=255)

            pos_bg_img = Image.new('RGB', (pos_tag_size, pos_tag_size), border_color)
            img.paste(pos_bg_img, (pos_x, pos_y), pos_mask)

            # 품사 텍스트 (중앙 정렬)
            pos_bbox = draw.textbbox((0, 0), pos_char, font=pos_font)
            pos_text_width = pos_bbox[2] - pos_bbox[0]
            pos_text_height = pos_bbox[3] - pos_bbox[1]
            pos_text_x = pos_x + (pos_tag_size - pos_text_width) // 2
            # pos_text_y = pos_y + int((pos_tag_size - pos_text_height) / 2.5)
            pos_text_y = pos_y + int((pos_tag_size - pos_text_height) / 3)
            draw.text((pos_text_x, pos_text_y), pos_char, font=pos_font, fill='white')

            # 정의 텍스트 (품사 태그의 우측 끝에서 간격만큼 떨어진 위치)
            definition_x = pos_x + pos_tag_size + tag_spacing
            definition_y = pos_y + (pos_tag_size - meaning_font_size) // 3.5 - 3 * (scale - (0.5 if scale == 1 else 0))

            # 정의 텍스트 길이 조절
            max_def_width = width - definition_x - padding - int(20 * scale)
            definition_text = str(definition)

            # 글자 수로 줄바꿈 처리 (20글자 기준)
            char_limit = 20
            lines = []
            current_line = ""
            current_char_count = 0

            # 쉼표로 구분된 각 뜻을 처리
            parts = definition_text.split(',')

            for i, part in enumerate(parts):
                part = part.strip()
                # 쉼표 추가 (마지막 항목 제외)
                if i < len(parts) - 1:
                    part_with_comma = part + ','
                else:
                    part_with_comma = part

                # 현재 줄에 추가했을 때의 글자 수 계산
                if current_line:
                    test_line = current_line + ' ' + part_with_comma
                    test_char_count = len(test_line)
                else:
                    test_line = part_with_comma
                    test_char_count = len(part_with_comma)

                # 20글자를 넘으면 새 줄로
                if test_char_count > char_limit and current_line:
                    lines.append(current_line)
                    current_line = part_with_comma
                    current_char_count = len(part_with_comma)
                else:
                    current_line = test_line
                    current_char_count = test_char_count

            # 마지막 줄 추가
            if current_line:
                lines.append(current_line)

            # 모든 줄 표시
            line_height = meaning_font_size + int(8 * scale)
            for line_idx, line in enumerate(lines):
                line_y = definition_y + (line_idx * line_height)
                draw.text((definition_x, line_y), line,
                          font=meaning_font, fill=(0, 0, 0))

            # 다음 품사 위치 계산 (마지막 줄 기준)
            total_lines_height = len(lines) * line_height
            if total_lines_height > pos_tag_size:
                current_y += total_lines_height + int(15 * scale)
            else:
                current_y += pos_tag_size + int(15 * scale)

        # 파일 저장
        img_bytes = BytesIO()
        img.save(img_bytes, format=image_format.upper())  # PNG, JPG 등
        img_bytes.seek(0)

        return img_bytes

    except Exception as e:
        print(f"[download_back_card ERROR] {e}")
        raise HTTPException(
            status_code=500,
            detail=f"이미지 생성 중 오류 발생: {str(e)}"
        )


def convert_meanings_to_dict(meanings: List[Meaning]):
    max_length = 0
    contents = {}

    for m in meanings:
        pos = m.part_of_speech
        content = contents.get(pos, '')

        if content:
            definition = f'{content}, {m.definition}'
        else:
            definition = m.definition
        contents[pos] = definition

        length = len(definition)
        if max_length < length:
            max_length = length

    d = {'max_length': max_length, 'contents': contents}
    return d
