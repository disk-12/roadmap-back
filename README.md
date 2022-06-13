# roadmap-back

**Architecture**

![](fig/infra_architecture.drawio.svg)

**CI/CD**

![](fig/ci_cd.drawio.svg)

Roadmap API Server (Backend)

## Development

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
    * `http://localhost:8080`
  * docs
    * `http://localhost:8080/docs`
  * redoc
    * `http://localhost:8080/redoc`
  * openapi.json
    * `http://localhost:8080/openapi.json`
## Command List

```shell
# docker-compose 起動
make up

# docker-compose 再ビルド
make reup

# docker-compose 停止
make down

# docker-compose ログを表示
make logs

# docker-compose api のコンテナに入る
make api
```