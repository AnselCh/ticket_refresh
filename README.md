# 本機執行建議先用虛擬環境
1.
```
  virtualenv ticket_env  #建立虛擬環境
  ticket_env\Scripts\activate   #進入虛擬環境
```
2.
```
 pip install -r requirements.txt
```

3.
```
 python main.py
```

4. 終端機會詢問要監聽的網址，輸入完按enter
再來會詢問監聽的票券範圍，較大的場館都會分不同票種 ，拓元官網HTML會使用id=group_numbe來編號，請使用瀏覽器進入開發者設定查詢，若只想監聽單一票種，監聽範圍請輸入一樣的數字就好
ex:
```
HTML
<ul id="group_0" class="area-list" style=""><li><span style="background: #005fbf;">&nbsp;</span><font color="#AAAAAA">特A1區4200 Sold out</font></li><li><span style="background: #005fbf;">&nbsp;</span><font color="#AAAAAA">特A2區4200 Sold out</font></li><li><span style="background: #56aaff;">&nbsp;</span><font color="#AAAAAA">特B區3800 Sold out</font></li></ul>
```
這時候範圍都輸入0就好了。

