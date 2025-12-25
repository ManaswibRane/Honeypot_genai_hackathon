import sqlite3, os, pwd, grp, stat, sys

DB="/var/lib/honeypot/state.db"
layer=int(sys.argv[1])

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("SELECT path,type,content,owner,mode FROM filesystem WHERE layer=?", (layer,))
for path,t,content,owner,mode in cur.fetchall():
    if t=="dir":
        os.makedirs(path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path,"w") as f:
            f.write(content)
    uid=pwd.getpwnam(owner).pw_uid
    gid=grp.getgrnam(owner).gr_gid
    os.chown(path,uid,gid)
    os.chmod(path,int(mode,8))

print(f"[+] Layer {layer} materialized")
