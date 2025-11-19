# 1. ベースイメージの指定
# (Python 3.9がプリインストールされた最小限のLinux環境を使う)
FROM python:3.11.9-slim

# 2. コンテナ内の作業ディレクトリを指定
WORKDIR /app

# 3. 必要なファイルをコピー
# (まずrequirements.txtだけコピーする)
COPY requirements.txt .

# 4. 依存ライブラリのインストール
# (Dockerfileの指示に基づき、コンテナ環境内にインストールされる)
# Cコンパイラ (gcc) やビルドに必要なツールをインストールする
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# 5. アプリケーションコードをコピー
COPY . .

# Streamlit設定ファイルを作成
COPY .streamlit/config.prod.toml ~/.streamlit/config.toml
# RUN cp .streamlit/config.prod.toml ~/.streamlit/config.toml

# Streamlit設定を環境変数で上書き (config.tomlを無視)
ENV STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS="0.0.0.0" \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLESTATICSERVING=false \
    STREAMLIT_BROWSER_SERVERADDRESS="0.0.0.0" \
    STREAMLIT_BROWSER_SERVERPORT=8080 \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    STREAMLIT_CLIENT_TOOLBARMODE="viewer" \
    STREAMLIT_CLIENT_SHOWSIDEBARNAVIGATION=false \
    STREAMLIT_UI_HIDETOPBAR=true \
    STREAMLIT_THEME_BASE="light" 

# 7. コンテナ起動時に実行するコマンド
# (Streamlitを $PORT で起動する)
CMD ["streamlit", "run", "app.py"]
