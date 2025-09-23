# url = "http://127.0.0.1:8000/generate/media"
#
# json_data = {
#     "spelling": "Apple",
#     "type": "초등",
#     "meanings": {"n": "사과"},
#     "examples": {"시험1": "I eat an apple."}
# }
#
# params = {
#     "audio_toggle": True,
#     "resolution": "FHD"
# }
#
# response = requests.post(url, json=json_data, params=params)
#
# with open("Apple.zip", "wb") as f:
#     f.write(response.content)