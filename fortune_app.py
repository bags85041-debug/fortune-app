import os
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)

def ask_ai(prompt):
    """AI에게 질문하고 응답 반환"""
    res = client.messages.create(
        model="claude-haiku",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text

class FortuneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 나의 운세 & 별자리 앱 🌟")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # 12개 별자리
        self.zodiac_signs = [
            "양자리 ♈", "황소자리 ♉", "쌍둥이자리 ♊", "게자리 ♋",
            "사자자리 ♌", "처녀자리 ♍", "천칭자리 ♎", "전갈자리 ♏",
            "궁수자리 ♐", "염소자리 ♑", "물병자리 ♒", "물고기자리 ♓"
        ]

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 제목
        title_label = tk.Label(
            self.root,
            text="🌟 나의 운세 & 별자리 앱 🌟",
            font=("Arial", 18, "bold"),
            fg="#FF6B9D"
        )
        title_label.pack(pady=20)

        # 입력 폼 프레임
        form_frame = ttk.Frame(self.root)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # 이름 입력
        ttk.Label(form_frame, text="👤 이름:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        self.name_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10)

        # 생년월일 입력
        ttk.Label(form_frame, text="📅 생년월일:", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=10)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=("Arial", 9), foreground="gray").grid(row=1, column=1, sticky="w", padx=10)
        self.birth_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.birth_entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # 별자리 선택
        ttk.Label(form_frame, text="⭐ 별자리 선택:", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=10)
        self.zodiac_var = tk.StringVar(value=self.zodiac_signs[0])
        zodiac_combo = ttk.Combobox(
            form_frame,
            textvariable=self.zodiac_var,
            values=self.zodiac_signs,
            state="readonly",
            font=("Arial", 10),
            width=27
        )
        zodiac_combo.grid(row=3, column=1, sticky="ew", padx=10)

        # 운세 보기 버튼
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        self.fortune_button = ttk.Button(
            button_frame,
            text="🔮 운세 보기",
            command=self.show_fortune
        )
        self.fortune_button.pack(ipady=10, ipadx=20)

        # 운세 결과 표시
        ttk.Label(self.root, text="오늘의 운세:", font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 5))

        self.result_text = tk.Text(
            self.root,
            height=10,
            width=55,
            font=("Arial", 10),
            wrap="word",
            bg="#FFF8F0",
            border=2,
            relief="solid"
        )
        self.result_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        self.result_text.config(state="disabled")

    def show_fortune(self):
        """운세 보기 버튼 클릭 시"""
        # 입력값 검증
        name = self.name_entry.get().strip()
        birth = self.birth_entry.get().strip()
        zodiac = self.zodiac_var.get()

        if not name:
            messagebox.showwarning("입력 오류", "이름을 입력해주세요!")
            return

        if not birth:
            messagebox.showwarning("입력 오류", "생년월일을 입력해주세요! (YYYY-MM-DD)")
            return

        # 생년월일 형식 검증
        try:
            from datetime import datetime
            datetime.strptime(birth, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("입력 오류", "생년월일 형식이 올바르지 않습니다.\n(예: 1995-05-15)")
            return

        # 버튼 비활성화 (로딩 중)
        self.fortune_button.config(state="disabled")
        self.fortune_button.config(text="⏳ 운세를 읽고 있습니다...")
        self.root.update()

        try:
            # AI 호출
            prompt = f"""사용자의 정보:
- 이름: {name}
- 생년월일: {birth}
- 별자리: {zodiac}

위 정보를 바탕으로 오늘의 운세를 4~5줄로 작성해줘.
- 밝고 친근한 말투로 작성
- 사용자가 재미있게 읽을 수 있도록 긍정적이고 격려하는 내용
- 일상 생활에서 도움이 될 만한 조언 포함
- 별자리의 특징을 반영하되, 너무 무겁지 않게"""

            fortune_text = ask_ai(prompt)

            # 결과 표시
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, fortune_text)
            self.result_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("오류", f"운세를 가져오는 중 오류가 발생했습니다:\n{str(e)}")

        finally:
            # 버튼 활성화
            self.fortune_button.config(state="normal")
            self.fortune_button.config(text="🔮 운세 보기")

def main():
    root = tk.Tk()
    app = FortuneApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
