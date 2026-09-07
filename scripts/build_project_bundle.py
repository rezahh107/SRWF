#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, subprocess, tarfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'; FIXED=(2026,1,1,0,0,0)
def h(b): return hashlib.sha256(b).hexdigest()
def rb(p):
    x=ROOT/p
    if not x.is_file(): raise SystemExit(f'missing:{p}')
    return x.read_bytes()
def commit():
    if os.getenv('GITHUB_SHA'): return os.environ['GITHUB_SHA']
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
def zwrite(path, entries):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n in sorted(entries):
            i=zipfile.ZipInfo(n,FIXED); i.create_system=3; i.external_attr=0o100644<<16; i.compress_type=zipfile.ZIP_DEFLATED; z.writestr(i,entries[n])
def main():
    cfg=json.loads(rb('bundle/project-package.json')); ver=rb('bundle/VERSION').decode().strip(); root=cfg['runtime_root']; entries={}
    instr=rb(cfg['instructions_source']).decode('utf-8').replace('\r\n','\n').encode('utf-8')
    entries[f'{root}/02_PROJECT_INSTRUCTIONS.md']=instr
    for src,dst in cfg['runtime_source_mappings'].items(): entries[f'{root}/{dst}']=rb(src)
    arc=ROOT/'history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz'
    with tarfile.open(arc,'r:xz') as tf:
        mem={m.name:m for m in tf.getmembers() if m.isfile()}
        for name,dst in cfg['materialized_knowledge_sources'].items():
            f=tf.extractfile(mem[name]); entries[f'{root}/{dst}']=f.read()
    out=DIST/f"SRWF_GPT_Project_Package_v{ver}.zip"; DIST.mkdir(exist_ok=True); zwrite(out,entries)
    errors=[]
    with zipfile.ZipFile(out) as z:
        names=z.namelist(); bad=z.testzip()
        if bad: errors.append(f'crc:{bad}')
        if len(names)!=len(set(names)): errors.append('duplicate_paths')
        tops={n.split('/')[0] for n in names}
        if tops!={root}: errors.append(f'top_roots:{sorted(tops)}')
        rel=[n[len(root)+1:] for n in names]
        if not all(x=='02_PROJECT_INSTRUCTIONS.md' or x.startswith('PROJECT_SOURCES/') for x in rel): errors.append('runtime_allowlist_violation')
        if rel.count('02_PROJECT_INSTRUCTIONS.md')!=1: errors.append('instructions_count')
        source_count=sum(1 for x in rel if x.startswith('PROJECT_SOURCES/') and not x.endswith('/'))
        txt=z.read(f'{root}/02_PROJECT_INSTRUCTIONS.md').decode('utf-8')
        if len(txt)>cfg['max_instruction_characters']: errors.append(f'instructions_chars:{len(txt)}')
        for marker in ['شروع','GitHub repository `rezahh107/SRWF`','STATE_NOT_PERSISTED','PROJECT_SOURCES/04_SEMANTIC_FIELD_CONTRACT.yaml']:
            if marker not in txt: errors.append(f'instructions_missing:{marker}')
        for forbidden in cfg['forbidden_runtime_names']:
            if any(Path(x).name==forbidden for x in rel): errors.append(f'build_only_leak:{forbidden}')
        expected=1+len(cfg['runtime_source_mappings'])+len(cfg['materialized_knowledge_sources'])
        if len(rel)!=expected: errors.append(f'entry_count:{len(rel)}!={expected}')
    report={'status':'PASS' if not errors else 'FAIL','package':out.name,'generator_standard':cfg['governing_generator_standard'],'generator_standard_sha256':cfg['governing_generator_standard_sha256'],'canonical_standard_sha256':cfg['embedded_canonical_standard_sha256'],'source_commit':commit(),'instruction_characters':len(instr.decode()),'runtime_source_count':source_count,'zip_entry_count':len(entries),'errors':errors,'remaining_not_proven':['future model compliance','deterministic retrieval/use of every Project Source','deployed ChatGPT Project behavior']}
    (DIST/f'{out.name}.build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    digest=h(out.read_bytes()); (DIST/f'{out.name}.sha256').write_text(f'{digest}  {out.name}\n',encoding='utf-8')
    print(json.dumps({**report,'sha256':digest},ensure_ascii=False)); return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
