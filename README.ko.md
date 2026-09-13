<p align="center"><a href="README.md">English</a> | <a href="README.ko.md">한국어</a></p>

<p align="center">
  <a href="https://github.com/wonjangcloud9/notdone/actions/workflows/validate.yml"><img src="https://github.com/wonjangcloud9/notdone/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6b5bd6" alt="Claude Code skill">
</p>

# notdone

**에이전트가 다 됐다고 말합니다. 화면은 한 번도 안 봤고요.**

증거 없이 완료를 선언하지 못하게 막는 스킬입니다.

---

모든 에이전트가 이럽니다:

> 설정 페이지에 다크 모드를 적용했습니다. 이제 정상 동작할 겁니다.

CSS를 썼을 뿐, 페이지를 열어보진 않았습니다. 글자가 읽히는지 모르고, 당신도 모릅니다 — 직접 확인하기 전까지는. 그 확인을 안 하려고 에이전트를 쓰는 건데 말이죠.

`notdone`을 깔면 같은 턴이 이렇게 끝납니다:

> | 주장 | 증거 | 판정 |
> |---|---|---|
> | 설정 페이지 다크 모드 | `shots/settings-dark.png` — 라벨 읽힘, 구분선 보임 | DONE |
> | 라이트 모드 영향 없음 | `shots/settings-light.png` | DONE |
> | 빈 상태 | — | **NOT DONE** |
> | 모바일 폭 | — | **NOT DONE** |
>
> **NOT DONE.** 저장된 프로필이 0개인 상태를 렌더링해보지 않았고, 400px에서 확인하지 않았습니다.

정직하게 표시된 두 줄이, 자신 있는 네 줄보다 낫습니다. [더 자세한 전후 비교](examples/session.md)에서는, 정직한 쪽이 자신 있는 쪽이 그냥 배포했을 버그를 잡아냅니다.

## 설치

```bash
git clone https://github.com/wonjangcloud9/notdone ~/.claude/skills/notdone
```

이게 전부입니다. 레포 자체가 스킬 디렉터리예요.

프로젝트 하나에만 적용하려면 해당 레포 안의 `.claude/skills/notdone`으로 clone 하면 됩니다.

플러그인으로 설치할 수도 있습니다. 이쪽은 업데이트가 편합니다:

```bash
claude plugin marketplace add wonjangcloud9/notdone
claude plugin install notdone@wonjang-skills
```

에이전트가 완료를 보고하려 할 때 알아서 발동합니다. `/notdone`으로 직접 부르거나 "이거 진짜 다 된 거야?"라고 물어도 됩니다.

## 규칙

이번 세션에서 얻은 **증거물**이 없으면 **done**, **수정 완료**, **동작함**, **준비됨**, **될 겁니다** 를 쓸 수 없습니다.

증거물은 변경한 **뒤에** 관찰한 것입니다:

- 실제로 실행한 명령의 출력
- 실제로 찍고 눈으로 본 스크린샷
- 실제로 받은 HTTP 응답

작성한 코드는 증거가 아닙니다. 왜 잘 동작할지에 대한 설명도 증거가 아닙니다. 추가했지만 실행하지 않은 테스트도 증거가 아닙니다.

## 무엇이 증거인가

| 바뀐 것 | 이것 없이는 완료 아님 |
|---|---|
| UI | 라이트·다크·빈 상태·~400px 스크린샷 4장, 각각 눈으로 확인 |
| 로직 / API | 실제 테스트 출력 — 명령, 종료 코드, 통과·실패 개수 |
| 버그 수정 | 같은 재현 절차가 수정 전엔 실패, 후엔 통과 |
| 데이터 / 마이그레이션 | 적용 출력 + 바뀐 스키마를 확인하는 쿼리 |
| 배포 | 바깥에서 실제 URL이 응답한 상태 코드 |
| 의존성 / 설정 | 이미 떠 있는 프로세스가 아니라 깨끗한 설치·부팅 |
| 문서 | 문서에 적힌 모든 명령을 적힌 그대로 실행 |

[checklists](checklists/)에 더 들어갑니다 — 다크 모드 스크린샷에서 실제로 봐야 할 것, 백필 카운트가 "이전"이 없으면 무의미한 이유, 빌드 초록불이 배포 성공이 아닌 이유.

## 없어지는 표현들

"이제 될 겁니다." "이걸로 해결될 거예요." "간단한 변경이라..." "X를 고쳤으니 이제 Y 할 겁니다." "괜찮아 보입니다."

전부 *확인 안 했다*는 말의 다른 표현입니다. 스킬이 이것들을 증거로, 아니면 **NOT DONE** + 빠진 항목으로 바꿉니다.

## 확인이 불가능할 때

브라우저가 없거나, 자격 증명이 없거나, 유료 외부 서비스라 정말 확인할 수 없을 때가 있습니다. 그럴 땐 바로 행동할 수 있는 형태로 말합니다:

> **NOT VERIFIED** — Stripe 웹훅 핸들러를 고쳤지만 여기서 Stripe에 닿을 수 없습니다.
> 확인 방법: 테스트 결제를 발생시키고 핸들러가 `payment.succeeded`를 로그에 남기는지 보세요.

확인 못 한 주장에 "완료"를 붙이는 일은 없습니다.

## 다른 에이전트

프로젝트 지침 파일이 있는 도구라면 어디서든 같은 규칙이 돕니다. Codex·Cursor 등에서는 [AGENTS.md](AGENTS.md)를 레포 루트에 두거나 기존 `CLAUDE.md` 뒤에 붙이세요.

## 왜

완료를 과장하는 에이전트는 느린 에이전트보다 나쁩니다. 느린 쪽은 시간을 뺏지만, 확신에 차서 틀리는 쪽은 **모든 보고를 못 믿게 만듭니다** — 사실인 보고까지 포함해서요.

**NOT DONE**을 보고하는 건 성공입니다. 끝낸 네 개와 정직한 다섯 번째 줄은 바로 대응할 수 있습니다. 다섯 개를 주장했는데 하나가 거짓이면 전부 다시 검증해야 하고, 그건 결국 직접 하는 것과 같습니다.

## 라이선스

MIT
