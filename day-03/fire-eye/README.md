# MediaPipe 웹캠 눈 이미지 합성

웹캠에서 얼굴의 양쪽 눈을 추적하여 `a.png`를 눈의 위치, 크기, 기울기에 맞게 실시간 합성하는 Python 예제입니다.

## 준비물

- Windows 10/11
- Python 3.10~3.12 권장
- 웹캠
- 합성할 이미지 `a.png`

프로젝트 폴더 구조:

```text
eye-overlay-mediapipe/
├─ a.png
├─ eye_overlay.py
├─ requirements.txt
├─ README.md
└─ 작업지시서.md
```

> 현재 제공된 파일 묶음에는 첨부 이미지가 포함되지 않을 수 있습니다. 사용하려는 이미지를 `a.png`라는 이름으로 이 폴더에 복사하세요. 투명 배경 PNG 사용을 권장합니다.

## 1. 환경 구성

PowerShell에서 프로젝트 폴더로 이동한 뒤 실행합니다.

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

CMD에서는 다음과 같이 활성화합니다.

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. 실행

```powershell
python eye_overlay.py
```

- 종료: `Q` 또는 `Esc`
- 좌우 반전 없이 실행: `python eye_overlay.py --no-mirror`
- 합성 크기 변경: `python eye_overlay.py --scale 1.8`
- 투명도 변경: `python eye_overlay.py --opacity 0.7`
- 두 번째 카메라 사용: `python eye_overlay.py --camera 1`
- 다른 이미지 사용: `python eye_overlay.py --image sample.png`

옵션은 함께 사용할 수 있습니다.

```powershell
python eye_overlay.py --image a.png --camera 0 --scale 1.6 --opacity 0.9
```

## 3. 동작 방식

1. OpenCV가 웹캠 프레임을 읽습니다.
2. MediaPipe Face Mesh가 얼굴 랜드마크를 추적합니다.
3. 눈꼬리와 눈꺼풀 좌표로 눈의 중심, 폭, 높이, 기울기를 계산합니다.
4. `a.png`를 계산된 크기로 조정하고 회전합니다.
5. 알파 블렌딩으로 원본 프레임의 양쪽 눈 위에 합성합니다.

## 4. 문제 해결

### `a.png`를 찾을 수 없음

`eye_overlay.py`와 같은 폴더에 `a.png`가 있는지 확인하세요. 다른 위치라면 전체 경로를 지정합니다.

```powershell
python eye_overlay.py --image "C:\images\a.png"
```

### 카메라를 열 수 없음

- Zoom, Teams 등 카메라를 사용 중인 앱을 종료합니다.
- Windows의 **설정 → 개인정보 및 보안 → 카메라**에서 데스크톱 앱 권한을 허용합니다.
- `--camera 1` 또는 `--camera 2`를 시험합니다.

### 합성 이미지가 너무 크거나 작음

`--scale`을 조절합니다. 기본값은 `1.55`입니다.

### MediaPipe 설치 실패

`python --version`으로 버전을 확인하세요. Python 3.13 이상이라면 Python 3.11 또는 3.12 가상환경을 사용하는 것이 안전합니다.

## 5. 문법 검사

웹캠 실행 전 다음 명령으로 Python 문법을 검사할 수 있습니다.

```powershell
python -m py_compile eye_overlay.py
```

이 프로그램은 카메라 영상을 파일이나 서버로 전송하지 않으며 화면에만 표시합니다.
