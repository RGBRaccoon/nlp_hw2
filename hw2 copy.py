from typing import List, Optional

input_path = "input.txt"
output_path = "output.txt"


class AutomataState:
    INITIAL = 0
    CONSONANT_1 = 1
    CONSONANT_2 = 2
    VOWEL_1 = 3
    VOWEL_2 = 4
    FINAL_1 = 5
    FINAL_2 = 6

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
        #  [{(초성)×588}+{(중성)×28}+(종성)]+44032
        if self.state == AutomataState.ERROR:
            # 에러일 때는 초성 또는 중성만 들어온다. 즉 한글자만 들어온다
            # 합칠필요도 딱히 없으니 바로 리턴하면됨
            retunring = buffer[0]
            buffer.clear()
            return retunring
        initial = FIRST.index(buffer[0])
        vowel = MIDDLE.index(buffer[1])
        if len(buffer) == 4:
            print("need to convert")
            jongsung = self.combine_final(first=buffer[2], second=buffer[3])
            jongsung = FINAL.index(jongsung)
        else:
            jongsung = FINAL.index(buffer[2]) if len(buffer) == 3 else 0
        combined_korean = chr(initial * 588 + vowel * 28 + jongsung + 44032)
        buffer.clear()
        return combined_korean

    def combine_possible(self, buffer: List[str]) -> bool:
        print(buffer)
        print(len(buffer))
        if len(buffer) == 4:
            get_key = buffer[2] + buffer[3]
            if get_key in LAST_CHANGE_ABLE:
                print("possible")
                return True
        return False

    def combine_final(self, first, second):
        get_key = first + second
        print(LAST_CHANGE_ABLE[get_key])
        return LAST_CHANGE_ABLE[get_key]

    def automata(self, input_data: List[str]) -> List[str]:
        self.state = AutomataState.INITIAL
        automata_result = []
        buffer = []

        for data in input_data:

            # if (data in FIRST) or (data in FINAL):
            #     match self.state:
            #         case AutomataState.INITIAL:
            #             # ex) []

            #             buffer.append(data)
            #             self.state = AutomataState.CONSONANT

            #         case AutomataState.CONSONANT:
            #             # ex)[ㄱ]
            #             self.state = AutomataState.ERROR
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             buffer.append(data)
            #             self.state = AutomataState.CONSONANT

            #         case AutomataState.VOWEL:
            #             # ex)[ㄱㅏ]
            #             buffer.append(data)
            #             self.state = AutomataState.FINAL

            #         case AutomataState.FINAL:
            #             # ex)[ㄱㅏㄱ]
            #             print("final")
            #             if self.combine_possible(buffer=buffer):
            #                 buffer.append(data)
            #                 self.state = AutomataState.FINAL_2
            #             else:
            #                 automata_result.append(self.combine_buffer(buffer=buffer))
            #                 buffer.append(data)
            #                 self.state = AutomataState.CONSONANT

            #         case AutomataState.FINAL_2:
            #             # ex)[ㄱㅏㄱㄱ]
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             buffer.append(data)
            #             self.state = AutomataState.CONSONANT

            # elif data in MIDDLE:
            #     match self.state:
            #         case AutomataState.INITIAL:
            #             # ex)[]
            #             self.state = AutomataState.ERROR
            #             buffer.append(data)
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             self.state = AutomataState.INITIAL

            #         case AutomataState.CONSONANT:
            #             # ex)[ㄱ]
            #             self.state = AutomataState.VOWEL
            #             buffer.append(data)

            #         case AutomataState.VOWEL:
            #             # ex)[ㄱㅏ]
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             self.state = AutomataState.ERROR
            #             buffer.append(data)
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             self.state = AutomataState.INITIAL

            #         case AutomataState.FINAL:
            #             # ex)[ㄱㅏㄱ]
            #             last_data = buffer.pop(-1)
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             buffer.append(last_data)
            #             buffer.append(data)
            #             self.state = AutomataState.VOWEL
            #         case AutomataState.FINAL_2:
            #             # ex)[ㄱㅏㄱㄱ]
            #             last_data = buffer.pop(-1)
            #             automata_result.append(self.combine_buffer(buffer=buffer))
            #             buffer.append(last_data)
            #             buffer.append(data)
            #             self.state = AutomataState.VOWEL
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
