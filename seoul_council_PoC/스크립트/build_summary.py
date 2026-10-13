import sys,re,json,glob,os,collections
root=sys.argv[1]
meta=json.load(open(os.path.join(root,'자료/원문이미지/meta.json'),encoding='utf-8'))
tags=json.load(open(os.path.join(root,'쟁점보고서/ai_쟁점_태그.json'),encoding='utf-8'))
TL={x['id']:x['label'] for x in meta['issue_types']}; CL={x['id']:x['label'] for x in meta['conclusions']}
L=[]
L.append("# 2026년도 서울시 예산안 10개 사업 쟁점 종합\n")
L.append("> 원자료: 「서울시 2026년도 예산안 사업 검토 정답지」(분석관용, 사업설명서 포함) — 예비심사보고서(검토보고) 쪽 이미지, 사업설명서 쪽 이미지, 의회 조정내역")
L.append("> 작성: AI(budget-issue-extractor 스킬) · 사업당 쟁점 6개(핵심 3 + 추가 3) · 외부 근거는 웹 검색 요약 기준, 서울시의회 회의록은 사이트 접속 차단으로 미확인")
L.append("> 정답지(#answers)는 비어 있어 정답 대조는 하지 않았음. 전문가 정답이 채워지면 `ai_쟁점_태그.json`으로 비교할 수 있음.\n")
L.append("## 1. 사업별 조정 현황 (단위: 천원)\n")
L.append("| ID | 사업 | 위원회 | 예산안 | 의회 조정 | 조정 후 | 핵심 쟁점 1 | 보고서 |")
L.append("|---|---|---|---:|---:|---:|---|---|")
tp=ta=0
for p in meta['projects']:
    am=p['amendment']; prop=sum(int(a['proposed']) for a in am) if am else None
    f=os.path.basename(glob.glob(os.path.join(root,'쟁점보고서',p['id']+'_*.md'))[0])
    txt=open(os.path.join(root,'쟁점보고서',f),encoding='utf-8').read()
    m=re.search(r'사업비\(당해년도\)|',txt)
    ch=int(p['council_change'])
    first=tags['projects'][p['id']]['issues'][0]['summary']
    if am:
        prop=int(am[0]['proposed']); amd=int(am[0]['amended'])
    else:
        prop=amd=None
    L.append(f"| {p['id']} | {p['title']} | {p['committee']} | {prop:,} | {ch:+,} | {amd:,} | {first} | [{f}]({f}) |" if prop is not None else f"| {p['id']} | {p['title']} | {p['committee']} | (조정 없음) | 0 | — | {first} | [{f}]({f}) |")
L.append("\n※ 예산안·조정 후 금액은 사업 전체 금액(의회 조정내역 JSON `amendment`의 proposed·amended). p02는 조정이 없어 예산안 500,000천원을 원안 의결.\n")
L.append("## 2. 사업별 요약 카드\n")
for p in meta['projects']:
    f=glob.glob(os.path.join(root,'쟁점보고서',p['id']+'_*.md'))[0]
    txt=open(f,encoding='utf-8').read()
    card=re.search(r'## 사업 요약 카드\n\n```\n(.+?)```',txt,re.S).group(1)
    L.append(f"### {p['id']}. {p['title']}\n\n```\n{card}```\n")
L.append("## 3. 쟁점 유형 집계 (주 유형 기준, 60개)\n")
cnt=collections.Counter(i['type'] for v in tags['projects'].values() for i in v['issues'])
cc=collections.Counter(i['conclusion'] for v in tags['projects'].values() for i in v['issues'])
L.append("| 쟁점 종류 | 개수 |\n|---|---:|")
for k,n in cnt.most_common(): L.append(f"| {TL.get(k,k)} | {n} |")
L.append("\n| 결론·권고 | 개수 |\n|---|---:|")
for k,n in cc.most_common(): L.append(f"| {CL.get(k,k)} | {n} |")
L.append("\n## 4. 10개 사업에서 반복된 문제 (예산 심사 전반에 쓸 수 있는 질의 포인트)\n")
L.append("""- **이월이 쌓이는데 증액**: p01(2025 예산 74% 이월 예정), p03(2025 집행률 2.3%), p06(2024 집행률 12.7%), p09(특교세 57억 명시이월). "작년 돈을 다 못 쓰고 올해 더 달라"는 구조 — 이월액 집행계획을 먼저 요구.
- **총사업비가 설계비뿐이거나 문서마다 다름**: p02(재원 시비 100% vs 국비 50%), p04(총사업비=설계 용역비), p06(총사업비 3가지), p07(총사업비=용역비), p09(총사업비·연차계획 없음). 후속 사업비가 예산서에 드러나지 않음.
- **기술용역·투자심사 결과를 예산에 반영하지 않음**: p02·p07(같은 날 같은 국, "용역비 조정" 미반영), p02(총사업비 500억 초과 신규인데 타당성조사 표기 없음).
- **산출근거 산식·표기 오류**: p01(800백만원×3개소=2,100백만원), p02(공사비 "425.097백만원", "시비350%"), p08(임시사무실 1억4,770만원 vs 104,770천원).
- **전문위원 지적과 의회 조정이 서로 다른 항목을 다룸**: p06(검토는 변전시설 이전비, 조정은 보상비), p08(검토는 교섭단체 공간, 조정은 보수·보강 공사) → 미해소 쟁점으로 남음.
- **성과지표가 산출(개소·건수)뿐**: 거의 모든 사업. 결과지표(효과) 설정을 공통 부대의견으로 제안할 만함.
""")
L.append("## 5. 한계와 확인 필요 사항\n")
L.append("""- 서울시의회 회의록(council.seoul.go.kr, clik.nanet.go.kr)은 이 작업 환경에서 접속이 막혀, 2025.11. 예비심사 발언은 하나도 인용하지 않았음. 언론에 보도된 의원 발언은 [언론]으로 표시하고 "회의록 원문 대조 전"으로 처리함.
- 웹 기사 본문은 열 수 없어(WebFetch가 국내 언론 도메인에 접속 불가) 검색 요약을 근거로 씀. 일자·수치는 의원 자료로 쓰기 전에 원문 확인이 필요함.
- 원문 이미지 판독은 확대 판독으로 검증했으나, 표기 오류로 보이는 수치(p02 "시비350%" 등)는 `[판독/오기 추정]`으로 표시함.
- 감액 산식 중 일부는 가정(p08 물가상승률 5% 등)을 포함하며, 보고서에 가정임을 밝혀 둠.
""")
open(os.path.join(root,'쟁점보고서/00_종합.md'),'w',encoding='utf-8').write('\n'.join(L))
print('ok', sum(cnt.values()))
