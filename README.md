# roadmap-back

Roadmap API Server (Backend)

## Architecture

**Architecture**

![](fig/infra_architecture.drawio.svg)

**CI/CD**

![](fig/ci_cd.drawio.svg)

**Architecture-code**

- クリーンアーキテクチャを用いる
- 以下の順で開発すると良い (推奨)
    1. モデルの作成
    2. レポジトリの作成
    3. サービスの作成
    4. ルータの作成

```shell
app
├── config.py # .env ファイルの読み出し
├── main.py # アプリの起動, ミドルウェアの定義
├── model # モデル
├── repository # DB などへの永続化を隠蔽
│   ├── cooud_firestore # 継承先
│   │   └── task.py 
│   └── task.py # 継承元
├── router # エンドポイントの切り分け
│   └── task.py
└── service #　ビジネスロジックを定義
    └── task.py
```

## Development

### 前提

- Firebase Admin SDK の秘密鍵が必要
- Docker
- docker-compose
- make
- エディタ

### 初期化

1. `app/` に `serviceAccountKey.json` を配置

```shell
mv serviceAccountKey.json path/to/app/
```

2. `.env.example` を `.env` にコピー

```shell
cp .env/example .env
```

3. `make up`

```shell
make up
```

4. アクセス

* api
    * [http://localhost:8080](http://localhost:8080)
* docs
    * [http://localhost:8080/docs](http://localhost:8080/docs)
* redoc
    * [http://localhost:8080/redoc](http://localhost:8080/redoc)
* openapi.json
    * [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)

5. `app/`以下のコードを編集すると自動で反映されます（ページリロードは必須）

### 終了時

1. コンテナをダウンさせる

```shell
make down
```

### 再開時

1. コンテナを起動

```shell
make up
```

## Command List

### docker-compose 関連

**プロセス確認**

```shell
make ps
````

**起動**

```shell
make up
````

**再起動**

```shell
make re
````

**再ビルド**

```shell
make reup
```

**停止**

```shell
make down
````

**ログを表示 (Cancel Ctrl+C)**

```shell
make logs
````

**コンテナに入る**

```shell
make api
```