from typing import List, Optional

input_path = "input.txt"
output_path = "output.txt"


class AutomataState:
    INITIAL = 0
    CONSONANT_1 = 1
    CONSONANT_2 = 2
    VOWEL_1 = 3
    VOWEL_2 = 4
    VOWEL_3 = 5
    FINAL_1 = 6
    FINAL_2 = 7

    ERROR = 9


class KoreanAutomata:
    def __init__(self):
        self.state = AutomataState.INITIAL
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self, path: str) -> List[str]:
        # 데이터를 불러온 뒤 유니코드로 변환
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        data_list = data.split("\n")

        return data_list

    def save_data(self, path: str, data: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    def combine_buffer(self, buffer: List[str]) -> str:
        # 여기 들어오기 전에 합칠 수 있는거는 합쳐서 보내는걸로하기
        #  [{(초성)×588}+{(중성)×28}+(종성)]+44032
        if self.state == AutomataState.ERROR:
            # 에러일 때는 초성 또는 중성만 들어온다. 즉 한글자만 들어온다
            # 합칠필요도 딱히 없으니 바로 리턴하면됨
            retunring = buffer[0]
            buffer.clear()
            return retunring
        initial = FIRST.index(buffer[0])
        vowel = MIDDLE.index(buffer[1])
        jongsung = FINAL.index(buffer[2]) if len(buffer) == 3 else 0
        combined_korean = chr(initial * 588 + vowel * 28 + jongsung + 44032)
        buffer.clear()
        return combined_korean

    def automata(self, input_data: List[str]) -> List[str]:
        self.state = AutomataState.INITIAL
        automata_result = []
        buffer = []

        for data in input_data:
            if data in CONSONANT_LIST:
                self.consonant_handler(data=data, buffer=buffer, automata_result=automata_result)
            elif data in VOWEL_LIST:
                self.vowel_handler(data=data, buffer=buffer, automata_result=automata_result)

            else:
                if buffer:
                    automata_result.append(self.combine_buffer(buffer=buffer))
                automata_result.append(data)
                self.state = AutomataState.INITIAL
        if 0 < len(buffer):
            if len(buffer) == 1:
                self.state = AutomataState.ERROR
            automata_result.append(self.combine_buffer(buffer=buffer))
        return automata_result

    def action(self, input_text: Optional[List[str]] = None):
        if not input_text:
            input_data = self.load_data(self.input_path)
        else:
            input_data = input_text

        automata_result = self.automata(input_data)
        automata_result = "".join(automata_result)
        print(automata_result)

        self.save_data(path=self.output_path, data=automata_result)

    def consonant_handler(self, data: str, buffer: List[str], automata_result: List[str]) -> str:
        match self.state:
            case AutomataState.INITIAL:
                # []
                buffer.append(data)
                self.state = AutomataState.CONSONANT_1

            case AutomataState.CONSONANT_1:
                # [ㄱ]
                buffer.append(data)
                if "".join(buffer) in FIRST_CHANGE_ABLE:
                    self.state = AutomataState.CONSONANT_2
                else:
                    self.state = AutomataState.ERROR
                    self.error_handler(buffer=buffer, automata_result=automata_result)

            case AutomataState.CONSONANT_2:
                # [ㄱ,ㄱ]
                self.state = AutomataState.ERROR
                self.error_handler(buffer=buffer, automata_result=automata_result)

            case AutomataState.VOWEL_1:
                # [ㄱ,ㅣ]
                buffer.append(data)
                self.state = AutomataState.FINAL_1

            case AutomataState.VOWEL_2:
                # [ㄱ,ㅏ,ㅣ]+data
                # ㄱ,ㅐ,data
                first_vowel = buffer.pop(-1)
                second_vowel = buffer.pop(-1)
                buffer.append(MIDDLE_CHANGE_ABLE[first_vowel + second_vowel])
                buffer.append(data)
                self.state = AutomataState.FINAL_1

            case AutomataState.VOWEL_3:
                # ㄱ,ㅗ,ㅏ,ㅣ
                buffer.append(data)
                self.state = AutomataState.FINAL_1

            case AutomataState.FINAL_1:
                # ㄱ,ㅣ,ㄱ
                last = buffer.pop(-1)
                if "".join([last, data]) in LAST_CHANGE_ABLE:
                    buffer.append(last)
                    buffer.append(data)
                    self.state = AutomataState.FINAL_2
                else:
                    buffer.append(last)
                    automata_result.append(self.combine_buffer(buffer=buffer))
                    buffer.append(data)
                    self.state = AutomataState.CONSONANT_1

            case AutomataState.FINAL_2:
                # ㄱ,ㅣ,ㄱ,ㄱ
                last_two = buffer.pop(-1)
                last_one = buffer.pop(-1)
                buffer.append(self.combine_final(data=[last_one, last_two]))
                automata_result.append(self.combine_buffer(buffer=buffer))

                buffer.append(data)
                self.state = AutomataState.CONSONANT_1

    def vowel_handler(self, data: str, buffer: List[str], automata_result: List[str]) -> str:
        match self.state:
            case AutomataState.INITIAL:
                self.state = AutomataState.ERROR
                buffer.append(data)
                automata_result.append(self.combine_buffer(buffer=buffer))
                self.state = AutomataState.INITIAL

            case AutomataState.CONSONANT_1:
                self.state = AutomataState.VOWEL_1
                buffer.append(data)

            case AutomataState.CONSONANT_2:
                self.state = AutomataState.VOWEL_1
                buffer.append(data)

            case AutomataState.VOWEL_1:
                first_vowel = buffer.pop(-1)
                if first_vowel + data in MIDDLE_CHANGE_ABLE:
                    buffer.append(first_vowel)
                    buffer.append(data)
                    self.state = AutomataState.VOWEL_2
                else:
                    buffer.append(first_vowel)
                    automata_result.append(self.combine_buffer(buffer=buffer))
                    self.state = AutomataState.ERROR
                    buffer.append(data)
                    automata_result.append(self.combine_buffer(buffer=buffer))
                    self.state = AutomataState.INITIAL

            case AutomataState.VOWEL_2:
                # ㄱ,ㅗ,ㅏ+ㅣ
                # ㄱ,ㅙ
                first_vowel = buffer.pop(-1)
                second_vowel = buffer.pop(-1)
                if first_vowel + second_vowel + data in MIDDLE_CHANGE_ABLE:
                    buffer.append(MIDDLE_CHANGE_ABLE[first_vowel + second_vowel + data])
                    self.state = AutomataState.VOWEL_3
                else:
                    buffer.append(first_vowel)

            case AutomataState.VOWEL_3:
                automata_result.append(self.combine_buffer(buffer=buffer))
                self.state = AutomataState.ERROR
                buffer.append(data)
                automata_result.append(self.combine_buffer(buffer=buffer))
                self.state = AutomataState.INITIAL

            case AutomataState.FINAL_1:
                # ㄱ,ㅏ,ㄱ+ㅏ
                # 가,ㄱ,ㅏ
                last = buffer.pop(-1)
                automata_result.append(self.combine_buffer(buffer=buffer))
                buffer.append(last)
                buffer.append(data)
                self.state = AutomataState.VOWEL_1

            case AutomataState.FINAL_2:
                # ㄱ,ㅏ,ㄱ,ㄱ+ ㅏ
                # 각, ㄱ,ㅏ
                last = buffer.pop(-1)
                automata_result.append(self.combine_buffer(buffer=buffer))
                buffer.append(last)
                buffer.append(data)
                self.state = AutomataState.VOWEL_1

    def error_handler(self, buffer: List[str], automata_result: List[str]) -> str:
        match self.state:
            case AutomataState.INITIAL:
                pass
            case AutomataState.CONSONANT_1:
                data = buffer.pop(-1)
                automata_result.append(self.combine_buffer(buffer=buffer))
                buffer.append(data)
                self.state = AutomataState.CONSONANT_1

            case AutomataState.CONSONANT_2:
                data = buffer.pop(-1)
                buffer.append(self.combine_first(data=buffer))
                automata_result.append(self.combine_buffer(buffer=buffer))
                buffer.append(data)
                self.state = AutomataState.CONSONANT_1
            case AutomataState.VOWEL_1:
                pass
            case AutomataState.VOWEL_2:
                pass
            case AutomataState.VOWEL_3:
                pass
            case AutomataState.FINAL_1:
                pass
            case AutomataState.FINAL_2:
                pass

    def combine_first(self, data: List[str]) -> str:
        combine = "".join(data)
        return FIRST_CHANGE_ABLE[combine]

    def combine_middle(self, data: List[str]) -> str:
        if len(data) == 2:
            combine = "".join(data)
            return MIDDLE_CHANGE_ABLE[combine]
        else:
            first = data.pop(1)
            combine = "".join(data)
            second = MIDDLE_CHANGE_ABLE[combine]
            return MIDDLE_CHANGE_ABLE[first + second]

    def combine_final(self, data: List[str]) -> str:
        combine = "".join(data)
        return LAST_CHANGE_ABLE[combine]


if __name__ == "__main__":
    korean_automata = KoreanAutomata()
    korean_automata.action()


FIRST = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
MIDDLE = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
FINAL = [
    "_",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]
FIRST_CHANGE_ABLE = {
    "ㄱㄱ": "ㄲ",
    "ㄷㄷ": "ㄸ",
    "ㅂㅂ": "ㅃ",
    "ㅅㅅ": "ㅆ",
    "ㅈㅈ": "ㅉ",
}
MIDDLE_CHANGE_ABLE = {
    "ㅏㅣ": "ㅐ",
    "ㅓㅣ": "ㅔ",
    "ㅑㅣ": "ㅒ",
    "ㅕㅣ": "ㅖ",
    "ㅗㅣ": "ㅚ",
    "ㅗㅏ": "ㅘ",
    "ㅗㅐ": "ㅙ",
    "ㅜㅣ": "ㅣ",
    "ㅜㅓ": "ㅝ",
    "ㅜㅔ": "ㅞ",
    "ㅡㅣ": "ㅢ",
}

LAST_CHANGE_ABLE = {
    "ㄱㄱ": "ㄲ",
    "ㄱㅅ": "ㄳ",
    "ㄴㅈ": "ㄵ",
    "ㄴㅎ": "ㄶ",
    "ㅂㅂ": "ㅃ",
    "ㄹㄱ": "ㄺ",
    "ㄹㅁ": "ㄻ",
    "ㄹㅂ": "ㄽ",
    "ㄹㅅ": "ㄾ",
    "ㄹㅍ": "ㄿ",
    "ㄹㅎ": "ㅀ",
    "ㅂㅅ": "ㅄ",
    "ㅅㅅ": "ㅆ",
}
CONSONANT_LIST = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
VOWEL_LIST = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"]
