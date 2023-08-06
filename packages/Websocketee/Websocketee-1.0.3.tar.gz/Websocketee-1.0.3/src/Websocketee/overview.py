from websocket import create_connection #line:2:from websocket import create_connection
import time #line:3:import time
import random #line:4:import random
import os ,sys ,requests #line:5:import os, sys,requests
import random #line:6:import random
import string #line:7:import string
import requests #line:8:import requests
import string #line:9:import string
import random #line:10:import random
from fake_useragent import UserAgent #line:12:from fake_useragent import UserAgent
ua =UserAgent ()#line:13:ua = UserAgent()
ua =str (ua )#line:14:ua = str(ua)
stt ='42["startPvtTableGame", {"_tableId":"'
edd = '"}]'
def create_connection (OOO0OOO000O0OOOO0 ,OOOOO0OOO00OO0O0O =None ,**O0OOOO0OOOOO0OO00 ):#line:17:def create_connection(url, timeout=None,  **options):
    ""#line:76:"""
    O00OO0O00O00O000O =O0OOOO0OOOOO0OO00 .pop ("sockopt",[])#line:77:sockopt = options.pop("sockopt", [])
    OO0OO0O0OOO0000OO =O0OOOO0OOOOO0OO00 .pop ("sslopt",{})#line:78:sslopt = options.pop("sslopt", {})
    O0O00O0OO00OO0O0O =O0OOOO0OOOOO0OO00 .pop ("fire_cont_frame",False )#line:79:fire_cont_frame = options.pop("fire_cont_frame", False)
    O000O000O00OOOO00 =O0OOOO0OOOOO0OO00 .pop ("enable_multithread",True )#line:80:enable_multithread = options.pop("enable_multithread", True)
    O000O00000O0O0O00 =O0OOOO0OOOOO0OO00 .pop ("skip_utf8_validation",False )#line:81:skip_utf8_validation = options.pop("skip_utf8_validation", False)
    O0OOO0OO0OO0O0O0O =class_ (sockopt =O00OO0O00O00O000O ,sslopt =OO0OO0O0OOO0000OO ,fire_cont_frame =O0O00O0OO00OO0O0O ,enable_multithread =O000O000O00OOOO00 ,skip_utf8_validation =O000O00000O0O0O00 ,**O0OOOO0OOOOO0OO00 )#line:85:skip_utf8_validation=skip_utf8_validation, **options)
    O0OOO0OO0OO0O0O0O .settimeout (OOOOO0OOO00OO0O0O if OOOOO0OOO00OO0O0O is not None else "")#line:86:websock.settimeout(timeout if timeout is not None else "")
    O0OOO0OO0OO0O0O0O .connect (OOO0OOO000O0OOOO0 ,**O0OOOO0OOOOO0OO00 )#line:87:websock.connect(url, **options)
    return O0OOO0OO0OO0O0O0O #line:88:return websock
ludoVerson ="7.7"#line:90:ludoVerson = "7.7"
versonCode ='243'#line:91:versonCode='243'
timeout =time .time ()+60 *20 #line:92:timeout = time.time() + 60*20
N =13 #line:94:N = 13
tr = '"_tableId":"'
trr= '","iWa'
res2 =''.join (random .choices (string .ascii_uppercase +string .digits ,k =N ))#line:95:res2 = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
rs2 =str (res2 )#line:96:rs2  = str(res2)
hoststs ='421["host_game", {"iLobbyId":"0", "hostTitle":"Ludo Classic 1", "bView":1}]'#line:98:hoststs = '421["host_game", {"iLobbyId":"0", "hostTitle":"Ludo Classic 1", "bView":1}]'
letters =string .ascii_uppercase #line:102:letters = string.ascii_uppercase
word1 =''.join (random .choice (letters )for OO0000OOOO00O0000 in range (1 ))#line:103:word1 =  ''.join(random.choice(letters) for i in range(1))
vf  = 'vPrivateCode":"'
vff = '"}]'
word2 =''.join (random .choice (letters )for O0O0000OO0O00O0OO in range (1 ))#line:104:word2 =  ''.join(random.choice(letters) for i in range(1))
numg =random .randint (1000 ,9999 )#line:107:numg = random.randint(1000,9999)
numg =str (numg )#line:109:numg = str(numg)
ir =  '"iTotalPlayer":'
iff = ',"aPlayers"'
numg =word1 +word2 +numg #line:110:numg = word1+word2+numg
iss = 'eStatus":"'
iss = '","iTurnCounter'
class HiddenPrints :#line:111:class HiddenPrints:
    def __enter__ (OOOOO0OO00O00O00O ):#line:112:def __enter__(self):
        OOOOO0OO00O00O00O ._original_stdout =sys .stdout #line:113:self._original_stdout = sys.stdout
        sys .stdout =open (os .devnull ,'w')#line:114:sys.stdout = open(os.devnull, 'w')
    def __exit__ (OOO000OO000OO0000 ,O0O0000OOOO000000 ,O000O0O0000OO0O0O ,OO0OOOO000O00OOOO ):#line:116:def __exit__(self, exc_type, exc_val, exc_tb):
        sys .stdout .close ()#line:117:sys.stdout.close()
        sys .stdout =OOO000OO000OO0000 ._original_stdout #line:118:sys.stdout = self._original_stdout
with HiddenPrints ():#line:121:with HiddenPrints():
    print ("This will not be printed")#line:122:print("This will not be printed")
class rk :#line:1
    response =requests .get ('https://api.ludoadda.co.in/apiv2.php?key=auth_key')#line:2
    auth_token =response .text 
ws ="hi"#line:157:ws = "hi"
def find_between (OO000O00OOO000OOO ,O00O0O00OO00OO000 ,OOOOOO00O0O00OO0O ):#line:160:def find_between( s, first, last ):
    try :#line:161:try:
        O0OO00OO0OOOO0OOO =OO000O00OOO000OOO .index (O00O0O00OO00OO000 )+len (O00O0O00OO00OO000 )#line:162:start = s.index( first ) + len( first )
        OOO00O0000O0OOOOO =OO000O00OOO000OOO .index (OOOOOO00O0O00OO0O ,O0OO00OO0OOOO0OOO )#line:163:end = s.index( last, start )
        return OO000O00OOO000OOO [O0OO00OO0OOOO0OOO :OOO00O0000O0OOOOO ]#line:164:return s[start:end]
    except ValueError :#line:165:except ValueError:
        return ""#line:166:return ""
def find_between_r (O000OO0OOO000OO0O ,OOOOOOOO00OO0OO00 ,OOOO0OO00OO00O0O0 ):#line:168:def find_between_r( s, first, last ):
    try :#line:169:try:
        O000OO00O00O0O000 =O000OO0OOO000OO0O .rindex (OOOOOOOO00OO0OO00 )+len (OOOOOOOO00OO0OO00 )#line:170:start = s.rindex( first ) + len( first )
        OOO0O0000OOO0OOOO =O000OO0OOO000OO0O .rindex (OOOO0OO00OO00O0O0 ,O000OO00O00O0O000 )#line:171:end = s.rindex( last, start )
        return O000OO0OOO000OO0O [O000OO00O00O0O000 :OOO0O0000OOO0OOOO ]#line:172:return s[start:end]
    except ValueError :#line:173:except ValueError:
        return ""#line:174:return ""
class loop :#line:177:class  loop:
    def loops ():#line:178:def loops():
        while True :#line:180:while True:
            ws .send ("2")#line:181:ws.send("2")
            OO0O0O0OO000O0OO0 =ws .recv ()#line:182:kt = ws.recv()
            O0O000OO00OO0OO00 =find_between (OO0O0O0OO000O0OO0 ,'"iTotalPlayer":',',"aPlayers"')#line:183:s = find_between(kt, '"iTotalPlayer":',',"aPlayers"')
            O0O000OO0OO0O0000 =find_between (OO0O0O0OO000O0OO0 ,'eStatus":"','","iTurnCounter')#line:184:ss = find_between(kt, 'eStatus":"','","iTurnCounter')
            O00OOO0O00OOOO0OO =find_between (OO0O0O0OO000O0OO0 ,'userId":"','","iTurnId":1')#line:187:sss = find_between(kt, 'userId":"','","iTurnId":1')
            if time .time ()>timeout :#line:188:if time.time() > timeout:
                exit ()#line:189:exit()
            if O0O000OO00OO0OO00 ==2 :#line:192:if s==2:
                ws .send ('42["startPvtTableGame", {"_tableId":""}]')#line:196:ws.send('42["startPvtTableGame", {"_tableId":"'+tab+'"}]')
                print ("Starting game")#line:197:print("Starting game")
            elif O0O000OO00OO0OO00 =="2":#line:199:elif s=="2":
                ws .send ('42["startPvtTableGame", {"_tableId":""}]')#line:203:ws.send('42["startPvtTableGame", {"_tableId":"'+tab+'"}]')
                print ("Starting game")#line:204:print("Starting game")
            elif O0O000OO0OO0O0000 =="Finished":#line:208:elif ss=="Finished":
                print ("win")#line:209:print("win")
                print (O00OOO0O00OOOO0OO )#line:210:print(sss)
                exit ()#line:212:exit()
            time .sleep (0.2 )#line:214:time.sleep(0.2)
