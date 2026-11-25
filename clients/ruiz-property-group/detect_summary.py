import subprocess,json,os,collections,glob
W=open('/tmp/ruizsite/W.txt').read().strip()
env=dict(os.environ,IMPECCABLE_NO_TELEMETRY='1')
out=subprocess.run(['bash',W+'/impeccable/scripts/impeccable','detect','--json']+glob.glob('site/*.html')+['site/styles.css','site/app.js'],capture_output=True,text=True,env=env).stdout
f=json.loads(out) if out.strip() else []
c=collections.Counter(x['antipattern'] for x in f)
bad={k:v for k,v in c.items() if k!='cramped-padding'}
print('DETECT_OK' if not bad else bad, dict(c))
