# 환율 계산기와 환율 기록

작성일: 2026-09-10

Frankfurter API에서 USD 기준 KRW·JPY·EUR 환율을 받아 CSV로 저장하고, HTML 계산기에서 네 통화를 서로 변환하는 프로젝트입니다. 향후 환율 변동 그래프를 만들 수 있도록 수집 기록을 별도 CSV에 누적합니다.

## 작업 위치와 파일

프로젝트 위치: `C:\ai-starter\output\Day2\exchange-calculator`

```text
C:\ai-starter\output\Day2\exchange-calculator
├─ README.md
├─ update-rates.ps1                 # API 수집, 최신 CSV 갱신, 이력 누적
├─ index.html                   # 한국어 환율 계산기 화면
├─ calculator.js                # CSV 해석, 입력 검증, 환율 계산
├─ exchange-rates.csv           # 가장 최근 수집한 환율 3행
├─ exchange-rate-history.csv    # 수집 시각별 누적 이력
└─ rates-data.js                # 최신 CSV를 읽어 생성한 브라우저용 사본
```

그 외 기존 폴더와 파일은 이번 환율 기능과 별개입니다.

## 실행 방법

계산기는 `C:\ai-starter\output\Day2\exchange-calculator\index.html`을 브라우저에서 열면 됩니다. 금액과 통화를 선택하면 자동 계산되며, 통화 교환 버튼으로 방향을 바꿀 수 있습니다.

최신 환율을 수동으로 수집하려면 PowerShell에서 실행합니다.

```powershell
cd C:\ai-starter\output\Day2\exchange-calculator
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\update-rates.ps1
```

수집에는 인터넷 연결이 필요합니다. 갱신 후 계산기 페이지를 새로고침하세요. 별도 Python·Node.js·패키지 설치는 필요하지 않습니다.

HTML을 더블클릭해 열면 `rates-data.js`에 저장된 CSV 사본을 사용합니다. HTTP 서버에서 열면 `exchange-rates.csv`를 직접 가져옵니다. CSV를 수동 수정했다면 화면의 **다른 CSV 불러오기**에서 해당 파일을 선택하세요. 이 선택은 화면에만 적용되며 디스크의 다른 파일을 갱신하지 않습니다.

## 데이터 출처와 CSV 형식

API: <https://api.frankfurter.dev/v1/latest?from=USD&to=KRW,JPY,EUR>

### 최신 환율: exchange-rates.csv

```csv
date,base,currency,rate
2026-09-09,USD,KRW,1336.2
2026-09-09,USD,JPY,153.27
2026-09-09,USD,EUR,0.85822
```

위 값은 최초 작업 시 받은 예시이며, 수집할 때마다 최신 파일을 덮어씁니다.

### 누적 이력: exchange-rate-history.csv

```csv
date,base,currency,rate,collected_at
2026-09-09,USD,KRW,1336.2,2026-09-10T14:36:38+09:00
```

| 열 | 의미 |
| --- | --- |
| `date` | API가 제공한 환율 기준일. 수집 날짜와 다를 수 있음 |
| `base` | 기준 통화. 현재 USD 고정 |
| `currency` | 대상 통화. KRW, JPY, EUR |
| `rate` | 1 USD당 대상 통화 금액 |
| `collected_at` | 실제 수집 시각. ISO 8601 형식이며 PC의 시간대 오프셋 포함 |

CSV는 UTF-8로 저장합니다. 매번 세 통화의 기록을 추가하며, 같은 환율이라도 수집 시각별로 남깁니다. 수동 실행 역시 이력을 추가합니다. USD 환율은 계산기에서 1로 취급하므로 CSV에 별도 행이 없습니다.

현재 계산기의 파일 선택 기능은 최신 환율 CSV 형식만 지원합니다. 누적 이력 CSV를 직접 넣어 계산하거나 그래프로 그리는 기능은 아직 없습니다.

## 계산 방식과 확인한 내용

```text
환산 금액 = 입력 금액 × 받는 통화의 USD 기준 환율 ÷ 보내는 통화의 USD 기준 환율
```

표시 금액은 소수점 둘째 자리까지 반올림하며, 은행 수수료와 환전 스프레드는 포함하지 않습니다. 빈 입력, 음수, 유효하지 않은 환율, 중복 통화 행 등을 검사합니다.

구현 당시 USD→KRW, KRW→USD, EUR→JPY, 0 입력, 음수 거부, 중복 CSV 거부, 최신 CSV와 브라우저용 사본의 일치를 코드로 확인했습니다. 이력 CSV의 첫 세 행과 수집 시각 형식도 확인했습니다.

## 예약 실행

2026-09-10에 다음 **Codex 자동화**를 등록했습니다.

- 이름: `매시 환율 CSV 수집`
- 자동화 ID: `csv`
- 일정: 매시 정각, 한국 시간 기준
- 실행 파일: `C:\ai-starter\output\Day2\exchange-calculator\update-rates.ps1`
- 성공 시 별도 알림 없이 종료하고, 실패 또는 사용자 조치가 필요할 때 알림

Windows 작업 스케줄러에 등록된 작업은 아닙니다. Codex의 자동화 화면에서 상태와 실행 결과를 확인하고 일정을 변경하거나 중지할 수 있습니다. 이 README와 파일만 다른 PC로 복사해도 예약 설정이 이전되지는 않습니다.

로컬 실행을 위해 PC와 Codex 실행 환경이 사용 가능해야 합니다. PC 종료·절전·네트워크 문제 등에 따라 수집이 누락되거나 지연될 수 있으므로 그래프에는 예약 시간이 아닌 실제 `collected_at`을 사용하세요. 매시 수집해도 API의 기준일과 환율이 그대로일 수 있습니다.

## 다음 작업: 환율 변동 그래프

아직 그래프는 구현하지 않았습니다. 다음 작업에서는 기존 누적 파일을 보존하고 아래 순서로 진행하면 됩니다.

1. `exchange-rate-history.csv`를 읽는 기능을 추가합니다.
2. 시간별 그래프는 `collected_at`을 시간대로 해석해 정렬하고, `currency`별로 선을 나눕니다.
3. 기준일별 그래프는 `date`와 `currency`별로 묶어 가장 늦은 `collected_at`의 기록 하나를 사용합니다.
4. KRW·JPY·EUR는 값의 크기가 다르므로 통화 선택 또는 별도 그래프로 표시하는 방식을 고려합니다.
5. 기간 선택, 데이터 없음, 수집 누락, CSV 불러오기 오류를 처리합니다.

이력은 2026-09-10부터 수집한 관측 기록이며 과거 환율을 소급 수집한 데이터는 아닙니다. 과거 기간이 필요하면 별도 수집 기능이 필요합니다.

다음 작업 요청 예시:

> C:\ai-starter\output\Day2\exchange-calculator\README.md를 읽고 이어서 작업해줘. 기존 환율 이력 CSV를 보존하면서 통화별 환율 변동 그래프를 HTML 계산기에 추가해줘.

## 유지보수 참고

- 이력 파일을 삭제하면 누적 기록을 잃습니다. 수정 전 백업하세요.
- 실행 중인 자동화와 수동 갱신을 동시에 실행하지 마세요. 현재 스크립트에는 동시 실행 잠금이 없습니다.
- API 요청이나 응답 검증 실패 시 오류로 종료합니다. 파일 쓰기 중 실패하면 파일 간 갱신 상태가 다를 수 있으므로 오류 원인을 해결한 후 재실행하고 이력을 확인하세요.
- 파일 경로를 옮기면 자동화의 실행 경로도 수정해야 합니다.
- `rates-data.js`는 생성 파일입니다. 환율은 API 갱신 또는 CSV 불러오기로 변경하세요.
