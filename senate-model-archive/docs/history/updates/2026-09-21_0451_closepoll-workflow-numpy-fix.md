# Close-poll PVI workflow fix

## 날짜
2026-09-21

첫 실행은 모델 계산 전에 `ModuleNotFoundError: No module named 'numpy'`로 중단됐다.

원인은 workflow에서 numpy 설치 단계를 누락한 것이다.

`python -m pip install --disable-pip-version-check numpy`를 추가했다.

첫 실행은 성능 결과로 간주하지 않는다. 동일한 실험을 수정된 workflow로 재실행한다.
