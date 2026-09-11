# MediaPipe 얼굴 랜드마크 프로젝트 실행 순서

이 문서는 Codex가 `TASK.md`에 따라 얼굴 랜드마크 출력 프로그램을 만들고 검증하도록 실행하는 순서를 설명한다.

## 준비 파일

프로젝트 폴더에 다음 파일을 둔다.

```text
face-project/
├── face_landmark.py
├── TASK.md
├── README.md
└── face.jpg
```

- `TASK.md`: Codex용 작업지시서
- `README.md`: 작업 및 실행 순서
- `face.jpg`: 분석할 정면 얼굴 사진

얼굴 사진은 밝고, 정면을 바라보며, 얼굴 전체가 선명하게 나온 이미지를 권장한다.

## 1. Codex 실행

프로젝트 폴더에서 Codex를 시작한 다음 아래처럼 지시한다.

```text
TASK.md를 읽고 지시사항대로 구현, 실행, 오류 수정, 최종 검증까지 완료해줘.
```

Codex는 다음 순서로 작업해야 한다.

```text
환경 확인
→ 기존 파일 확인
→ requirements.txt 작성
→ face_landmark.py 작성
→ 패키지 설치
→ 구문 검사
→ 실제 이미지 실행
→ 결과 이미지 검증
→ 완료 보고
```

## 2. Codex가 생성할 파일

작업이 끝나면 구조는 다음과 같아야 한다.

```text
face-project/
├── TASK.md
├── README.md
├── face.jpg
├── face_landmark.py
├── requirements.txt
└── face_landmark_result.jpg
```

## 3. 직접 실행하는 방법

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py face_landmark.py face.jpg
```

PowerShell 실행 정책 때문에 가상환경 활성화가 막히면 현재 창에서만 허용한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS 또는 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python face_landmark.py face.jpg
```

## 4. 다른 파일과 출력 경로 사용

```bash
python face_landmark.py input.jpg -o output.jpg
```

화면 창에서도 결과를 확인하려면 데스크톱 환경에서 `--show`를 추가한다.

```bash
python face_landmark.py input.jpg -o output.jpg --show
```

기본 실행에서는 창을 띄우지 않고 `face_landmark_result.jpg`만 저장한다.

## 5. 결과 확인

정상 완료 시 다음을 확인한다.

- 터미널에 검출된 랜드마크 수가 표시된다.
- `face_landmark_result.jpg`가 생성된다.
- 얼굴 위에 랜드마크 점과 연결선이 보인다.
- 각 점 주변에 랜드마크 번호가 표시된다.
- 원본 `face.jpg`는 변경되지 않는다.

## 6. 자주 발생하는 오류

| 오류 | 확인 및 조치 |
|---|---|
| `python` 또는 `py`를 찾을 수 없음 | Python 3.10 이상 설치 후 터미널 재실행 |
| `No module named mediapipe` | `python -m pip install -r requirements.txt` 실행 |
| 이미지 파일 없음 | 파일명과 현재 폴더 확인 |
| 이미지를 읽을 수 없음 | JPG/PNG 파일인지, 손상되지 않았는지 확인 |
| 얼굴을 찾지 못함 | 정면 사진, 밝기, 얼굴 크기, 가림 여부 확인 |
| 결과 파일 저장 실패 | 출력 폴더 존재 여부와 쓰기 권한 확인 |
| 창 표시 실패 | `--show`를 빼고 이미지 파일로 결과 확인 |

## 7. Codex 재실행 요청

오류가 발생하면 전체 코드를 새로 만들게 하지 말고 다음처럼 요청한다.

```text
현재 오류의 원인을 확인하고 관련 부분만 수정한 뒤, TASK.md의 완료 기준으로 다시 검증해줘.
```

출력 파일은 재실행할 때 덮어써도 되지만 입력 얼굴 사진과 사용자가 만든 다른 파일은 변경하지 않는다.

## 8. 작업 완료 기준

Codex의 최종 보고에서 아래 네 가지를 확인한다.

1. 생성하거나 수정한 파일
2. 실제 사용한 실행 명령
3. 테스트 성공 여부
4. 결과 이미지 경로 또는 해결하지 못한 문제

이 프로젝트의 결과는 얼굴 특징점 시각화 용도이며 의료 진단 결과로 사용하지 않는다.
