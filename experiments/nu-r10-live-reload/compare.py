"""Compare the accepted live/fresh trace pair without changing either trace."""
import argparse, hashlib, json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("live",type=Path); p.add_argument("fresh",type=Path); p.add_argument("output",type=Path)
a=p.parse_args()
def load(path):
    rows=[json.loads(x) for x in path.read_text().splitlines()]
    by={}
    for row in rows: by.setdefault(row["event"],[]).append(row)
    return rows,by
def one(by,name):
    xs=by.get(name,[])
    assert len(xs)==1,(name,len(xs))
    return xs[0]
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"))
def digest(x): return hashlib.sha256(canon(x).encode()).hexdigest()
lr,l=load(a.live); fr,f=load(a.fresh)
lc,fc=one(l,"checkpoint-halted"),one(f,"checkpoint-halted")
lp=one(l,"post-reload-pre-advance")
lu,fu=one(l,"post-update-halted"),one(f,"post-update-halted")
ln,fn=one(l,"next-halted-stable"),one(f,"next-halted-stable")
li=one(l,"reload-installed")
for by in (l,f):
    assert one(by,"result")["pass"] is True
    assert one(by,"oracle-data-controls")=={"event":"oracle-data-controls","score100Rejected":True,"resetRejected":True,"wrongBrickRejected":True}
    schedule=one(by,"event-schedule")
    assert schedule["order"]==["TimeUpdate","Update"] and schedule["gameDeltaUpdates"]==[1]
    assert schedule["updates"]==schedule["timeUpdates"]==1
for row in (lc,fc,lp,lu,fu,ln,fn):
    assert row["leftInputs"]==row["rightInputs"]==0 and row["projectionErrors"]==[]
assert lc["model"]==fc["model"]==lp["model"]
assert lc["projection"]==fc["projection"]==lp["projection"]
assert lu["model"]==fu["model"]==ln["model"]==fn["model"]
assert lu["projection"]==fu["projection"]==ln["projection"]==fn["projection"]
assert (lu["model"]["time"],lu["model"]["score"],lu["model"]["lives"],len(lu["model"]["bricks"]))==(150,300,5,28)
assert "@455" not in [x["name"] for x in lu["model"]["bricks"]]
assert lu["model"]["ballPosition"]==["C2800000","42600000","00000000"]
assert lu["model"]["ballDirection"]==["00000000","BF800000","00000000"]
assert li["reward"]==200 and li["actualType"]==lp["rawType"] and li["dispatcherModelType"]==lp["rawType"]
assert lp["codeReloadEvents"]==1
out={
 "pass":True,
 "checkpoint_model_sha256":digest(lc["model"]),"checkpoint_projection_sha256":digest(lc["projection"]),
 "post_model_sha256":digest(lu["model"]),"post_projection_sha256":digest(lu["projection"]),
 "actual_fsi_type":li["actualType"],"dispatcher_type":li["dispatcherType"],"dispatcher_model_type":li["dispatcherModelType"],
 "event_word":["TimeUpdate","Update"],"game_delta_updates":[1],
 "post_summary":{"time":150,"score":300,"lives":5,"bricks":28,"removed":["@455"],"ball_position_bits":lu["model"]["ballPosition"],"ball_direction_bits":lu["model"]["ballDirection"]},
 "live_trace_sha256":hashlib.sha256(a.live.read_bytes()).hexdigest(),"fresh_trace_sha256":hashlib.sha256(a.fresh.read_bytes()).hexdigest(),
}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
