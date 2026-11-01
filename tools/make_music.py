"""Original royalty-free background loop for reels. Usage: make_music.py <seconds> <out.wav> [bpm]
Upbeat, light electronic: soft chord pads, plucked arpeggio, kick, clap, hats. Fades in/out."""
import sys, wave, numpy as np
dur=float(sys.argv[1]); out=sys.argv[2]; bpm=float(sys.argv[3]) if len(sys.argv)>3 else 112
sr=48000; n=int(sr*dur); t=np.arange(n)/sr; beat=60/bpm
mix=np.zeros(n)
def note(f): return 440*2**((f-69)/12)
def env(length,a=0.005,r=0.2):
    k=np.arange(length)/sr; e=np.minimum(1,k/a)*np.exp(-k/r); return e
def add(sig,start):
    s=int(start*sr)
    if s>=n: return
    e=min(n,s+len(sig)); mix[s:e]+=sig[:e-s]
# chord progression (C major-ish, uplifting): Am F C G
prog=[[57,60,64],[53,57,60],[48,52,55,60],[55,59,62]]
bar=4*beat
for b in range(int(dur/bar)+1):
    ch=prog[b%4]
    L=int(bar*sr); k=np.arange(L)/sr
    pad=sum(np.sin(2*np.pi*note(m)*k)+0.3*np.sin(2*np.pi*note(m)*2*k) for m in ch)/len(ch)
    pe=np.minimum(1,k/0.3)*np.minimum(1,(bar-k)/0.3)
    add(0.16*pad*pe,b*bar)
    # bass on beats 1 and 3
    for q in (0,2):
        Lb=int(beat*sr); kb=np.arange(Lb)/sr
        add(0.28*np.sin(2*np.pi*note(ch[0]-12)*kb)*env(Lb,0.01,0.35),b*bar+q*beat)
    # arpeggio eighths
    arp=ch+[ch[1]+12]
    for i in range(8):
        m=arp[i%len(arp)]+12; Ln=int(beat/2*sr); kn=np.arange(Ln)/sr
        tone=np.sin(2*np.pi*note(m)*kn)+0.4*np.sin(2*np.pi*note(m)*3*kn)
        add(0.07*tone*env(Ln,0.003,0.12),b*bar+i*beat/2)
rng=np.random.default_rng(7)
for i in range(int(dur/beat)+1):
    st=i*beat
    Lk=int(0.25*sr); kk=np.arange(Lk)/sr
    f=50+90*np.exp(-kk/0.03)
    add(0.55*np.sin(2*np.pi*np.cumsum(f)/sr)*env(Lk,0.001,0.12),st)
    if i%2==1:
        Lc=int(0.2*sr); add(0.18*rng.standard_normal(Lc)*env(Lc,0.001,0.05),st)
    for h in (0.5,):
        Lh=int(0.05*sr); add(0.05*rng.standard_normal(Lh)*env(Lh,0.001,0.015),st+h*beat)
fade=np.minimum(1,np.minimum(t/0.8,(dur-t)/1.2)); mix*=fade
mix/=np.max(np.abs(mix))*1.12
st=np.stack([mix,np.roll(mix,240)],1)
with wave.open(out,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes())
print("ok")
