from gpiozero import TonalBuzzer
from time import sleep

# TonalBuzzer를 GPIO18에 연결

tb = TonalBuzzer(18)

# 음악 정의
SONG = [
  ["E5",0.3],["Eb5",0.3],["E5",0.3],["Eb5",0.3],["E5",0.3],
  ["B4",0.3],["D5",0.3],["C5",0.3],["A4",0.6],[None,0.1],
  ["C4",0.3],["E4",0.3],["A4",0.3],["B4",0.6],[None,0.1],
  ["E4",0.3],["Ab4",0.3],["B4",0.3],["C5",0.6],[None,0.1],
  ["E4",0.3],["E5",0.3],["Eb5",0.3],["E5",0.3],["Eb5",0.3],
  ["E5",0.3],["B4",0.3],["D5",0.3],["C5",0.3],["A4",0.6],
  [None,0.1],["C4",0.3],["E4",0.3],["A4",0.3],["B4",0.6],
  [None,0.1],["E4",0.3],["C5",0.3],["B4",0.3],["A4",0.1]
]
# 음악 재생 함수
def play(tune):
    """
    TonalBuzzer를 사용하여 음악 재생.
    :param tune: (음표, 지속시간)으로 이루어진 리스트
    """
    for note, duration in tune:
        if note:
            tb.play(note)  # 음표를 재생
        sleep(float(duration))  # 음표의 지속 시간만큼 대기
    tb.stop()  # 재생이 끝난 후 멈춤

# 음악 정지 함수
def stop_music():
    tb.stop()
