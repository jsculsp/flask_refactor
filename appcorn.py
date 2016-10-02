from app.app import create_app

app = create_app()

# 在 gunicorn 上运行的命令
# nohup gunicorn -b '0.0.0.0:80' appcorn:app &