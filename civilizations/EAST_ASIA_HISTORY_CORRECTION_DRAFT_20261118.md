# 사용자 제공 문명.xlsx — 한·중·일 18셀 역사 연대 교정 검토본
2026-11-18 | **PROPOSAL / 사용자 최종 승인 전**

## 원본 보존
- 사용자 업로드 원본 셀 값: [USER_UPLOADED_CIVILIZATION_SHEET1_20261118.csv](USER_UPLOADED_CIVILIZATION_SHEET1_20261118.csv) — **무변경**.
- 25×14 전체 표에 수정안만 적용한 복사본: [USER_UPLOADED_CIVILIZATION_SHEET1_EAST_ASIA_CORRECTION_DRAFT_20261118.csv](USER_UPLOADED_CIVILIZATION_SHEET1_EAST_ASIA_CORRECTION_DRAFT_20261118.csv)
- 한국(A3:N3), 중국(A5:N5), 일본(A7:N7)의 **18개 셀만 수정**. 다른 문명·시대 헤더·미래빈칸 유지.
- ChatGPT에서 사용자에게 제공한 XLSX 사본: `문명_원본기준_한중일수정안.xlsx`. 이 문서의 GitHub CSV는 **셀값만** 저장하며 엑셀 서식의 복제나 XLSX 바이너리 업로드를 뜻하지 않음.

## 실제 변경된 셀 (원본 → 수정안)
| 좌표 | 원본 | 수정안 |
|---|---|---|
| C3 | 고구려/백제/신라 | 고조선/위만조선 → 부여/삼한/초기 삼국·가야 |
| D3 | 고구려/백제/신라 | 고구려/백제/신라/가야 |
| E3 | 통일신라/발해 -> 고려 | 고구려/백제/신라 → 신라/발해 → 후삼국 → 고려 |
| J3 | 조선 | 조선 → 대한제국 |
| K3 | 대한제국 | 대한제국 → (일제강점기·대한민국 임시정부) |
| B5 | 하 -> 상 -> 주 | 하(전승) → 상 → 서주 |
| C5 | 춘추전국 -> 진 -> 한 | 동주(춘추·전국) → 진 → 한 |
| D5 | 수 | 삼국(위·촉·오) → 진 → 남북조 → 수 |
| E5 | 당 | 수 → 당 → 오대십국/요/북송 |
| F5 | 북송 -> 남송 ->원 | 북송/요/서하 → 남송/금/서하 → 원 |
| C7 | *(빈칸)* | 왜(야요이 소국) |
| D7 | *(빈칸)* | 야마타이국/야마토 왕권 |
| E7 | *(빈칸)* | 야마토 왕권 → 율령 일본 → 헤이안 조정 |
| F7 | *(빈칸)* | 헤이안 조정 → 가마쿠라 막부 |
| G7 | 무로마치 | 가마쿠라 막부 → 무로마치 막부 |
| H7 | 센고쿠 -> 도쿠가와 | 전국시대/아즈치·모모야마 → 도쿠가와 막부 |
| I7 | 도쿠가와 | 도쿠가와 막부 |
| J7 | 도쿠가와 | 도쿠가와 막부 → 메이지 일본 |

## 주요 이유와 공식 참고자료
- **한국 C3,D3,E3:** 고조선·삼한·삼국·가야 형성 및 병존, 신라/발해·후삼국·고려의 출현 연대. [국사편찬위원회 초기국가](https://contents.history.go.kr/front/nh/print.do?levelId=nh_004_0040), [후삼국과 고려](https://contents.history.go.kr/front/ta/view.do?levelId=ta_e32_0030_0050_0080)
- **한국 J3,K3:** 대한제국 선포는 1897년이며 1910년에 국권 상실. 1919년 대한민국 임시정부는 망명 독립운동 정부로, 당시 한반도의 독립 통치국가와 구분한다. [국사편찬위원회 대한제국](https://contents.history.go.kr/front/nh/view.do?levelId=nh_042), [임시정부](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_o400800)
- **중국 B5~F5:** 하왕조의 전승과 사료 논쟁, 동주·진·한, 삼국·진·남북조·수, 수·당·오대십국, 송·요·서하·금·원 병존. [Met 고대 중국](https://www.metmuseum.org/de/toah/ht/03/eac), [Met 1–500](https://82nd-and-fifth.metmuseum.org/toah/ht/05/eac.html), [Met 500–1000](https://www.metmuseum.org/zh/toah/ht/06/eac.html), [Met 1000–1400](https://artistproject.metmuseum.org/toah/ht/07/eac.html)
- **일본 C7~J7:** 왜·야마타이국·야마토 왕권·율령일본·헤이안·가마쿠라·무로마치·전국시대·에도·메이지의 연대 반영. [Met 일본 1–500](https://www.metmuseum.org/ja/toah/ht/05/eaj), [Met 일본 500–1000](https://www.metmuseum.org/ko/toah/ht/06/eaj), [Columbia 일본 연표](https://afe.easia.columbia.edu/timelines/japan_timeline.htm).
- **일본 B7은 원본대로 공란**. 조몬/야요이 문화기를 독립국가로 만들어 채우지 않는다.
- 화살표는 시간적 전개를 뜻하며 정치적·법적 직접 계승을 자동 확정하지 않음. 슬래시는 병렬 세력/동일 시대에 등장한 정치체이며 이들 모두가 시대 구간 내내 동시 존속했다고 단정하지 않음.
- **현재 수정안은 역사 연대 검토안일 뿐 플레이 가능한 Civilization의 국가별 최종 로스터를 승인한 것이 아님.** 원본에 없는 문명 분리·멸망·건국 이벤트의 게임 코드는 수정하지 않음.
