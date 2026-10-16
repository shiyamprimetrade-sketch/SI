import json,platform,statistics,time
from si import run,run_compiled,compile_source,execute
source='PUSH 1\n'+('PUSH 1\nADD\n'*100)+'PRINT'
code=compile_source(source)
N=2000
results={}
for name,fn in [('source_interpreter',lambda:run(source)),('compile_each_run',lambda:run_compiled(source)),('precompiled_vm',lambda:execute(code))]:
    samples=[]
    for _ in range(5):
        t=time.perf_counter()
        for i in range(N): fn()
        samples.append((time.perf_counter()-t)/N*1000)
    results[name]={'median_ms_per_run':statistics.median(samples),'samples_ms_per_run':samples}
print(json.dumps({'python':platform.python_version(),'platform':platform.platform(),'iterations_per_sample':N,'results':results},indent=2))