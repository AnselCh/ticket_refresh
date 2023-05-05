# 說明
請先點“TicketMonitor.zip”進入後，downloads後解壓縮  
進到執行檔後按著鍵盤control點擊TicketMonitor開啟
> 這支程式只能監控有分區域的票種，可以看下面範例圖，若是單一票種沒有分區域則不適用  
> 若執行檔可以成功執行，可將TicketMonitor以外的檔案都清除

# 使用執行檔(僅支援Ｍ1 M2 arm晶片)
1. 直接開啟TicketMonitor
2. 輸入要監聽的網址
3. 輸入要監聽範圍（看以下範例）
4. 若沒票會顯示ＸＸ區域No tickets available，幾秒過後會再重新載入一次，直到刷到票會跳出剩餘票券的視窗

# 查詢監聽範圍
1. 到網頁按右鍵點選inspect打開開發者工具
![1](https://github.com/AnselCh/ticket_refresh/blob/main/img/1.png)
2. 用開發者工具左上角的游標定位票種的tag
![2](https://github.com/AnselCh/ticket_refresh/blob/main/img/2.png)
3. 記起來是group_多少，之後可以帶入到監聽範圍
![3](https://github.com/AnselCh/ticket_refresh/blob/main/img/3.png)


# 本機執行建議先用虛擬環境(使用source code 執行)
1.
```
  virtualenv ticket_env  #建立虛擬環境
  win: ticket_env\Scripts\activate   #進入虛擬環境
  macOS: source ./ticket_env/bin/activate
```
2.
```
 pip3 install -r requirements.txt
```

3.
```
 python3 main.py
```
> arm架構晶片pyqt5需使用brew安裝！

4. 終端機會詢問要監聽的網址，輸入完按enter
再來會詢問監聽的票券範圍，較大的場館都會分不同票種 ，拓元官網HTML會使用id=group_numbe來編號，請使用瀏覽器進入開發者設定查詢，若只想監聽單一票種，監聽範圍請輸入一樣的數字就好
ex:
```
HTML
<ul id="group_0" class="area-list" style=""><li><span style="background: #005fbf;">&nbsp;</span><font color="#AAAAAA">特A1區4200 Sold out</font></li><li><span style="background: #005fbf;">&nbsp;</span><font color="#AAAAAA">特A2區4200 Sold out</font></li><li><span style="background: #56aaff;">&nbsp;</span><font color="#AAAAAA">特B區3800 Sold out</font></li></ul>
```
這時候範圍都輸入0就好了。

