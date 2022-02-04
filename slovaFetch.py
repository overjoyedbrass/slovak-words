import httpx
import json
import time

slova = []
URL = "https://slovnik.aktuality.sk/pravopis/slovnik-sj/{}/{}"
letters = 'abcdefghijklmnopqrstuvwxyz'

opener = '<div class="four columns">'
closerer = 'id="nav"'

start = time.time()

for l in letters:
    print(f"Stahujem pre pismeno {l}, uplynuty čas: {(time.time()-start)}")
    page = 1
    while True:
        r = httpx.get(URL.format(l, page))
        if not r.is_success:
            break

        l_i = str.find(r.text, opener)
        if l_i == -1:
            break
        
        p_i = str.find(r.text, closerer)
        if p_i == -1:
            break

        goodPart = r.text[l_i:p_i]
        words = goodPart.split('</a>')
        words = list(map(
            lambda x: x.split('>')[-1], 
            words
        ))[:-1]
        slova += words
        page += 1

print(f"Hotovo. {time.time()-start} ms")

f = open("words.txt", mode='w', encoding='utf-8')
for w in slova:
    try:
        f.write(w)
    except:
        pass

    f.write('\n')
f.close()