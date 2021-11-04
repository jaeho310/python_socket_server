# socket_server

IOC DI를 통한 layered architecture를 적용한 tcp socket 서버입니다.

heart_beat 스레드를 만들어 클라이언트의 접속을 계속 확인하는 로직을 넣었으며

tcp 패킷이 밀려 여러건의 데이터가 붙어오는 경우의 핸들링 작업도 포함하였습니다.

단 tcp 버퍼가 모두 차는 경우의 에러는 막지 않았습니다. (read즉시 비즈니스 로직을 처리하지않고 저장한후 저장된 데이터를 폴링 방법 등 으로 처리할 수 있습니다

클라이언트별로 스레드를 잡고 whlie문을 돌려 클라이언트의 요청이 올때까지 서버의 스레드를 블락시키는 방법으로 사용했으며

production레벨에서 사용할때는 서버의 스레드를 블락시키지않도록 해야합니다.

async begin select 등의 접두사가 붙어있는(callbcak을 등록시켜 event가 왔을때 서버가 깨어나는) read 방식을 사용해야합니다.(파이썬은 select)

<br>

## 기능
- 사용자는 UID를 통해 서버에 데이터를 넣고 확인할 수 있습니다.
- statefull한 socket서버의 특징 확인을 위해 서버가 클라이언트에게 실시간 공지사항을 내려주는 기능도 넣었습니다.

## 사용 기술
- socket
- thread
- sys.arg
- re

## 사용방법
서버와 클라이언트 모두 cli환경의 user interface가 제공됩니다.

단 python argument 실습을 위해 server는 데이터 저장방법을 위해 python argument를 받도록 하였습니다.

```
ex1). python main.py mem -> 메모리 디비 사용

ex2). python main.py rdb -> rdb 사용(파일디비인 sqlite를 사용)
```

<br>

## protocol
```
'get<1>' 이라는 요청이 오면 1이라는 key에 있는 data를 클라이언트에게 내려주며
'put<1,hello>' 라는 요청이 오면 1이라는 key에 hello라는 value를 저장합니다.

tcp 패킷이 밀리는 것을 대비하여 <> 기호를 추가했습니다.
(tcp는 패킷중 일부분이 어떤 라우터에 걸려 늦게오는경우 tcp는 모든 패킷을 기다리므로 이전요청과 다음요청이 한꺼번에 가는경우가 자주 발생합니다.)

ex1) <>를 사용하지 않고 단순히 'get,1' 이라는 프로토콜을 사용할시 패킷이 밀려 'get,1get,2' 처럼 데이터가 왔을때 처리하기가 까다롭습니다.
ex2) 'get<1>get<2>' 라는 방식으로 데이터가오면 >를 구분자로 두개의 메시지를 구분하고 <구분자를 통해 get,put과 data를 구분할 수 있습니다.
```


## 아키텍쳐
앨리스터 코오번의 Hexagonal Architecture 를 적용하므로써 관심사를 분리한 애플리케이션입니다.

소프트웨어를 계층으로 분리하고 의존성 규칙을 준수한다면 본질적으로 테스트하기 쉬운 시스템이 되고(테스트 관심사가 아닌 컴포넌트는 Mock, Stub 등 test double로 치환)

업무로직이나 데이터베이스의 변경이 필요한 시점에 각 요소를 비교적 쉽게 교체할 수 있다는 장점이 있습니다.

<br>
<br>

- layer는 presentation(interface) 계층, application(Business Layer, persistence Laye) 계층, infrastructure(db) 계층으로 나눴습니다.

<img src="https://media.vlpt.us/images/sj950902/post/94b0f3bb-dbd9-43e2-ab31-d6d429553c0f/image.png" width=50%>

<br>
<br>
<br>

- 컴포넌트는 controller계층, usecase계층, repoisotry계층 으로 나눴습니다

<img src="https://miro.medium.com/max/1400/0*nPHeRaVlP2V9Gq_5" width=50%>


계층구조의 장점과 추상에 의존한 느슨한 결합의 장점을 확인하기 위해

python argument 에 따라 repository의 구현체를 rdb, memorydb로 구분하여 사용하도록 하였습니다.
```
.
|-- main.py
|-- application
|   |-- custom_logger.py
|   |-- interactor.py
|   |-- repository.py
|   `-- usecase.py
|-- infrastructure
|   |-- db_sqlite3.py
|   |-- socket_server.py
|   `-- user_inerface.py
`-- presentation
    `-- interface
        |-- controller
        |   `-- client_controller.py
        `-- gateway
            |-- memory_repository.py
            `-- rdb_repository.py
```

## logging
singleton 패턴을 활용하여 간단한 콘솔 로그를 만들었습니다.

서버에서 정상적으로 프로그램을 종료하면

fileio를 통해 txt파일로 저장하도록 하였습니다.

<br>
<br>

## user interface
사용자 interface는 cli로 구축하였습니다.
현재 접속인원 확인, 로그확인(level별) 등의 기능을 포함하며

stateful 실습을 위하여 모든 사용자에게 공지사항을 보내는 기능을 추가하였습니다.

일반적인 http는 server는 클라이언트의 request가 있어야 서버가 response를 내려주지만,

커넥션을 유지하고있는 tcp socket server는 클라이언트의 요청이 없더라도 서버가 클리어언트에게 데이터를 줄 수 있습니다.

(네이버에서 웹툰을 보고있을때 사용자가 새로고침을 하지 않는다면 공지사항이 있어도 확인하지 못하지만, socket을 사용하는 경우(ex.게임) 실시간 공지사항을 확인할 수 있습니다.)
