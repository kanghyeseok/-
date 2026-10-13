# seoul_council_PoC

서울시의회 2026년도 예산안 10개 사업에 대해 AI로 **사업별 쟁점**(질의문·요구자료·조정 의견 포함)을 만드는 PoC.

## 바로 보기
| 보고 싶은 것 | 파일 |
|---|---|
| 10개 사업 종합(조정 현황표, 요약 카드, 반복 문제) | [쟁점보고서/00_종합.md](쟁점보고서/00_종합.md) |
| 사업별 쟁점 보고서 | [쟁점보고서/](쟁점보고서/) `p01_…md` ~ `p10_…md` |
| AI 쟁점을 채운 정답지(브라우저로 열기) | [정답지_AI초안/서울예산_사업검토_정답지_AI쟁점초안.html](정답지_AI초안/서울예산_사업검토_정답지_AI쟁점초안.html) |
| 정답지 형식 비교용 데이터 | [쟁점보고서/ai_쟁점_태그.json](쟁점보고서/ai_쟁점_태그.json) |
| 원본 정답지(빈 정답지) | [자료/원본/](자료/원본/) |
| 스킬 | [.claude/skills/budget-issue-extractor/](.claude/skills/budget-issue-extractor/) |
| 공유용 스킬 파일 | [공유/budget-issue-extractor.skill](공유/budget-issue-extractor.skill) |
| 스킬 1차 평가(가상 사업 2건, 사용 100% vs 미사용 75%) | [평가/스킬평가_1차/](평가/스킬평가_1차/) |
| 작업 계획서 | [계획/](계획/) |

## 폴더 구조
```
seoul_council_PoC/
├─ CLAUDE.md                     작업 규칙(Claude Code가 자동으로 읽음)
├─ .claude/skills/
│   └─ budget-issue-extractor/   쟁점 도출 스킬(SKILL.md, references/, scripts/, evals/)
├─ 자료/
│   ├─ 원본/                      사용자 원본 정답지 HTML(수정 금지)
│   └─ 원문이미지/                 원본에서 뽑은 검토보고·사업설명서 쪽 이미지(p01~p10), meta.json
├─ 쟁점보고서/                    사업별 보고서, 종합본, 태그 JSON
├─ 정답지_AI초안/                 AI 쟁점을 채운 정답지 HTML
├─ 평가/스킬평가_1차/              스킬 평가 결과(리뷰 화면 HTML 포함)
├─ 계획/                         작업 계획서
├─ 공유/                         배포용 .skill
└─ 스크립트/                      extract · build_tags · build_summary · fill_sheet
```

## PC에서 쓰는 법
1. 이 폴더를 PC의 projects 폴더로 받습니다(아래 둘 중 하나).
   - Git: `git clone -b claude/wonderful-fermi-dhzkag https://github.com/kanghyeseok/-.git` 후 `seoul_council_PoC` 폴더를 `projects` 안으로 옮깁니다.
   - GitHub 웹: 저장소에서 브랜치를 `claude/wonderful-fermi-dhzkag`로 바꾼 뒤 Code → Download ZIP → 압축을 풀어 `seoul_council_PoC` 폴더를 `projects` 안으로 옮깁니다.
2. 그 폴더에서 Claude Code를 엽니다: `cd projects/seoul_council_PoC` → `claude`
3. `/budget-issue-extractor`로 스킬을 부르거나, "새 정답지 파일로 쟁점 뽑아줘"처럼 요청하면 됩니다. 작업 순서와 규칙은 `CLAUDE.md`에 있습니다.

## 한계
- 서울시의회 회의록은 작업 환경에서 접속이 막혀 인용하지 않았습니다. 외부 근거는 웹 검색 요약 기준입니다.
- 정답지의 전문가 정답이 비어 있어 AI 결과의 정확도는 아직 채점하지 않았습니다.
