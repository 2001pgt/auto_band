# 이 프로그램은 밴드에 새로운 글이 올라오면 자동으로 댓글을 다는 프로그램입니다.


<프로그램 다운로드 방법>
그림처럼 CODE 클릭수 DOWNLOAT ZIP 클릭 
아무 폴더에 압축해제
![캡처8](https://github.com/user-attachments/assets/f7f1f955-5eaf-4dcd-b676-f8a343fccbd2)

# 사용법
우선 Access Token 을 발급 받아주세요
방법은 https://github.com/voyageth/bandopenapi/blob/main/python/..%2Fperl%2FREADME.md 링크를 보시고 따라해 주세요

총 5개의 Access Token을 발급받아줍니다.

이제 프로그램을 실행시켜주세요.
올라와있는 자료들 전부 다운 받아 아무 폴더에 저장 후 dist폴더 안에 있는 app.exe 파일을 클릭하여 실행합니다.

![캡처3](https://github.com/user-attachments/assets/73ee4940-333d-4e5f-944c-313f76841754)

발급받은 토큰 5개를 각각 입력합니다.
Comment Text에 자동으로 달릴 댓글 내용을 입력합니다.
Submit Tokens 클릭

![캡처4](https://github.com/user-attachments/assets/0dc7a76a-1d9b-4841-8e52-00f73f761727)

저는 임시로 한개의 토큰만 입력하고 실행하겠습니다.(토큰 1개당 프로그램이 50분 정도 지속됩니다. 5개의 토큰이 전부 만료된 이후에는 자동 종료됨)
그러면 위 사진처럼 가입된 밴드명이 차례로 뜹니다.
그 중 자동으로 댓글 남기고 싶은 밴드를 클릭 후 Start Commenting 을 클릭하시면 프로그램이 실행됩니다.

아래는 실행 후 새 글이 올라왔을 때 예시

![캡처5](https://github.com/user-attachments/assets/1e3050a9-99ac-4ade-ad25-b2c7ae338e9a)

![캡처6](https://github.com/user-attachments/assets/96ca0811-26da-44e6-9c6d-30808f3bdb68)

![캡처7](https://github.com/user-attachments/assets/736ccffd-58a9-4677-bcee-7f94eeaba1cd)

# 주의 
완성된 프로그램이 아닌 제가 임시로 만든 프로그램임으로 사용중 에러가 발생하실 수 있습니다.

# 현재까지 발견한 버그
-새 글이 빠르게 여러개가 올라오면 처음 올라오는 글만 댓글이 달리고 그뒤로 5초정도 시간 동안 새 글에 댓글이 달리지 않는 버그가 있습니다.

# 코드 
app.py 를 실행하시면 프로그램 코드를 보실수 있습니다. 
거기서 CALL_DELAY = 3 이라고 되있는 부분이 API 호출 간격입니다
시간을 짧게 하면 더 빠르게 댓글이 달리지만 그만큼 호출 횟수가 빠르게 소모되어 프로그램 지속시간이 짧아집니다.
