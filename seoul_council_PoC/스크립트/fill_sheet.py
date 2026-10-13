import sys,json,re,glob,os,datetime
src,root,out=sys.argv[1],sys.argv[2],sys.argv[3]
s=open(src,encoding='utf-8').read()
tags=json.load(open(os.path.join(root,'쟁점보고서/ai_쟁점_태그.json'),encoding='utf-8'))
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
A={"sheet_id":tags['sheet_id'],"version":1,"author":"AI 초안(budget-issue-extractor)","updated_at":now,"saved_at":now,"projects":{}}
for pid,v in tags['projects'].items():
    f=glob.glob(os.path.join(root,'쟁점보고서',pid+'_*.md'))[0]; txt=open(f,encoding='utf-8').read()
    card=re.search(r'## 사업 요약 카드\n\n```\n(.+?)```',txt,re.S).group(1)
    overall=re.search(r'종합 조정 의견: (.+)',card).group(1).strip()
    issues=[]
    for it in v['issues']:
        # 조정 의견 한 줄을 요지에 덧붙임
        blk=re.search(r'### 쟁점 %d\. .+?(?=\n### |\n## |\Z)'%it['no'],txt,re.S).group(0)
        adj=re.search(r'■ 조정 의견\n- (.+)',blk) or re.search(r'- 조정 의견: (.+)',blk)
        summ=it['summary']+(' / 조정: '+re.sub(r'\*\*','',adj.group(1)).strip() if adj else '')
        issues.append({"type":it['type'],"type_other":it['type_other'] if it['type']=='other' else "",
            "summary":summ,"evidence":re.sub(r'\*\*','',it['evidence']),"conclusion":it['conclusion'],
            "importance":it['importance'],"source":it['source']})
    note=("[AI 초안] 종합 조정 의견: "+overall+" · 외부 근거는 웹 검색 요약 기준, 서울시의회 회의록은 접속 차단으로 미확인. 상세: 쟁점보고서/"+os.path.basename(f))
    A['projects'][pid]={"done":True,"no_issue":False,"issues":issues,"note":note}
js=json.dumps(A,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
a=s.index('<script type="application/json" id="answers">')+len('<script type="application/json" id="answers">'); b=s.index('</script>',a)
assert s[a:b].strip()=='null'
s2=s[:a]+js+s[b:]
s2=s2.replace('<title>사업 검토 정답지</title>','<title>사업 검토 정답지 (AI 초안)</title>',1)
open(out,'w',encoding='utf-8').write(s2)
# 검증: 필수 칸
miss=[(pid,i) for pid,p in A['projects'].items() for i,it in enumerate(p['issues']) if not(it['type'] and it['summary'] and it['conclusion'] and it['importance']) or (it['type']=='other' and not it['type_other'])]
print('written',len(s2),'missing',miss, 'issues',sum(len(p['issues']) for p in A['projects'].values()))
