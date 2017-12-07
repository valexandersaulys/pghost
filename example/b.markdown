Title: Procmail 搭配 Script
Slug: procmail-pipe-to-python-script
Date: 2016-03-29 15:56:26
Categories: Python
Tags: mail,procmail,python
---
我們每天都在收信，那有沒有某些信件是你想挑出來，特別處理的？有的話可以使用 [procmail](https://en.wikipedia.org/wiki/Procmail) 這個程式來幫你。
<!--more-->
首先你家目錄下的 `.forward` 檔案內容必須是
```sh
"|/usr/local/bin/procmail"
```
確定信件會被 pipe 給 procmail 處理。

那現在重點會擺在 `.procmailrc` 這個檔案，這裡只會粗淺的講一下實現「用 procmail 將信件傳遞給 script 執行」。

假設我想要將從 `ken8203@love.com` 寄來的信傳至 `mail_processing.py` 做處理
```sh
:0Wc:
* ^From.*ken8203@love.com
| /usr/local/bin/python $HOME/mail_processing.py
```
如此一來就可以正確的執行了，更細節的 filter 寫法可以到網路上查查，挺多的！

OK，那 `mail_processing.py` 的改怎麼寫，才可以接住 pipe 過來的內容
```python
# -*- coding: utf-8 -*-

import sys
import email

full_msg = sys.stdin.readlines()
msg = email.message_from_string(''.join(full_msg))

with open('mail.txt', 'w') as fout:
    fout.write(msg['to'] + '\n')
    fout.write(msg['from'] + '\n')
    fout.write(''.join(full_msg))
```
就是這麼簡單！

## Note
如果你的 `mail.txt` 遲遲不出來（有時候會 delay 一下，讓子彈飛一會兒），你可以考慮寫進 log 看看問題在哪，修改一下 `.procmailrc`
```sh
VERBOSE=on
LOGFILE=$HOME/procmail.log

:0Wc:
* ^From.*ken8203@love.com
| /usr/local/bin/python $HOME/mail_processing.py
```
加入1~2行，就能自己 debug 囉！
