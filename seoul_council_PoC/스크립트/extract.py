import sys,json,base64,os
src,out=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
a=s.find('id="sheet-data">')+len('id="sheet-data">'); b=s.find('</script>',a)
d=json.loads(s[a:b])
meta={k:v for k,v in d.items() if k!='projects'}; meta['projects']=[]
for p in d['projects']:
    pd=os.path.join(out,p['id']); os.makedirs(pd,exist_ok=True)
    r=p['review']; h=p['handout']
    for i,u in enumerate(r['images']):
        open(os.path.join(pd,f"검토_{r['pdf_pages'][i] if i<len(r['pdf_pages']) else i+1}.jpg"),'wb').write(base64.b64decode(u.split(',',1)[1]))
    labs=h.get('labels',[])
    for i,u in enumerate(h['images']):
        lab=labs[i] if i<len(labs) else f"x{i+1}"
        open(os.path.join(pd,f"설명서_{i+1:02d}_{lab}.jpg"),'wb').write(base64.b64decode(u.split(',',1)[1]))
    m={k:v for k,v in p.items() if k not in('review','handout')}
    m['review']={k:v for k,v in r.items() if k!='images'}; m['handout']={k:v for k,v in h.items() if k!='images'}
    meta['projects'].append(m)
json.dump(meta,open(os.path.join(out,'meta.json'),'w'),ensure_ascii=False,indent=1)
print('ok')
