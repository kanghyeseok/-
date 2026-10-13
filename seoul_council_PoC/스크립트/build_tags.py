import sys,re,json,glob,os
root=sys.argv[1]
meta=json.load(open(os.path.join(root,'자료/원문이미지/meta.json'),encoding='utf-8'))
T={x['label']:x['id'] for x in meta['issue_types']}
C={x['label']:x['id'] for x in meta['conclusions']}
I={x['label']:x['id'] for x in meta['importance']}
S={x['label']:x['id'] for x in meta['sources']}
TK=[('집행 부진','exec_overrun'),('이월','carryover'),('추경','supp_unspent'),('산출근거','basis'),('투자심사','invest_review'),('국비','funding'),('지방채','bond'),('기금','fund'),('사업 준비','readiness'),('필요성','necessity'),('유사·중복','duplication'),('성과지표','performance'),('위탁','delivery')]
SK=[('전문위원','review'),('의회 감액','council'),('분석관','own')]
def kw(label,pairs):
    for k,v in pairs:
        if k in label: return v
    return None
def match(label,table):
    label=label.strip()
    for k,v in table.items():
        if label==k or label in k or k in label: return v
    return None
out={"sheet_id":meta['sheet_id'],"generated_by":"AI(budget-issue-extractor)","note":"AI 분석 결과. 전문가 정답지(#answers)와 비교용이며 정답지에는 넣지 않음","projects":{}}
bad=[]
for p in meta['projects']:
    f=glob.glob(os.path.join(root,'쟁점보고서',p['id']+'_*.md'))[0]
    txt=open(f,encoding='utf-8').read()
    blocks=re.split(r'\n(?=### 쟁점 \d+\.)',txt)
    issues=[]
    for b in blocks[1:]:
        title=re.match(r'### 쟁점 (\d+)\. (.+)',b)
        tagline=re.search(r'`종류: ([^`]+)` · `결론: ([^`]+)` · `중요도: ([^`]+)` · `출처: ([^`]+)`',b)
        if not tagline: bad.append((p['id'],title.group(1))); continue
        types=[t.strip() for t in tagline.group(1).split(' / ')]
        tid=[kw(t,TK) for t in types]
        prim=next((x for x in tid if x),'other')
        ev=re.search(r'■ 현황\n((?:- .+\n?)+)',b) or re.search(r'\n((?:- .+\n?){1,3})',b)
        evidence=' '.join(l[2:].strip() for l in ev.group(1).strip().split('\n')[:3]) if ev else ''
        srcs=[kw(s,SK) for s in re.split(r', ',tagline.group(4))]
        srcs=sorted(set(x if x else 'own' for x in srcs))
        to=next((t for t,x in zip(types,tid) if x is None),tagline.group(1)) if prim=='other' else ''
        to=re.sub(r'^기타\((.*)\)$',r'\1',to)
        issues.append({"no":int(title.group(1)),"type":prim,"type_other":to,"types_all":[x or 'other' for x in tid],
          "summary":title.group(2).strip(),"evidence":evidence[:600],"conclusion":match(tagline.group(2),C) or 'note',
          "importance":match(tagline.group(3),I) or 'should',"source":srcs})
    out['projects'][p['id']]={"title":p['title'],"issues":issues}
json.dump(out,open(os.path.join(root,'쟁점보고서/ai_쟁점_태그.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('bad',bad)
for pid,v in out['projects'].items():
    print(pid,v['title'],len(v['issues']),[ (i['type'],i['conclusion'],i['importance']) for i in v['issues']][:2])
