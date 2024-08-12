import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
from threading import Thread
import datetime
import sys

# 글로벌 변수
tokens = []  # 여러 개의 토큰을 저장할 리스트
current_token_index = 0  # 현재 사용 중인 토큰의 인덱스
band_key = ""
comment_text = ""  # 사용자가 입력한 댓글 내용을 저장할 변수
commented_post_keys = []
call_count = 0  # 현재 토큰의 호출 횟수를 추적하기 위한 변수
MAX_CALLS_PER_TOKEN = 1000  # 각 토큰의 최대 호출 횟수
CALL_DELAY = 3  # <<=========== 호출 간 딜레이 조절하는 변수

# 표준 출력을 텍스트 위젯에 리다이렉트하는 클래스
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):  # flush 메서드가 필요할 수 있음
        pass

# 밴드 목록을 가져오는 함수
def get_band_list():
    global tokens, current_token_index
    url = "https://openapi.band.us/v2.1/bands"
    headers = {
        "Authorization": f"Bearer {tokens[current_token_index]}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('result_data', {}).get('bands', [])
    else:
        messagebox.showerror("Error", f"밴드 목록을 가져오지 못했습니다: {response.status_code}")
        return []

# 최신 포스트 키를 가져오는 함수
def get_latest_post_key():
    global tokens, current_token_index
    url = "https://openapi.band.us/v2/band/posts"
    headers = {
        "Authorization": f"Bearer {tokens[current_token_index]}"
    }
    params = {
        "band_key": band_key,
        "locale": "ko_KR",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        latest_post_key = data.get('result_data', {}).get('items', [])[0].get('post_key', None)
        return latest_post_key
    else:
        print(f"포스트 키를 가져오지 못했습니다: {response.status_code}")
        return None

# 댓글을 작성하는 함수
def post_comment(post_key):
    global tokens, current_token_index, comment_text
    url = "https://openapi.band.us/v2/band/post/comment/create"
    headers = {
        "Authorization": f"Bearer {tokens[current_token_index]}"
    }
    data = {
        "band_key": band_key,
        "post_key": post_key,
        "body": comment_text  # 사용자가 입력한 댓글 내용 사용
    }
    response = requests.post(url, headers=headers, data=data)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        print(f"[{current_time}] 댓글 작성 성공! (post_key: {post_key})")
        commented_post_keys.append(post_key)
    else:
        print(f"[{current_time}] 댓글 작성 실패: {response.status_code}, {response.text}")

# 토큰을 변경하는 함수
def switch_token():
    global current_token_index, call_count
    if current_token_index < len(tokens) - 1:
        current_token_index += 1
        call_count = 0
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] 토큰이 변경되었습니다. 새로운 토큰으로 전환: {current_token_index + 1}번째 토큰 사용 중")
    else:
        print("모든 토큰을 사용했습니다. 더 이상 호출할 수 없습니다.")
        messagebox.showinfo("Info", "모든 토큰이 사용되었습니다. 프로그램이 종료됩니다.")
        root.quit()

# 자동 댓글을 시작하는 함수
def start_commenting():
    global call_count
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{start_time}] 프로그램이 시작되었습니다.")
    try:
        last_post_key = get_latest_post_key()
        while True:
            try:
                latest_post_key = get_latest_post_key()
                if latest_post_key != last_post_key and latest_post_key not in commented_post_keys:
                    post_comment(latest_post_key)
                    last_post_key = latest_post_key

                call_count += 1

                if call_count >= MAX_CALLS_PER_TOKEN:  # 현재 토큰이 최대 호출 횟수에 도달하면
                    switch_token()

                time.sleep(CALL_DELAY)  # 호출 간 0.1초 대기
            except Exception as e:
                print(f"오류 발생: {e}. 다음 토큰으로 전환합니다.")
                switch_token()
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] 프로그램 오류로 종료되었습니다: {e}")

# 댓글 작성 버튼이 클릭되었을 때 호출되는 함수
def on_start():
    global band_key, comment_text
    band_name = band_listbox.get(tk.ACTIVE)
    comment_text = comment_entry.get()  # 사용자가 입력한 댓글 내용을 가져옴
    
    if not tokens or not band_name or not comment_text:
        messagebox.showwarning("Warning", "토큰, 밴드, 댓글 내용을 모두 입력해주세요.")
        return

    selected_band = next((band for band in bands if band['name'] == band_name), None)
    if selected_band:
        band_key = selected_band['band_key']
        Thread(target=start_commenting, daemon=True).start()
        messagebox.showinfo("Info", "자동 댓글이 시작되었습니다.")

# 토큰 제출 버튼이 클릭되었을 때 호출되는 함수
def on_token_submit():
    global tokens
    tokens = [entry.get().strip() for entry in token_entries if entry.get().strip()]
    
    if not tokens:
        messagebox.showwarning("Warning", "모든 토큰을 입력해주세요.")
        return
    
    global bands
    bands = get_band_list()
    
    if bands:
        band_listbox.delete(0, tk.END)
        for band in bands:
            band_listbox.insert(tk.END, band['name'])
    else:
        messagebox.showwarning("Warning", "밴드를 불러오지 못했습니다.")

# GUI 생성
root = tk.Tk()
root.title("밴드 자동 댓글 프로그램")

# 토큰 입력 라벨과 5개의 입력 창
tk.Label(root, text="Access Tokens:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

token_entries = []
for i in range(5):
    entry = tk.Entry(root, width=50)
    entry.grid(row=i + 1, column=0, padx=10, pady=5)
    token_entries.append(entry)

# 댓글 내용 입력 라벨과 입력 창
tk.Label(root, text="Comment Text:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
comment_entry = tk.Entry(root, width=50)
comment_entry.grid(row=7, column=0, padx=10, pady=5)

# 토큰 제출 버튼
token_submit_btn = tk.Button(root, text="Submit Tokens", command=on_token_submit)
token_submit_btn.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="n")

# 밴드 목록 표시 라벨과 리스트 박스
tk.Label(root, text="Select Band:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
band_listbox = tk.Listbox(root, height=10, width=50)
band_listbox.grid(row=9, column=0, padx=10, pady=10)

# 자동 댓글 시작 버튼
start_btn = tk.Button(root, text="Start Commenting", command=on_start)
start_btn.grid(row=10, column=0, padx=10, pady=10)

# 터미널 출력을 표시할 텍스트 위젯
output_text = tk.Text(root, height=15, width=80)
output_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# 표준 출력을 텍스트 위젯으로 리다이렉트
sys.stdout = StdoutRedirector(output_text)

root.mainloop()
