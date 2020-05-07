# translate_pdf
Translate your *.pdf* file from and into any language supported by translate.yandex.ru. And get nice output in both *.html* and *.pdf* formats. 

The tool takes *.pdf* document **->** converts it into text **->** translates the text chunk-by-chunk (set TRANSLATION_CHUNKS to 1 if you translate a small file) **->** creates an *.html* file with a 2-column table (source - translation) **->** converts *.html* to *.pdf* 

The tool ensures strong linkage between the original and translated text so that you could easily access original text in case that the text is not translated well.

The tool does not support rendering tables / figures from the source document and creates a bit noisy output.

Future development is needed to make the translation clean and of higher quality (e.g. paid connection to DeepL's API instead of Yandex's one). Design issues also need some consideration. Also, there's an idea to pack the tool into a Telegram / Slack / etc. chat-bot to make the translation more accessible
