# 컴퓨터 기본 정보 조회
$pc = Get-CimInstance Win32_ComputerSystem        # 제조사, 모델, 메모리 정보 조회
$os = Get-CimInstance Win32_OperatingSystem       # 운영체제와 부팅 정보 조회
$cpu = Get-CimInstance Win32_Processor            # CPU 정보 조회
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"  # C드라이브 조회

$totalMem = $pc.TotalPhysicalMemory / 1GB         # 전체 메모리를 GB로 변환
$freeMem = $os.FreePhysicalMemory / 1MB           # 남은 메모리를 GB로 변환
$usedMem = $totalMem - $freeMem                   # 사용 중인 메모리 계산
$memRate = ($usedMem / $totalMem) * 100           # 메모리 사용률 계산

$totalDisk = $disk.Size / 1GB                     # C드라이브 전체 용량을 GB로 변환
$freeDisk = $disk.FreeSpace / 1GB                 # C드라이브 남은 공간을 GB로 변환
$usedDisk = $totalDisk - $freeDisk                # C드라이브 사용 공간 계산

Write-Host "===== 내 PC 시스템 정보 ====="          # 제목 출력
Write-Host "제조사/모델 :" $pc.Manufacturer $pc.Model  # 제조사와 모델 출력
Write-Host "운영체제    :" $os.Caption             # Windows 이름 출력
Write-Host "CPU         :" $cpu.Name               # CPU 이름 출력
Write-Host "CPU 코어    :" $cpu.NumberOfCores "개"  # 물리 코어 수 출력
Write-Host "메모리      :" ("{0:N1} / {1:N1} GB ({2:N1}%)" -f $usedMem,$totalMem,$memRate)  # 메모리 출력
Write-Host "C드라이브   :" ("사용 {0:N1} / 전체 {1:N1} GB / 남음 {2:N1} GB" -f $usedDisk,$totalDisk,$freeDisk)  # 디스크 출력
Write-Host "최근 부팅   :" $os.LastBootUpTime       # 최근 부팅 시각 출력