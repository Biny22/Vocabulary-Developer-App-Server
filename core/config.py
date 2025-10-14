from pathlib import Path

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 폰트 경로
FONTS_DIR = BASE_DIR / "fonts"
FONT_FREESENTATION_DIR = FONTS_DIR / "freesentation"


# 단어 템플릿 경로
TEMPLATES_DIR = BASE_DIR / "protected" / "templates"
WORD_TEMPLATE_FILE = TEMPLATES_DIR / "word_template.xlsx"


# 템플릿 업로드 경로
TEMPLATE_UPLOAD_DIR = BASE_DIR / "template_uploads"
TEMPLATE_UPLOAD_DIR.mkdir(exist_ok=True)
