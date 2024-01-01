# auto-bilibili-helper 
這是一個用於自動登入 Bilibili 並完成日常任務的 Python CLI 工具。它可以幫助用戶自動執行如簽到、分享影片、瀏覽影片等任務，同時提供靈活的命令行選項來控制這些功能。

### 功能
使用 Cookie 登入: 透過提供的 Cookie 文件來登入您的 Bilibili 賬號。

- 自動直播簽到: 自動完成 Bilibili 直播的簽到任務。
- 分享影片: 自動分享一個影片到您的 Bilibili 賬號。
- 瀏覽影片: 自動瀏覽一個影片。
- 投幣: 可以選擇是否給影片投幣。

### 安裝
此工具需要 Python 3 環境。您可以通過以下命令安裝所需的依賴：
`pip install requests`

### 使用方法
`python3 ./bilibili.py [選項]`

### 可用選項
- --cookieFile: 指定 cookie.txt 文件的絕對路徑 [必要]

- --logfile: 啟用日誌檔案寫入。 
- --no-logfile: 停用日誌檔案寫入。[預設不寫入]
- --liveSign: 啟用自動直播簽到。  [預設啟動]
- --no-liveSign: 停用自動直播簽到。
- --shareVideo: 啟用影片分享。    [預設啟動]
- --no-shareVideo: 停用影片分享。
- --watchVideo: 啟用影片瀏覽。    [預設啟動]
- --no-watchVideo: 停用影片瀏覽。
- --coins: 啟用投幣。 [預設啟動]
- --no-coins: 停用投幣。

### 獲取 cookie.txt
1. 打開瀏覽器登入  [Bilibili 官網](https://www.bilibili.com/)
2. 登入您的賬號之後，按下 F12 鍵開啟開發者工具。
3. 在開發者工具中，切換到 Network 標籤頁。
4. 在 Bilibili 的主頁面上重新加載一次（您可以按下瀏覽器的刷新按鈕或按 F5 鍵）。
5. 在 Network 標籤頁中，尋找名為 www.bilibili.com 的 HTTP 請求。
6. 點擊該請求，在出現的側邊欄中找到 Headers 標籤頁。
7. 在 Headers 頁面中向下滾動，直到找到 Request Headers 部分，裡面會有一個 Cookie 欄目。
8. 複製 Cookie 欄目中的全部內容。
9. 將這些內容粘貼到一個新建的文本文件中，並將其保存為 cookie.txt。

PS: 請確保您複製的是整個 Cookie 欄目的內容，並且不要遺漏任何部分，為了您賬戶的安全，請妥善保管這個 cookie.txt 文件，不要與他人共享或公開。


### 範例

- 啟動所有功能, 並且入日誌
`python3 ./bilibili.py --logfile --liveSign --shareVideo --watchVideo --coins --cookieFile /configs/bilibili/cookie.txt`

- 僅執行瀏覽影片和直播簽到，且不進行日誌檔案寫入：
`python3 ./bilibili.py --no-logfile --liveSign --no-shareVideo --watchVideo --no-coins --cookieFile /configs/bilibili/cookie.txt`

### 注意事項
- 確保您的 Cookie 文件是最新的，以避免登入問題。
- 此工具僅用於學術和研究目的，請勿用於任何違法行為。
- 使用此工具可能違反 Bilibili 的使用條款，請自行承擔相關風險。