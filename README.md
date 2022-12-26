# WebTeaPest
An system for tea disease identification  
Link to our website: http://140.112.183.138:1007/

- teadiagnose 
  - settings.py # settings for Django, database, linebot, …
  - urls.py # urls for webpages, APIs, …
- checkpoints # model files (.pth file) 
  - tea
  - cucumber
  - tea bud
- imgUp # app for webpage # other apps based on the functions defined here
  - demo.py # basic detection functions
  - models.py # interactions between detections and database
  - views.py # logics for handling requests
- tealinebot # app for linebot
  - demo.py 
  - models.py
  - views.py
- iBp # app for APIs
  - demo.py 
  - views.py 
- templates # html files for webpage
- media # saved images
